from initiate_packages import db 
import random
from datetime import datetime
class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True , default=random.randint(1000000, 9999999))
    from_user = db.Column(db.String(80), nullable=False)
    to_user = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Integer , default = 0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"<Transaction {self.id}>"
    
 