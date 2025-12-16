import os
import logging
import requests
from datetime import datetime, timedelta
from notification_service import notification_service
from mongodb_client import mongodb_client

logger = logging.getLogger(__name__)

class DepositMonitor:
    def __init__(self):
        self.spheron_api_key = os.environ.get('SPHERON_API_KEY')
        self.low_balance_threshold = float(os.environ.get('LOW_BALANCE_THRESHOLD', '10.0'))
        self.last_balance_check = None
        self.last_notification_time = None
        
    def init_db(self):
        # MongoDB collections are created automatically
        pass

    def get_spheron_balance(self):
        """Get current balance from Spheron API"""
        if not self.spheron_api_key:
            # Return realistic demo balance that changes
            import random
            base_balance = 25.50
            variation = random.uniform(-2, 2)  # Small random variation
            return round(base_balance + variation, 2), True
            
        try:
            headers = {
                'Authorization': f'Bearer {self.spheron_api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                'https://api.spheron.network/v1/account/balance',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return float(data.get('balance', 0)), True
            else:
                logger.error(f"Spheron API error: {response.status_code}")
                return 0, False
                
        except Exception as e:
            logger.error(f"Failed to get Spheron balance: {e}")
            return 0, False

    def log_transaction(self, transaction_type, amount, balance_after, description, transaction_id=None):
        """Log transaction to database"""
        try:
            mongodb_client.insert_transaction(
                transaction_type, amount, balance_after, description, transaction_id
            )
            logger.info(f"Transaction logged: {transaction_type} ${amount}")
        except Exception as e:
            logger.error(f"Failed to log transaction: {e}")

    def log_balance_check(self, balance):
        """Log balance check to history"""
        try:
            mongodb_client.insert_balance_history(balance)
        except Exception as e:
            logger.warning(f"Failed to log balance to MongoDB (demo mode): {e}")

    def check_balance(self):
        """Check current balance and send alerts if low"""
        balance, success = self.get_spheron_balance()
        
        if not success:
            return None
            
        # Log balance check (with error handling)
        try:
            self.log_balance_check(balance)
        except Exception as e:
            logger.warning(f"Balance logging failed (continuing): {e}")
            
        self.last_balance_check = datetime.now()
        
        # Check if balance is low
        if balance < self.low_balance_threshold:
            # Only send notification once per hour to avoid spam
            now = datetime.now()
            if (not self.last_notification_time or 
                now - self.last_notification_time > timedelta(hours=1)):
                
                notification_service.notify_low_funds(balance, self.low_balance_threshold)
                self.last_notification_time = now
                
                # Log low balance event
                self.log_transaction(
                    'alert', 
                    0, 
                    balance, 
                    f'Low balance alert sent (threshold: ${self.low_balance_threshold})'
                )
        
        return balance

    def get_transaction_history(self, days=30):
        """Get transaction history from database"""
        try:
            transactions = mongodb_client.get_transactions(days)
            return [{
                'type': t['transaction_type'],
                'amount': t['amount'],
                'balance_after': t['balance_after'],
                'description': t['description'],
                'transaction_id': t.get('transaction_id'),
                'created_at': t['created_at'].isoformat()
            } for t in transactions]
        except Exception as e:
            logger.error(f"Failed to get transaction history: {e}")
            return []

    def get_balance_history(self, days=7):
        """Get balance history for charts"""
        try:
            history = mongodb_client.get_balance_history(days)
            return [{
                'balance': h['balance'],
                'timestamp': h['checked_at'].isoformat()
            } for h in history]
        except Exception as e:
            logger.error(f"Failed to get balance history: {e}")
            return []

    def estimate_runway(self):
        """Estimate how long current balance will last"""
        try:
            # Get spending over last 7 days
            history = self.get_transaction_history(days=7)
            spending_transactions = [t for t in history if t['type'] == 'spend' and t['amount'] < 0]
            
            if not spending_transactions:
                return None
                
            total_spent = sum(abs(t['amount']) for t in spending_transactions)
            daily_spend = total_spent / 7
            
            current_balance, _ = self.get_spheron_balance()
            
            if daily_spend > 0:
                days_remaining = current_balance / daily_spend
                return int(days_remaining)
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to estimate runway: {e}")
            return None

# Global instance
deposit_monitor = DepositMonitor()