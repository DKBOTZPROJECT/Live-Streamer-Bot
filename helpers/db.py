import datetime
from dkbotzdb import DkBotzDB
from pymongo import MongoClient
import ssl
import certifi
from Config import *

class Database:
    def __init__(self, token):
        self.cache = {}

        if DB_TYPE == 'dkbotz':
            self.db = DkBotzDB()[token]
        else:
            mongo_client = MongoClient(token, tlsCAFile=certifi.where())
            self.db = mongo_client["DKBOTZYTBOT"]

        self.col = self.db.dkusers

    def new_user(self, id):
        return dict(
            id=id,
            join_date=datetime.date.today().isoformat(),
            last_used_on=datetime.date.today().isoformat(),
            paid_status={
                'is_paid': False,
                'paid_duration': 0,
                'paid_on': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'paid_username': '',
                'paid_reason': ''
            },
            ban_status={
                'is_banned': False,
                'ban_duration': 0,
                'banned_on': datetime.date.max.isoformat(),
                'ban_reason': ''
            }
        )

    def get_user(self, id):
        id = int(id)
        if id in self.cache:
            return self.cache[id]
        user = self.col.find_one({"id": id})
        if user:
            self.cache[id] = user
        return user

    def add_user(self, id):
        if not self.get_user(id):
            user = self.new_user(id)
            self.col.insert_one(user)
            self.cache[int(id)] = user

    def is_user_exist(self, id):
        return bool(self.get_user(id))

    def get_all_users(self):
        return list(self.col.find({}))

    def total_users_count(self):
        return self.col.count_documents({})

    def delete_user(self, user_id):
        user_id = int(user_id)
        self.cache.pop(user_id, None)
        self.col.delete_many({"id": user_id})

    def update_last_used_on(self, id):
        today = datetime.date.today().isoformat()
        if id in self.cache:
            self.cache[id]["last_used_on"] = today
        self.col.update_one({"id": int(id)}, {"$set": {"last_used_on": today}})

    def get_last_used_on(self, id):
        user = self.get_user(id)
        return user.get("last_used_on", datetime.date.today().isoformat())

    # 💰 Paid status
    def paid_user(self, user_id, paid_username, paid_duration, paid_reason):
        self.get_user(user_id)
        paid_status = {
            'is_paid': True,
            'paid_duration': paid_duration,
            'paid_on': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'paid_username': paid_username,
            'paid_reason': paid_reason
        }
        self.cache[int(user_id)]["paid_status"] = paid_status
        self.col.update_one({"id": int(user_id)}, {"$set": {"paid_status": paid_status}})

    def remove_paid(self, id):
        self.get_user(id)
        paid_status = {
            'is_paid': False,
            'paid_duration': 0,
            'paid_on': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'paid_username': '',
            'paid_reason': ''
        }
        self.cache[int(id)]["paid_status"] = paid_status
        self.col.update_one({"id": int(id)}, {"$set": {"paid_status": paid_status}})

    def get_paid_status(self, id):
        user = self.get_user(id)
        return user.get("paid_status", {
            'is_paid': False,
            'paid_duration': 0,
            'paid_on': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'paid_username': '',
            'paid_reason': ''
        })

    def get_all_paid_users(self):
        return list(self.col.find({"paid_status.is_paid": True}))

    # 🚫 Ban Status
    def ban_user(self, user_id, ban_duration, ban_reason):
        self.get_user(user_id)
        ban_status = {
            'is_banned': True,
            'ban_duration': ban_duration,
            'banned_on': datetime.date.today().isoformat(),
            'ban_reason': ban_reason
        }
        self.cache[int(user_id)]["ban_status"] = ban_status
        self.col.update_one({"id": int(user_id)}, {"$set": {"ban_status": ban_status}})

    def remove_ban(self, id):
        self.get_user(id)
        ban_status = {
            'is_banned': False,
            'ban_duration': 0,
            'banned_on': datetime.date.max.isoformat(),
            'ban_reason': ''
        }
        self.cache[int(id)]["ban_status"] = ban_status
        self.col.update_one({"id": int(id)}, {"$set": {"ban_status": ban_status}})

    def get_ban_status(self, id):
        user = self.get_user(id)
        return user.get("ban_status", {
            'is_banned': False,
            'ban_duration': 0,
            'banned_on': datetime.date.max.isoformat(),
            'ban_reason': ''
        })

    def get_all_banned_users(self):
        return list(self.col.find({"ban_status.is_banned": True}))


db = Database(DB_TOKEN)
