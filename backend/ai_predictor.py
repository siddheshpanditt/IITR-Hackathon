try:
    import numpy as np
except ImportError:
    # Fallback for systems without numpy
    class NumpyFallback:
        @staticmethod
        def polyfit(x, y, deg):
            # Simple linear regression fallback
            if len(x) < 2:
                return [0, 0]
            n = len(x)
            sum_x = sum(x)
            sum_y = sum(y)
            sum_xy = sum(x[i] * y[i] for i in range(n))
            sum_x2 = sum(x[i] * x[i] for i in range(n))
            
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x) if (n * sum_x2 - sum_x * sum_x) != 0 else 0
            return [slope, 0]
        
        @staticmethod
        def mean(arr):
            return sum(arr) / len(arr) if arr else 0
    
    np = NumpyFallback()
import logging
from datetime import datetime, timedelta
from collections import deque
import json

logger = logging.getLogger(__name__)

class AIPredictor:
    def __init__(self):
        self.cpu_history = deque(maxlen=100)
        self.memory_history = deque(maxlen=100)
        self.latency_history = deque(maxlen=100)
        self.failure_patterns = []
        
    def add_metrics(self, cpu, memory, latency, is_online):
        """Add new metrics for analysis"""
        timestamp = datetime.now()
        
        self.cpu_history.append({'value': cpu, 'timestamp': timestamp, 'online': is_online})
        self.memory_history.append({'value': memory, 'timestamp': timestamp, 'online': is_online})
        self.latency_history.append({'value': latency, 'timestamp': timestamp, 'online': is_online})
        
    def predict_failure_probability(self):
        """Predict probability of failure in next 30 minutes"""
        if len(self.cpu_history) < 10:
            return {'probability': 0, 'confidence': 'low', 'factors': []}
        
        risk_factors = []
        risk_score = 0
        
        # CPU trend analysis
        recent_cpu = [m['value'] for m in list(self.cpu_history)[-10:]]
        cpu_trend = np.polyfit(list(range(len(recent_cpu))), recent_cpu, 1)[0]
        
        if cpu_trend > 2:  # Increasing CPU usage
            risk_score += 0.3
            risk_factors.append(f"CPU usage trending up ({cpu_trend:.1f}%/min)")
        
        if recent_cpu[-1] > 85:  # High current CPU
            risk_score += 0.4
            risk_factors.append(f"High CPU usage ({recent_cpu[-1]:.1f}%)")
            
        # Memory analysis
        recent_memory = [m['value'] for m in list(self.memory_history)[-10:]]
        if recent_memory[-1] > 90:
            risk_score += 0.5
            risk_factors.append(f"Critical memory usage ({recent_memory[-1]:.1f}%)")
        elif recent_memory[-1] > 80:
            risk_score += 0.2
            risk_factors.append(f"High memory usage ({recent_memory[-1]:.1f}%)")
            
        # Latency spikes
        recent_latency = [m['value'] for m in list(self.latency_history)[-5:]]
        avg_latency = np.mean(recent_latency) if recent_latency else 0
        
        if avg_latency > 3000:
            risk_score += 0.3
            risk_factors.append(f"High latency ({avg_latency:.0f}ms)")
            
        # Historical failure patterns
        recent_failures = [m for m in list(self.cpu_history)[-20:] if not m['online']]
        if len(recent_failures) > 2:
            risk_score += 0.4
            risk_factors.append(f"Recent instability ({len(recent_failures)} failures)")
            
        probability = min(risk_score, 0.95)
        confidence = 'high' if len(self.cpu_history) > 50 else 'medium' if len(self.cpu_history) > 20 else 'low'
        
        return {
            'probability': round(probability, 2),
            'confidence': confidence,
            'factors': risk_factors,
            'recommendation': self._get_recommendation(probability, risk_factors)
        }
        
    def _get_recommendation(self, probability, factors):
        """Get AI recommendation based on prediction"""
        if probability > 0.7:
            return "CRITICAL: Immediate intervention required. Consider restarting services."
        elif probability > 0.4:
            return "WARNING: Monitor closely. Prepare for potential issues."
        elif probability > 0.2:
            return "CAUTION: System showing stress indicators."
        else:
            return "HEALTHY: System operating normally."
            
    def analyze_root_cause(self, failure_data):
        """Perform automated root cause analysis"""
        causes = []
        
        # Analyze metrics before failure
        pre_failure_window = failure_data.get('pre_failure_metrics', [])
        
        if not pre_failure_window:
            return {'primary_cause': 'Unknown', 'contributing_factors': [], 'confidence': 'low'}
            
        # Check for resource exhaustion
        high_cpu = any(m.get('cpu', 0) > 90 for m in pre_failure_window[-5:])
        high_memory = any(m.get('memory', 0) > 95 for m in pre_failure_window[-5:])
        high_latency = any(m.get('latency', 0) > 5000 for m in pre_failure_window[-3:])
        
        if high_memory:
            causes.append({'cause': 'Memory Exhaustion', 'confidence': 0.9, 'evidence': 'Memory usage >95%'})
        if high_cpu:
            causes.append({'cause': 'CPU Overload', 'confidence': 0.8, 'evidence': 'CPU usage >90%'})
        if high_latency:
            causes.append({'cause': 'Network Issues', 'confidence': 0.7, 'evidence': 'Latency >5000ms'})
            
        # Pattern matching with historical failures
        similar_patterns = self._find_similar_patterns(failure_data)
        if similar_patterns:
            causes.extend(similar_patterns)
            
        if not causes:
            causes.append({'cause': 'External Service Dependency', 'confidence': 0.6, 'evidence': 'No internal resource issues detected'})
            
        primary_cause = max(causes, key=lambda x: x['confidence']) if causes else {'cause': 'Unknown', 'confidence': 0.1}
        
        return {
            'primary_cause': primary_cause['cause'],
            'contributing_factors': [c for c in causes if c != primary_cause],
            'confidence': primary_cause['confidence'],
            'recommended_actions': self._get_recovery_actions(primary_cause['cause'])
        }
        
    def _find_similar_patterns(self, current_failure):
        """Find similar historical failure patterns"""
        # Simplified pattern matching
        patterns = []
        
        for pattern in self.failure_patterns:
            similarity = self._calculate_pattern_similarity(current_failure, pattern)
            if similarity > 0.7:
                patterns.append({
                    'cause': pattern.get('resolved_cause', 'Similar Historical Issue'),
                    'confidence': similarity * 0.8,
                    'evidence': f'Similar to failure on {pattern.get("date", "unknown date")}'
                })
                
        return patterns
        
    def _calculate_pattern_similarity(self, failure1, failure2):
        """Calculate similarity between two failure patterns"""
        # Simple similarity based on metrics ranges
        score = 0
        factors = 0
        
        for metric in ['cpu', 'memory', 'latency']:
            if metric in failure1 and metric in failure2:
                diff = abs(failure1[metric] - failure2[metric])
                max_val = max(failure1[metric], failure2[metric])
                if max_val > 0:
                    similarity = 1 - (diff / max_val)
                    score += similarity
                    factors += 1
                    
        return score / factors if factors > 0 else 0
        
    def _get_recovery_actions(self, cause):
        """Get recommended recovery actions based on root cause"""
        actions = {
            'Memory Exhaustion': [
                'Restart application services',
                'Clear application caches',
                'Scale up memory resources',
                'Check for memory leaks'
            ],
            'CPU Overload': [
                'Restart high-CPU processes',
                'Scale up CPU resources',
                'Optimize application performance',
                'Check for infinite loops'
            ],
            'Network Issues': [
                'Check network connectivity',
                'Restart network services',
                'Verify DNS resolution',
                'Check firewall rules'
            ],
            'External Service Dependency': [
                'Check external service status',
                'Implement circuit breaker',
                'Use cached responses',
                'Switch to backup services'
            ]
        }
        
        return actions.get(cause, ['Restart all services', 'Check system logs', 'Monitor closely'])
        
    def record_failure_pattern(self, failure_data, resolution):
        """Record a failure pattern for future analysis"""
        pattern = {
            'date': datetime.now().isoformat(),
            'failure_data': failure_data,
            'resolved_cause': resolution.get('cause'),
            'resolution_time': resolution.get('time_to_resolve'),
            'actions_taken': resolution.get('actions')
        }
        
        self.failure_patterns.append(pattern)
        
        # Keep only last 50 patterns
        if len(self.failure_patterns) > 50:
            self.failure_patterns.pop(0)
            
        logger.info(f"Recorded failure pattern: {resolution.get('cause')}")

# Global AI predictor instance
ai_predictor = AIPredictor()