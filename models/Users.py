from initiate_packages import db 
import random
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True , default=random.randint(1000000, 9999999))
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique = True , nullable=False)
    phone = db.Column(db.String(120))
    amount = db.Column(db.Integer , default = 0)
    def __repr__(self):
        return f"<User {self.name}>"
    
 