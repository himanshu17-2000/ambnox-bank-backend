from flask import Blueprint
from flask import request
from initiate_packages import db
from models.Users import Users
from models.Transactions import Transactions
import json 
import random

api = Blueprint(name='api' ,import_name='api')

@api.route('/')
def home_func():
    return "Himanshu's home page" 

@api.route('/get_users' , methods=['GET'])
def get_users():
    try:
        data = Users.query.all() 
        def get_dict(item):
            return {
                'account':item.id,
                'name':item.name,
                'email':item.email,
                'phone':item.phone,
                'amount':item.amount,
            }
        return json.dumps(list(map(get_dict,data)))
    except Exception as err:
            return json.dumps( { "message" :f"error occur {err}"}) , 400 

@api.route('/get_transactions' ,methods=['GET'])
def get_transaction():
    try:
        data = Transactions.query.all() 
        print(type(data[0].timestamp))
        def get_dict(item):
            return {
                "from" : item.from_user,
                "to" : item.to_user,
                "amount":item.amount,
                "time" :str(item.timestamp)
            }
        return json.dumps(list(map(get_dict,data)))
    except Exception as err:
            return json.dumps( { "message" :f"error occur {err}"}) , 400 

@api.route('/register' , methods =['POST'])  
def register_user():
    try:
       data = request.json
       existing_user =  Users.query.filter(Users.email == data['email']).first()
       if(existing_user != None):
            return json.dumps({'message':"email already exists"}) ,400 
       new_user = Users(id =random.randint(10000000 ,99999999), name = data['name'], email= data['email'],phone= data['phone'],amount= data['amount'])
       db.session.add(new_user)
       db.session.commit()
       return json.dumps({"message" : "user registered" , 'id':new_user.id}),200 
    except Exception as err:
            return json.dumps( { "message" :f"error occur {err}"}) , 400 


@api.route('/transfer' , methods = ['POST'])
def transfer():
    try:
      data = request.json 
      from_user = Users.query.filter(Users.id == data['from_account']).first()
      old_from_amt = from_user.amount 
      from_user.amount = old_from_amt - data['amount']
      to_user = Users.query.filter(Users.id == data['to_account']).first()
      old_to_amt = to_user.amount 
      to_user.amount = old_to_amt + data['amount']
      new_transaction = Transactions(from_user = from_user.name , to_user = to_user.name , amount = data['amount'] )
      db.session.add(new_transaction)
      db.session.commit()
      return json.dumps({"message":"transaction saved sucessfully"}),200
    except Exception as err:
                return json.dumps( { "message" :f"error occur {err}"}) , 400 
      

@api.route("/user/<int:id>" , methods =['GET'])
def get_customer_by_id(id):
        try:
            data = Users.query.get(id)
            print(data)
            return json.dumps( {
                        'account':data.id,
                        'name':data.name,
                        'email':data.email,
                        'phone':data.phone,
                        'amount':data.amount,
                    })
        except Exception as err:
            return json.dumps( { "message" :f"error occur {err}"}) , 400 

@api.route("/withdraw_deposite" , methods =['POST'])
def withdraw_deposite():
    try:
        data = request.json 
        user = Users.query.get(data['id'])
        if(data['method'] == 'deposite'):
                user.amount = user.amount + data['amount'] 
        elif(data['method'] == 'withdraw'):
                user.amount = user.amount - data['amount'] 
        db.session.commit()
        return json.dumps( {
                    "name" : user.name ,
                    "method" : data['method'] ,
                    "amount" : data["amount"]
                }) , 200 
    except Exception as err:
            return json.dumps( { "message" :f"error occur {err}"}) , 400 