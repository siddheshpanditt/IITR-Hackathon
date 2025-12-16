import logging
from datetime import datetime, timedelta
from collections import defaultdict, deque
import hashlib

logger = logging.getLogger(__name__)

class IntelligentAlerting:
    def __init__(self):
        self.alert_history = deque(maxlen=1000)
        self.alert_counts = defaultdict(int)
        self.suppressed_alerts = {}
        self.alert_patterns = defaultdict(list)
        
    def should_send_alert(self, alert_type, message, severity='medium'):
        """Determine if alert should be sent based on intelligent filtering"""
        
        # Create alert fingerprint
        alert_hash = self._create_alert_hash(alert_type, message)
        current_time = datetime.now()
        
        # Check if alert is currently suppressed
        if self._is_suppressed(alert_hash, current_time):
            logger.info(f"Alert suppressed: {alert_type}")
            return False
            
        # Check for duplicate alerts in recent history
        if self._is_duplicate_recent(alert_hash, current_time):
            self._update_suppression(alert_hash, current_time, severity)
            logger.info(f"Duplicate alert detected, applying suppression: {alert_type}")
            return False
            
        # Check for alert storms
        if self._is_alert_storm(alert_type, current_time):
            self._suppress_alert_type(alert_type, current_time)
            logger.warning(f"Alert storm detected for {alert_type}, suppressing for 30 minutes")
            return False
            
        # Record the alert
        self._record_alert(alert_hash, alert_type, message, severity, current_time)
        
        return True
        
    def _create_alert_hash(self, alert_type, message):
        """Create unique hash for alert deduplication"""
        content = f"{alert_type}:{message[:100]}"  # First 100 chars to handle minor variations
        return hashlib.md5(content.encode()).hexdigest()
        
    def _is_suppressed(self, alert_hash, current_time):
        """Check if alert is currently suppressed"""
        if alert_hash in self.suppressed_alerts:
            suppress_until = self.suppressed_alerts[alert_hash]
            if current_time < suppress_until:
                return True
            else:
                # Remove expired suppression
                del self.suppressed_alerts[alert_hash]
        return False
        
    def _is_duplicate_recent(self, alert_hash, current_time, window_minutes=15):
        """Check if same alert was sent recently"""
        cutoff_time = current_time - timedelta(minutes=window_minutes)
        
        for alert in reversed(self.alert_history):
            if alert['timestamp'] < cutoff_time:
                break
            if alert['hash'] == alert_hash:
                return True
        return False
        
    def _is_alert_storm(self, alert_type, current_time, threshold=5, window_minutes=10):
        """Detect if there's an alert storm for this type"""
        cutoff_time = current_time - timedelta(minutes=window_minutes)
        
        count = 0
        for alert in reversed(self.alert_history):
            if alert['timestamp'] < cutoff_time:
                break
            if alert['type'] == alert_type:
                count += 1
                
        return count >= threshold
        
    def _update_suppression(self, alert_hash, current_time, severity):
        """Update suppression time based on severity and frequency"""
        base_suppression = {
            'low': 30,      # 30 minutes
            'medium': 60,   # 1 hour  
            'high': 120,    # 2 hours
            'critical': 30  # 30 minutes (critical alerts should not be suppressed long)
        }
        
        suppression_minutes = base_suppression.get(severity, 60)
        
        # Increase suppression for repeated alerts
        if alert_hash in self.suppressed_alerts:
            suppression_minutes *= 2  # Double suppression time
            
        suppress_until = current_time + timedelta(minutes=suppression_minutes)
        self.suppressed_alerts[alert_hash] = suppress_until
        
    def _suppress_alert_type(self, alert_type, current_time):
        """Suppress all alerts of a specific type temporarily"""
        suppress_until = current_time + timedelta(minutes=30)
        
        # Mark all recent alerts of this type as suppressed
        for alert in self.alert_history:
            if alert['type'] == alert_type:
                self.suppressed_alerts[alert['hash']] = suppress_until
                
    def _record_alert(self, alert_hash, alert_type, message, severity, timestamp):
        """Record alert in history"""
        alert_record = {
            'hash': alert_hash,
            'type': alert_type,
            'message': message,
            'severity': severity,
            'timestamp': timestamp
        }
        
        self.alert_history.append(alert_record)
        self.alert_counts[alert_type] += 1
        
    def get_alert_summary(self):
        """Get summary of alert patterns and statistics"""
        current_time = datetime.now()
        last_24h = current_time - timedelta(hours=24)
        
        recent_alerts = [a for a in self.alert_history if a['timestamp'] > last_24h]
        
        summary = {
            'total_alerts_24h': len(recent_alerts),
            'suppressed_count': len(self.suppressed_alerts),
            'alert_types': defaultdict(int),
            'severity_breakdown': defaultdict(int),
            'top_alert_types': [],
            'suppression_status': []
        }
        
        for alert in recent_alerts:
            summary['alert_types'][alert['type']] += 1
            summary['severity_breakdown'][alert['severity']] += 1
            
        # Top alert types
        summary['top_alert_types'] = sorted(
            summary['alert_types'].items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        # Current suppressions
        for alert_hash, suppress_until in self.suppressed_alerts.items():
            if suppress_until > current_time:
                minutes_left = int((suppress_until - current_time).total_seconds() / 60)
                summary['suppression_status'].append({
                    'hash': alert_hash[:8],
                    'minutes_remaining': minutes_left
                })
                
        return summary
        
    def cleanup_old_data(self):
        """Clean up old suppression data"""
        current_time = datetime.now()
        
        # Remove expired suppressions
        expired_hashes = [
            h for h, until in self.suppressed_alerts.items() 
            if until < current_time
        ]
        
        for hash_key in expired_hashes:
            del self.suppressed_alerts[hash_key]
            
        logger.info(f"Cleaned up {len(expired_hashes)} expired alert suppressions")

# Global intelligent alerting instance
intelligent_alerting = IntelligentAlerting()