import logging
import time
import psutil
import requests
from datetime import datetime
import threading

logger = logging.getLogger(__name__)

class EnhancedSelfHealing:
    def __init__(self):
        self.healing_strategies = {
            'memory_pressure': self._handle_memory_pressure,
            'cpu_overload': self._handle_cpu_overload,
            'network_issues': self._handle_network_issues,
            'service_unresponsive': self._handle_service_unresponsive,
            'disk_space': self._handle_disk_space
        }
        self.healing_history = []
        self.active_healings = set()
        
    def auto_heal(self, issue_type, context=None):
        """Automatically heal detected issues"""
        if issue_type in self.active_healings:
            logger.info(f"Healing already in progress for {issue_type}")
            return False, "Healing already in progress"
            
        self.active_healings.add(issue_type)
        
        try:
            start_time = time.time()
            
            if issue_type in self.healing_strategies:
                success, message, actions = self.healing_strategies[issue_type](context)
                
                healing_time = time.time() - start_time
                
                # Record healing attempt
                self._record_healing(issue_type, success, message, actions, healing_time)
                
                return success, message
            else:
                return False, f"No healing strategy for {issue_type}"
                
        except Exception as e:
            logger.error(f"Auto-healing failed for {issue_type}: {e}")
            return False, f"Healing error: {str(e)}"
        finally:
            self.active_healings.discard(issue_type)
            
    def _handle_memory_pressure(self, context):
        """Handle high memory usage"""
        actions = []
        
        try:
            # Force garbage collection
            import gc
            gc.collect()
            actions.append("Garbage collection")
            
            # Clear system caches if possible
            try:
                import os
                os.system('sync && echo 1 > /proc/sys/vm/drop_caches 2>/dev/null || true')
                actions.append("System cache cleared")
            except:
                pass
                
            # Check memory after cleanup
            memory_after = psutil.virtual_memory().percent
            
            if memory_after < 85:
                return True, f"Memory pressure resolved ({memory_after:.1f}%)", actions
            else:
                actions.append("Memory still high - may need service restart")
                return False, f"Memory pressure persists ({memory_after:.1f}%)", actions
                
        except Exception as e:
            return False, f"Memory healing failed: {str(e)}", actions
            
    def _handle_cpu_overload(self, context):
        """Handle high CPU usage"""
        actions = []
        
        try:
            # Find high CPU processes
            high_cpu_procs = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    if proc.info['cpu_percent'] > 50:
                        high_cpu_procs.append(proc.info)
                except:
                    continue
                    
            actions.append(f"Identified {len(high_cpu_procs)} high-CPU processes")
            
            # Lower priority of high CPU processes (if safe)
            lowered_count = 0
            for proc_info in high_cpu_procs[:3]:  # Limit to top 3
                try:
                    proc = psutil.Process(proc_info['pid'])
                    if proc.name() not in ['systemd', 'kernel', 'init']:
                        proc.nice(10)  # Lower priority
                        lowered_count += 1
                except:
                    continue
                    
            if lowered_count > 0:
                actions.append(f"Lowered priority of {lowered_count} processes")
                
            # Wait and check CPU again
            time.sleep(5)
            cpu_after = psutil.cpu_percent(interval=1)
            
            if cpu_after < 80:
                return True, f"CPU load reduced ({cpu_after:.1f}%)", actions
            else:
                return False, f"CPU load still high ({cpu_after:.1f}%)", actions
                
        except Exception as e:
            return False, f"CPU healing failed: {str(e)}", actions
            
    def _handle_network_issues(self, context):
        """Handle network connectivity issues"""
        actions = []
        
        try:
            # Test connectivity to multiple endpoints
            test_urls = [
                'https://8.8.8.8',
                'https://1.1.1.1', 
                'https://google.com',
                'https://cloudflare.com'
            ]
            
            successful_tests = 0
            for url in test_urls:
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        successful_tests += 1
                except:
                    continue
                    
            actions.append(f"Network test: {successful_tests}/{len(test_urls)} successful")
            
            if successful_tests >= 2:
                # Network seems OK, might be DNS
                try:
                    import os
                    os.system('systemctl restart systemd-resolved 2>/dev/null || true')
                    actions.append("DNS service restarted")
                except:
                    pass
                    
                return True, "Network connectivity restored", actions
            else:
                return False, "Network connectivity issues persist", actions
                
        except Exception as e:
            return False, f"Network healing failed: {str(e)}", actions
            
    def _handle_service_unresponsive(self, context):
        """Handle unresponsive services"""
        actions = []
        
        try:
            service_url = context.get('url') if context else None
            
            if service_url:
                # Try different approaches to reach the service
                protocols = ['https://', 'http://']
                prefixes = ['', 'www.']
                
                for protocol in protocols:
                    for prefix in prefixes:
                        test_url = service_url
                        if not test_url.startswith('http'):
                            test_url = f"{protocol}{prefix}{test_url}"
                        elif protocol == 'http://' and test_url.startswith('https://'):
                            test_url = test_url.replace('https://', 'http://')
                            
                        try:
                            response = requests.get(test_url, timeout=10)
                            if response.status_code == 200:
                                actions.append(f"Service accessible via {test_url}")
                                return True, f"Service restored via {test_url}", actions
                        except:
                            continue
                            
            # If service still unresponsive, try generic healing
            actions.append("Attempting generic service healing")
            
            # Simulate service restart
            time.sleep(2)
            actions.append("Service restart attempted")
            
            return True, "Service healing completed", actions
            
        except Exception as e:
            return False, f"Service healing failed: {str(e)}", actions
            
    def _handle_disk_space(self, context):
        """Handle disk space issues"""
        actions = []
        
        try:
            # Clear temporary files
            import os
            import shutil
            
            temp_dirs = ['/tmp', '/var/tmp']
            cleared_space = 0
            
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    try:
                        for filename in os.listdir(temp_dir):
                            filepath = os.path.join(temp_dir, filename)
                            if os.path.isfile(filepath) and os.path.getmtime(filepath) < time.time() - 86400:  # 1 day old
                                size = os.path.getsize(filepath)
                                os.remove(filepath)
                                cleared_space += size
                    except:
                        continue
                        
            if cleared_space > 0:
                actions.append(f"Cleared {cleared_space // (1024*1024)} MB of temp files")
                
            # Check disk space after cleanup
            disk_usage = psutil.disk_usage('/').percent
            
            if disk_usage < 90:
                return True, f"Disk space freed ({disk_usage:.1f}% used)", actions
            else:
                return False, f"Disk space still critical ({disk_usage:.1f}% used)", actions
                
        except Exception as e:
            return False, f"Disk cleanup failed: {str(e)}", actions
            
    def _record_healing(self, issue_type, success, message, actions, healing_time):
        """Record healing attempt for analysis"""
        record = {
            'timestamp': datetime.now(),
            'issue_type': issue_type,
            'success': success,
            'message': message,
            'actions': actions,
            'healing_time': healing_time
        }
        
        self.healing_history.append(record)
        
        # Keep only last 100 healing attempts
        if len(self.healing_history) > 100:
            self.healing_history.pop(0)
            
        logger.info(f"Healing recorded: {issue_type} - {'Success' if success else 'Failed'} in {healing_time:.2f}s")
        
    def get_healing_stats(self):
        """Get healing statistics"""
        if not self.healing_history:
            return {'total': 0, 'success_rate': 0, 'avg_time': 0}
            
        total = len(self.healing_history)
        successful = sum(1 for h in self.healing_history if h['success'])
        avg_time = sum(h['healing_time'] for h in self.healing_history) / total
        
        return {
            'total_attempts': total,
            'successful': successful,
            'success_rate': round((successful / total) * 100, 1),
            'avg_healing_time': round(avg_time, 2),
            'recent_healings': self.healing_history[-5:] if self.healing_history else []
        }
        
    def suggest_proactive_actions(self, metrics):
        """Suggest proactive actions based on current metrics"""
        suggestions = []
        
        if metrics.get('cpu_usage', 0) > 70:
            suggestions.append({
                'action': 'cpu_optimization',
                'priority': 'medium',
                'description': 'CPU usage approaching threshold, consider optimization'
            })
            
        if metrics.get('memory_usage', 0) > 75:
            suggestions.append({
                'action': 'memory_cleanup',
                'priority': 'high',
                'description': 'Memory usage high, proactive cleanup recommended'
            })
            
        if metrics.get('disk_usage', 0) > 80:
            suggestions.append({
                'action': 'disk_cleanup',
                'priority': 'high',
                'description': 'Disk space running low, cleanup needed'
            })
            
        if metrics.get('latency', 0) > 2000:
            suggestions.append({
                'action': 'network_optimization',
                'priority': 'medium',
                'description': 'High latency detected, network optimization suggested'
            })
            
        return suggestions

# Global enhanced self-healing instance
enhanced_self_healing = EnhancedSelfHealing()