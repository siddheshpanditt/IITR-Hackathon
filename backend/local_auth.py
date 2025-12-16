import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class LocalAuth:
    def __init__(self):
        self.users_file = 'users.json'
        self.users = self.load_users()
        
    def load_users(self):
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Create default admin user
        default_users = {
            'admin': {
                'username': 'admin',
                'password_hash': generate_password_hash('admin123'),
                'email': 'admin@monitor.com',
                'created_at': datetime.now().isoformat(),
                'last_login': None
            }
        }
        self.save_users(default_users)
        return default_users
    
    def save_users(self, users=None):
        if users is None:
            users = self.users
        try:
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=2)
        except Exception as e:
            print(f"Failed to save users: {e}")
    
    def create_user(self, username, password, email=''):
        if username in self.users:
            return False, "Username already exists"
        
        self.users[username] = {
            'username': username,
            'password_hash': generate_password_hash(password),
            'email': email,
            'created_at': datetime.now().isoformat(),
            'last_login': None
        }
        self.save_users()
        return True, "User created successfully"
    
    def verify_user(self, username, password):
        if username not in self.users:
            return False, "Invalid credentials"
        
        user = self.users[username]
        if check_password_hash(user['password_hash'], password):
            # Update last login
            self.users[username]['last_login'] = datetime.now().isoformat()
            self.save_users()
            return True, user
        
        return False, "Invalid credentials"
    
    def get_user(self, username):
        return self.users.get(username)

# Global instance
local_auth = LocalAuth()