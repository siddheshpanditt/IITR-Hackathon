import os
import logging
import certifi
from pymongo import MongoClient
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash

logger = logging.getLogger(__name__)

class MongoDBClient:
    def __init__(self):
        self.connection_string = os.environ.get('MONGODB_URI')
        self.database_name = os.environ.get('MONGODB_DATABASE', 'deployment_monitor')
        self.client = None
        self.db = None
        self._connected = False

    def connect(self):
        if self._connected or not self.connection_string:
            return
            
        try:
            # Use SSL certificates for Atlas connections
            if 'mongodb+srv://' in self.connection_string:
                self.client = MongoClient(self.connection_string, tlsCAFile=certifi.where())
            else:
                self.client = MongoClient(self.connection_string)
            
            self.db = self.client[self.database_name]
            # Test connection
            self.client.admin.command('ping')
            logger.info(f"Connected to MongoDB: {self.database_name}")
            self.init_collections()
            self._connected = True
        except Exception as e:
            logger.error(f"MongoDB connection failed: {e}")
            raise
    
    def ensure_connected(self):
        if not self._connected:
            if not self.connection_string:
                raise Exception("MONGODB_URI environment variable not set")
            self.connect()

    def init_collections(self):
        # Create collections and indexes
        collections = ['users', 'daily_reports', 'weekly_reports', 'actions', 'alerts', 'transactions', 'balance_history']
        
        for collection in collections:
            if collection not in self.db.list_collection_names():
                self.db.create_collection(collection)
        
        # Create indexes
        self.db.users.create_index("username", unique=True)
        self.db.daily_reports.create_index("date", unique=True)
        self.db.transactions.create_index("created_at")
        self.db.balance_history.create_index("checked_at")
        
        # Create default admin user
        admin_exists = self.db.users.find_one({"username": "admin"})
        if not admin_exists:
            admin_hash = generate_password_hash('admin123')
            result = self.db.users.insert_one({
                "username": "admin",
                "password_hash": admin_hash,
                "email": "admin@monitor.com",
                "created_at": datetime.now(),
                "last_login": None
            })
            if result.inserted_id:
                logger.info("Default admin user created successfully")
            else:
                logger.error("Failed to create default admin user")

    def get_user(self, username):
        self.ensure_connected()
        return self.db.users.find_one({"username": username})

    def insert_daily_report(self, date, uptime_percentage, avg_latency, incidents, report_data):
        self.ensure_connected()
        return self.db.daily_reports.replace_one(
            {"date": date},
            {
                "date": date,
                "uptime_percentage": uptime_percentage,
                "avg_latency": avg_latency,
                "incidents": incidents,
                "report_data": report_data,
                "created_at": datetime.utcnow()
            },
            upsert=True
        )

    def insert_weekly_report(self, week_start, week_end, report_data):
        self.ensure_connected()
        return self.db.weekly_reports.insert_one({
            "week_start": week_start,
            "week_end": week_end,
            "report_data": report_data,
            "created_at": datetime.utcnow()
        })

    def insert_action(self, action_type, status, message):
        self.ensure_connected()
        return self.db.actions.insert_one({
            "action_type": action_type,
            "status": status,
            "message": message,
            "created_at": datetime.utcnow()
        })

    def insert_transaction(self, transaction_type, amount, balance_after, description, transaction_id=None):
        self.ensure_connected()
        return self.db.transactions.insert_one({
            "transaction_type": transaction_type,
            "amount": amount,
            "balance_after": balance_after,
            "description": description,
            "transaction_id": transaction_id,
            "created_at": datetime.utcnow()
        })

    def insert_balance_history(self, balance):
        self.ensure_connected()
        return self.db.balance_history.insert_one({
            "balance": balance,
            "checked_at": datetime.utcnow()
        })

    def get_daily_reports(self, limit=30):
        self.ensure_connected()
        return list(self.db.daily_reports.find().sort("date", -1).limit(limit))

    def get_weekly_reports(self, limit=10):
        self.ensure_connected()
        return list(self.db.weekly_reports.find().sort("week_start", -1).limit(limit))

    def get_daily_report_by_id(self, report_id):
        self.ensure_connected()
        from bson import ObjectId
        return self.db.daily_reports.find_one({"_id": ObjectId(report_id)})

    def get_transactions(self, days=30):
        self.ensure_connected()
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return list(self.db.transactions.find(
            {"created_at": {"$gte": cutoff_date}}
        ).sort("created_at", -1))

    def get_balance_history(self, days=7):
        self.ensure_connected()
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return list(self.db.balance_history.find(
            {"checked_at": {"$gte": cutoff_date}}
        ).sort("checked_at", 1))

# Global instance
mongodb_client = MongoDBClient()