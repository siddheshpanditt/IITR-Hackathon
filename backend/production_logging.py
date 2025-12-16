import logging
import json
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
import hashlib
import threading
from collections import deque

class ProductionLogger:
    def __init__(self, log_dir='logs'):
        self.log_dir = log_dir
        self.ensure_log_directory()
        self.setup_loggers()
        self.audit_trail = deque(maxlen=10000)
        self.security_events = deque(maxlen=1000)
        self._lock = threading.Lock()
        
    def ensure_log_directory(self):
        """Ensure log directory exists"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            
    def setup_loggers(self):
        """Setup production-ready loggers"""
        
        # Main application logger
        self.app_logger = logging.getLogger('app')
        self.app_logger.setLevel(logging.INFO)
        
        app_handler = RotatingFileHandler(
            os.path.join(self.log_dir, 'app.log'),
            maxBytes=50*1024*1024,  # 50MB
            backupCount=10
        )
        app_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        app_handler.setFormatter(app_formatter)
        self.app_logger.addHandler(app_handler)
        
        # Security logger
        self.security_logger = logging.getLogger('security')
        self.security_logger.setLevel(logging.WARNING)
        
        security_handler = RotatingFileHandler(
            os.path.join(self.log_dir, 'security.log'),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=20
        )
        security_formatter = logging.Formatter(
            '%(asctime)s - SECURITY - %(levelname)s - %(message)s'
        )
        security_handler.setFormatter(security_formatter)
        self.security_logger.addHandler(security_handler)
        
        # Audit logger
        self.audit_logger = logging.getLogger('audit')
        self.audit_logger.setLevel(logging.INFO)
        
        audit_handler = RotatingFileHandler(
            os.path.join(self.log_dir, 'audit.log'),
            maxBytes=25*1024*1024,  # 25MB
            backupCount=15
        )
        audit_formatter = logging.Formatter(
            '%(asctime)s - AUDIT - %(message)s'
        )
        audit_handler.setFormatter(audit_formatter)
        self.audit_logger.addHandler(audit_handler)
        
        # Performance logger
        self.perf_logger = logging.getLogger('performance')
        self.perf_logger.setLevel(logging.INFO)
        
        perf_handler = RotatingFileHandler(
            os.path.join(self.log_dir, 'performance.log'),
            maxBytes=100*1024*1024,  # 100MB
            backupCount=5
        )
        perf_formatter = logging.Formatter(
            '%(asctime)s - PERF - %(message)s'
        )
        perf_handler.setFormatter(perf_formatter)
        self.perf_logger.addHandler(perf_handler)
        
    def log_app_event(self, level, message, context=None):
        """Log application events with context"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message,
            'context': context or {}
        }
        
        self.app_logger.log(getattr(logging, level.upper()), json.dumps(log_entry))
        
    def log_security_event(self, event_type, details, severity='medium'):
        """Log security events"""
        with self._lock:
            event = {
                'timestamp': datetime.now().isoformat(),
                'event_type': event_type,
                'severity': severity,
                'details': details,
                'event_id': self._generate_event_id(event_type, details)
            }
            
            self.security_events.append(event)
            self.security_logger.warning(json.dumps(event))
            
    def log_audit_trail(self, user, action, resource, result='success', details=None):
        """Log audit trail for compliance"""
        with self._lock:
            audit_entry = {
                'timestamp': datetime.now().isoformat(),
                'user': user,
                'action': action,
                'resource': resource,
                'result': result,
                'details': details or {},
                'session_id': self._get_session_id(),
                'audit_id': self._generate_audit_id(user, action, resource)
            }
            
            self.audit_trail.append(audit_entry)
            self.audit_logger.info(json.dumps(audit_entry))
            
    def log_performance_metric(self, metric_name, value, unit='ms', context=None):
        """Log performance metrics"""
        perf_entry = {
            'timestamp': datetime.now().isoformat(),
            'metric': metric_name,
            'value': value,
            'unit': unit,
            'context': context or {}
        }
        
        self.perf_logger.info(json.dumps(perf_entry))
        
    def log_system_health(self, metrics):
        """Log system health metrics"""
        health_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'system_health',
            'metrics': metrics
        }
        
        self.perf_logger.info(json.dumps(health_entry))
        
    def log_api_request(self, method, endpoint, user, response_time, status_code, ip_address=None):
        """Log API requests for monitoring"""
        api_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'api_request',
            'method': method,
            'endpoint': endpoint,
            'user': user,
            'response_time': response_time,
            'status_code': status_code,
            'ip_address': ip_address
        }
        
        # Log to audit for API access tracking
        self.audit_logger.info(json.dumps(api_entry))
        
        # Log to performance for response time tracking
        self.perf_logger.info(json.dumps(api_entry))
        
    def log_error_with_context(self, error, context=None, stack_trace=None):
        """Log errors with full context for debugging"""
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'error',
            'error': str(error),
            'context': context or {},
            'stack_trace': stack_trace,
            'error_id': self._generate_error_id(str(error))
        }
        
        self.app_logger.error(json.dumps(error_entry))
        
    def get_recent_security_events(self, limit=50):
        """Get recent security events"""
        with self._lock:
            return list(self.security_events)[-limit:]
            
    def get_audit_trail(self, user=None, limit=100):
        """Get audit trail, optionally filtered by user"""
        with self._lock:
            trail = list(self.audit_trail)
            
            if user:
                trail = [entry for entry in trail if entry.get('user') == user]
                
            return trail[-limit:]
            
    def search_logs(self, query, log_type='app', limit=100):
        """Search logs by query (simplified implementation)"""
        results = []
        log_file = os.path.join(self.log_dir, f'{log_type}.log')
        
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    
                for line in reversed(lines[-1000:]):  # Search last 1000 lines
                    if query.lower() in line.lower():
                        results.append(line.strip())
                        if len(results) >= limit:
                            break
                            
            except Exception as e:
                self.log_error_with_context(e, {'operation': 'log_search', 'query': query})
                
        return results
        
    def get_log_statistics(self):
        """Get logging statistics"""
        stats = {
            'audit_entries': len(self.audit_trail),
            'security_events': len(self.security_events),
            'log_files': {}
        }
        
        # Get log file sizes
        for log_type in ['app', 'security', 'audit', 'performance']:
            log_file = os.path.join(self.log_dir, f'{log_type}.log')
            if os.path.exists(log_file):
                stats['log_files'][log_type] = {
                    'size_mb': round(os.path.getsize(log_file) / (1024*1024), 2),
                    'modified': datetime.fromtimestamp(os.path.getmtime(log_file)).isoformat()
                }
                
        return stats
        
    def _generate_event_id(self, event_type, details):
        """Generate unique event ID"""
        content = f"{event_type}:{str(details)}:{datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:16]
        
    def _generate_audit_id(self, user, action, resource):
        """Generate unique audit ID"""
        content = f"{user}:{action}:{resource}:{datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:16]
        
    def _generate_error_id(self, error):
        """Generate unique error ID"""
        content = f"{error}:{datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:16]
        
    def _get_session_id(self):
        """Get current session ID (simplified)"""
        return f"session_{threading.current_thread().ident}"
        
    def cleanup_old_logs(self, days_to_keep=30):
        """Clean up old log files"""
        cutoff_time = datetime.now().timestamp() - (days_to_keep * 24 * 3600)
        
        for root, dirs, files in os.walk(self.log_dir):
            for file in files:
                if file.endswith('.log'):
                    file_path = os.path.join(root, file)
                    if os.path.getmtime(file_path) < cutoff_time:
                        try:
                            os.remove(file_path)
                            self.log_app_event('info', f'Cleaned up old log file: {file}')
                        except Exception as e:
                            self.log_error_with_context(e, {'operation': 'log_cleanup', 'file': file})

# Global production logger instance
production_logger = ProductionLogger()