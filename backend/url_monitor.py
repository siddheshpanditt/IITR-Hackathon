import requests
import time
import logging
import json
import os
from datetime import datetime
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class URLMonitor:
    def __init__(self):
        self.urls_file = 'monitored_urls.json'
        self.monitored_urls = self.load_urls()
        
    def load_urls(self):
        """Load URLs from local file"""
        if os.path.exists(self.urls_file):
            try:
                with open(self.urls_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def save_urls(self):
        """Save URLs to local file"""
        try:
            with open(self.urls_file, 'w') as f:
                json.dump(self.monitored_urls, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save URLs: {e}")
        
    def add_url(self, url, user_id="default"):
        """Add URL to monitoring list"""
        try:
            # Validate URL
            parsed = urlparse(url)
            if not parsed.scheme:
                url = "https://" + url
            
            # Test URL first
            start_time = time.time()
            response = requests.get(url, timeout=10)
            response_time = (time.time() - start_time) * 1000
            
            url_data = {
                'url': url,
                'user_id': user_id,
                'status': 'active',
                'last_check': datetime.now().isoformat(),
                'response_time': round(response_time, 2),
                'status_code': response.status_code,
                'is_online': response.status_code == 200,
                'added_at': datetime.now().isoformat()
            }
            
            # Save to local storage
            self.monitored_urls[url] = url_data
            self.save_urls()
            
            return {'success': True, 'message': f'URL {url} added successfully'}
            
        except Exception as e:
            return {'success': False, 'message': f'Failed to add URL: {str(e)}'}
    
    def check_url(self, url):
        """Check single URL status"""
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10, allow_redirects=True)
            response_time = (time.time() - start_time) * 1000
            
            return {
                'url': url,
                'status_code': response.status_code,
                'response_time': round(response_time, 2),
                'is_online': response.status_code == 200,
                'headers': dict(response.headers),
                'final_url': response.url,
                'checked_at': datetime.now().isoformat()
            }
            
        except requests.exceptions.Timeout:
            return {
                'url': url,
                'status_code': 0,
                'response_time': 10000,
                'is_online': False,
                'error': 'Timeout',
                'checked_at': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'url': url,
                'status_code': 0,
                'response_time': 0,
                'is_online': False,
                'error': str(e),
                'checked_at': datetime.now().isoformat()
            }
    
    def get_monitored_urls(self, user_id="default"):
        """Get all monitored URLs for user"""
        try:
            return list(self.monitored_urls.values())
        except Exception as e:
            logger.error(f"Failed to get monitored URLs: {e}")
            return []
    
    def remove_url(self, url, user_id="default"):
        """Remove URL from monitoring"""
        try:
            if url in self.monitored_urls:
                del self.monitored_urls[url]
                self.save_urls()
                return {'success': True, 'message': 'URL removed successfully'}
            else:
                return {'success': False, 'message': 'URL not found'}
                
        except Exception as e:
            return {'success': False, 'message': f'Failed to remove URL: {str(e)}'}
    
    def check_all_urls(self, user_id="default"):
        """Check all monitored URLs"""
        urls = self.get_monitored_urls(user_id)
        results = []
        
        for url_data in urls:
            result = self.check_url(url_data['url'])
            
            # Update local storage
            try:
                if url_data['url'] in self.monitored_urls:
                    self.monitored_urls[url_data['url']].update({
                        'last_check': datetime.now().isoformat(),
                        'response_time': result['response_time'],
                        'status_code': result['status_code'],
                        'is_online': result['is_online']
                    })
                    self.save_urls()
            except Exception as e:
                logger.error(f"Failed to update URL status: {e}")
            
            results.append(result)
        
        return results

# Global instance
url_monitor = URLMonitor()