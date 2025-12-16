import requests
import ssl
import socket
import logging
from datetime import datetime
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class AdvancedMonitor:
    def __init__(self):
        pass
    
    def get_comprehensive_status(self, url):
        """Get comprehensive monitoring status"""
        try:
            parsed_url = urlparse(url)
            hostname = parsed_url.hostname or url
            
            status = {
                'url': url,
                'hostname': hostname,
                'ssl_info': self.check_ssl_certificate(hostname),
                'dns_resolution': self.check_dns_resolution(hostname),
                'port_status': self.check_port_status(hostname, 443 if parsed_url.scheme == 'https' else 80),
                'response_headers': self.get_response_headers(url),
                'timestamp': datetime.now().isoformat()
            }
            
            return status
            
        except Exception as e:
            logger.error(f"Advanced monitoring failed: {e}")
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    def check_ssl_certificate(self, hostname):
        """Check SSL certificate status"""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    return {
                        'valid': True,
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'subject': dict(x[0] for x in cert['subject']),
                        'expires': cert['notAfter'],
                        'version': cert['version']
                    }
        except Exception as e:
            return {'valid': False, 'error': str(e)}
    
    def check_dns_resolution(self, hostname):
        """Check DNS resolution"""
        try:
            import socket
            ip = socket.gethostbyname(hostname)
            return {'resolved': True, 'ip': ip}
        except Exception as e:
            return {'resolved': False, 'error': str(e)}
    
    def check_port_status(self, hostname, port):
        """Check if port is open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((hostname, port))
            sock.close()
            return {'open': result == 0, 'port': port}
        except Exception as e:
            return {'open': False, 'port': port, 'error': str(e)}
    
    def get_response_headers(self, url):
        """Get HTTP response headers"""
        try:
            response = requests.head(url, timeout=10, allow_redirects=True)
            return {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'final_url': response.url
            }
        except Exception as e:
            return {'error': str(e)}

# Global instance
advanced_monitor = AdvancedMonitor()