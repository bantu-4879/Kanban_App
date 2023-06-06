from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

from flask_restful import Resource, Api, reqparse
from werkzeug.exceptions import HTTPException
from flask import make_response





# Database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./database.sqlite3"



db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

# Api
api = Api(app)




# For List PUT Method
update_list_parser = reqparse.RequestParser()
update_list_parser.add_argument('list_tag')
update_list_parser.add_argument('list_name')

# For List POST Method
create_list_parser = reqparse.RequestParser()
create_list_parser.add_argument('list_tag')
create_list_parser.add_argument('list_name')

# For Card PUT Method
update_card_parser = reqparse.RequestParser()
update_card_parser.add_argument('card_title')
update_card_parser.add_argument('card_content')
update_card_parser.add_argument('card_deadline')
update_card_parser.add_argument('card_status')
update_card_parser.add_argument('list_id')

# For List Post method 
create_card_parser = reqparse.RequestParser()
create_card_parser.add_argument('card_title')
create_card_parser.add_argument('card_content')
create_card_parser.add_argument('card_deadline')
create_card_parser.add_argument('card_status')
create_card_parser.add_argument('list_id')




class Login(db.Model):
  __tablename__ = 'login'
  username = db.Column(db.String, primary_key = True, nullable = False)
  role = db.Column(db.String, nullable = False)




class List(db.Model):
  __tablename__= 'list'
  list_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  list_tag = db.Column(db.String, unique = True, nullable = False)
  list_name = db.Column(db.String, nullable = False)
  
 
class Card(db.Model):
  __tablename__= 'card'
  card_id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True)
  card_title = db.Column(db.String, unique = True, nullable = False)
  card_content = db.Column(db.String, nullable = False)
  card_deadline = db.Column(db.Integer, nullable = False)
  card_status = db.Column(db.String, nullable = False)
  list_id = db.Column(db.Integer, db.ForeignKey("list.list_id"), nullable = False)
  

  

# App

@app.route('/', methods = ["GET", "POST"])
def login():
  if request.method == "GET":
       return render_template("temp_login.html")

    
  if request.method == "POST":
      username = request.form["username"]
      role = request.form["role"]
      

      stmt = Login(username = username, role = role)
      db.session.add(stmt)
      db.session.commit()

      list_division = List.query.all()
      return render_template("temp_1.html", list_division = list_division)



  
@app.route('/list', methods = ["GET", "POST"])
def list():
  list_division = List.query.all()
  return render_template("temp_1.html", list_division = list_division)


@app.route('/list/add', methods = ["GET", "POST"])
def AddList():
    if request.method == "GET":
       return render_template("temp_2.html")

    
    if request.method == "POST":
      tag = request.form["list_tag"]
      name = request.form["list_name"]
      

      stmt = List(list_tag = tag, list_name = name)
      db.session.add(stmt)
      db.session.commit()

      list_division = List.query.all()
      return render_template("temp_1.html", list_division = list_division)



@app.route('/list/<list_id>/update', methods = ["GET", "POST"])
def UpdateList(list_id):
  if request.method == "GET":
    stmt = List.query.all()
    for i in stmt:
      
      if(i.list_id == int(list_id)):
        list_id = i.list_id
        list_tag = i.list_tag
        list_name = i.list_name
        
    return render_template("temp_3.html", list_id = list_id, list_tag = list_tag, list_name = list_name)
  
  
  if request.method == "POST":
      list_tag = request.form["list_tag"]
      list_name = request.form["list_name"]

      stmt = List.query.all()
      for i in stmt:
      
          if(i.list_id == int(list_id)):
            i.list_name = list_name
            i.list_tag  = list_tag
      db.session.commit()

      list_division = List.query.all()
      return render_template("temp_1.html", list_division = list_division)


@app.route('/list/<list_id>/delete', methods = ["GET", "POST"])
def DeleteList(list_id):
    stmt = List.query.all()
    for i in stmt:
      if(i.list_id == int(list_id)):
        db.session.delete(i)
        db.session.commit()
        
    
    list_division = List.query.all()
    return render_template("temp_1.html", list_division = list_division)



@app.route('/card/<list_id>', methods = ["GET", "POST"])
def card(list_id):
  list_division = Card.query.all()
  result = []
  for i in list_division:
    if(i.list_id == int(list_id)):
      result.append(i)

  return render_template("temp_4.html", result = result)
      
      
@app.route('/card/add', methods = ["GET", "POST"])
def AddCard():
    if request.method == "GET":
       return render_template("temp_5.html")

    
    if request.method == "POST":
      title = request.form["card_title"]
      content = request.form["card_content"]
      deadline = request.form["card_deadline"]
      status = request.form["card_status"]
      list_id = request.form["list_id"]
      

      stmt = Card(card_title = title, card_content = content, card_deadline = deadline, card_status = status, list_id = list_id)
      db.session.add(stmt)
      db.session.commit()

      list_division = Card.query.all()
      result = []
      for i in list_division:
          if(i.list_id == int(list_id)):
            result.append(i)

      return render_template("temp_4.html", result = result)    




@app.route('/card/<card_id>/update', methods = ["GET", "POST"])
def UpdateCard(card_id):
  if request.method == "GET":
    stmt = Card.query.all()
    for i in stmt:
      
      if(i.card_id == int(card_id)):
        card_id = i.card_id
        card_title = i.card_title
        card_content = i.card_content
        card_deadline = i.card_deadline
        card_status = i.card_status
        list_id = i.list_id
      
    return render_template("temp_6.html",card_id = card_id,  card_title = card_title, card_content = card_content, card_deadline = card_deadline, card_status = card_status, list_id = list_id)
  
  
  if request.method == "POST":
      card_title = request.form["card_title"]
      card_content = request.form["card_content"]
      card_deadline = request.form["card_deadline"]
      card_status = request.form["card_status"]
      list_id = request.form["list_id"]

      stmt = Card.query.all()
      for i in stmt:
      
          if(i.card_id == int(card_id)):
            i.card_title = card_title
            i.card_content = card_content
            i.card_deadline = card_deadline
            i.card_status = card_status
            i.list_id = list_id
      db.session.commit()

      list_division = Card.query.all()
      result = []
      for i in list_division:
         if(i.list_id == int(list_id)):
           result.append(i)

      return render_template("temp_4.html", result = result)



@app.route('/card/<card_id>/delete', methods = ["GET", "POST"])
def DeleteCard(card_id):
    stmt = Card.query.all()
    for i in stmt:
      if(i.card_id == int(card_id)):
        list_id = i.list_id
        db.session.delete(i)
        db.session.commit()
        
    
    list_division = Card.query.all()
    result = []
    for i in list_division:
      if(i.list_id == int(list_id)):
        result.append(i)

    return render_template("temp_4.html", result = result)


@app.route('/summary', methods = ["GET", "POST"])
def Summary():
  
  stmt = Card.query.all()
  dic = {}

  for i in stmt:
    if(i.list_id in dic):
      dic[i.list_id] = dic[i.list_id] + 1
    else:
      dic[i.list_id] = 1 
      
  list = []

  # for lists 
  for i in dic:
    list.append([i, dic[i]])
    
  stmt_1 = List.query.all()
  
  for i in stmt_1:
    for j in range(len(list)):
      if(i.list_id == list[j][0]):
        list[j].append(i.list_tag)
        
  list.sort(key = lambda x: x[0])

  # for completed and delayed missions
  stmt_2 = Card.query.all()
  completed_number = 0
  delayed_number = 0

  for i in stmt_2:
    if(i.card_status == "Completed"):
      completed_number = completed_number + 1

      
    if(i.card_status == "Delayed"):
      delayed_number = delayed_number + 1 
      
      

  
  return render_template("temp_7.html", list = list, delayed_number = delayed_number, completed_number = completed_number)










# Handling Exceptions for API 

  
class NotFoundError(HTTPException):
  def __init__(self, status_code):
    self.response = make_response('', status_code)


class Error(HTTPException):
  def __init__(self, status_code, error_code, error_message):
    message = {"error_code": error_code, 
               "error_message": error_message}
    self.response = make_response(message, status_code)






# API

class UserApi(Resource):
  
  def get(self, list_id):
    
    data = db.session.query(List).filter(List.list_id == list_id).first()

    if data:
      return {"list_id" : data.list_id, "list_tag" : data.list_tag, "list_name" : data.list_name}
      
    else:
      raise NotFoundError(status_code = 404)


  
  def put(self, list_id):
    data = db.session.query(List).filter(List.list_id == list_id).first()

    if data is None:
      raise NotFoundError(status_code = 404)
      
    else:
      
      args = update_list_parser.parse_args()
      list_tag = args.get("list_tag", None)
      list_name = args.get("list_name", None)

      
    # Raising the exceptions
      
      if list_tag is None or type(list_tag) is not(str):
         raise Error(status_code = 400, error_code = "List01", error_message = "List Tag is required and should be string.")

      if len(list_tag) > 7:
         raise Error(status_code = 400, error_code = "List02", error_message = "List Tag should not be more than 7 letters")

      if list_name is None or type(list_name) is not(str):
         raise Error(status_code = 400, error_code = "List03", error_message = "List Name is required and should be string.")           

      if len(list_name) > 15:
         raise Error(status_code = 400, error_code = "List04", error_message = "List Name should not be more than 15 letters")

    
      # If everything is fine updating the entries 
      data.list_tag = list_tag
      data.list_name = list_name
      db.session.commit()
      
      return {"list_id" : data.list_id, "list_tag" : data.list_tag, "list_name" : data.list_name}


  
  def delete(self, list_id):
    
    data = db.session.query(List).filter(List.list_id == list_id).first()

    if data:
      db.session.delete(data)
      db.session.commit()
      return {}, 200
      
    else:
      raise NotFoundError(status_code = 404)



  
  
  def post(self):
    
    args = create_list_parser.parse_args()
    list_tag = args.get("list_tag", None)
    list_name = args.get("list_name", None)
    
    
    # Raising the exceptions
    if list_tag is None or type(list_tag) is not(str):
         raise Error(status_code = 400, error_code = "List01", error_message = "List Tag is required and should be string.")

    if len(list_tag) > 7:
         raise Error(status_code = 400, error_code = "List02", error_message = "List Tag should not be more than 7 letters")

    if list_name is None or type(list_name) is not(str):
         raise Error(status_code = 400, error_code = "List03", error_message = "List Name is required and should be string.")           

    if len(list_name) > 15:
         raise Error(status_code = 400, error_code = "List04", error_message = "List Name should not be more than 15 letters")
    
    data_roll = db.session.query(List).filter(List.list_tag == list_tag).first()
    if data_roll:
        raise NotFoundError(status_code = 409)
    
    
    # If everything is fine and no exception is raised, then add new Course
    new_list = List(list_tag = list_tag, list_name = list_name)
    db.session.add(new_list)
    db.session.commit()
    return {"list_tag" : list_tag, "list_name" : list_name}, 201




api.add_resource(UserApi, "/api/list/add", "/api/list/<list_id>")






class UserCardApi(Resource):
 
  
  def get(self, card_id):
    
    data = db.session.query(Card).filter(Card.card_id == card_id).first()

    if data:
      return {"card_id" : data.card_id, "card_title" : data.card_title, "card_content" : data.card_content, "card_deadline" : data.card_deadline, "card_status" : data.card_status, "list_id" : data.list_id}
    else:
      raise NotFoundError(status_code = 404)
    
    
  def put(self, card_id):
    
    data = db.session.query(Card).filter(Card.card_id == card_id).first()

    if data is None:
      raise NotFoundError(status_code = 404)
      
    else:
      
      args = update_card_parser.parse_args()
      card_title = args.get("card_title", None)
      card_content = args.get("card_content", None)
      card_deadline = args.get("card_deadline", None)
      card_status = args.get("card_status", None)
      list_id = args.get("list_id", None)
                            
      
      # Raising the exceptions
      if card_title is None or type(card_title) is not(str):
         raise Error(status_code = 400, error_code = "Card01", error_message = "Card Title is required and should be String")     

      if len(card_title) > 10:
         raise Error(status_code = 400, error_code = "Card02", error_message = "Card Title should not be more than 10 letters")

      
      if card_content is None or type(card_content) is not(str):
         raise Error(status_code = 400, error_code = "Card03", error_message = "Card Content is required and should be String")

      if len(card_content) > 20:
         raise Error(status_code = 400, error_code = "Card04", error_message = "Card Content should not be more than 20 letters")


      if card_status is None or type(card_status) is not(str):
         raise Error(status_code = 400, error_code = "Card05", error_message = "Card Status is required and should be String")

      if len(card_status) > 20:
         raise Error(status_code = 400, error_code = "Card06", error_message = "Card Status should not be more than 20 letters")  

        
      if list_id is None or type(list_id) is not(int):
         raise Error(status_code = 400, error_code = "Card07", error_message = "List Id is required and should be String")
      
      
      data.card_title = card_title
      data.card_content = card_content
      data.card_deadline = card_deadline
      data.card_status = card_status
      data.list_id = list_id
      db.session.commit()
      
      return {"card_id" : data.card_id, "card_title" : data.card_title, "card_content" : data.card_content, "card_deadline" : data.card_deadline, "card_status" : data.card_status, "list_id" : data.list_id}

      
      
      

  
  def delete(self, card_id):
    
    data = db.session.query(Card).filter(Card.card_id == card_id).first()

    if data:
      db.session.delete(data)
      db.session.commit()
      return {}, 200
      
    else:
      raise NotFoundError(status_code = 404)



  
  
  def post(self):

      args = create_card_parser.parse_args()
      card_title = args.get("card_title", None)
      card_content = args.get("card_content", None)
      card_deadline = args.get("card_deadline", None)
      card_status = args.get("card_status", None)
      list_id = args.get("list_id", None)


    
      # Raising the exceptions
      if card_title is None or type(card_title) is not(str):
         raise Error(status_code = 400, error_code = "Card01", error_message = "Card Title is required and should be String")     

      if len(card_title) > 10:
         raise Error(status_code = 400, error_code = "Card02", error_message = "Card Title should not be more than 10 letters")

      
      if card_content is None or type(card_content) is not(str):
         raise Error(status_code = 400, error_code = "Card03", error_message = "Card Content is required and should be String")

      if len(card_content) > 20:
         raise Error(status_code = 400, error_code = "Card04", error_message = "Card Content should not be more than 20 letters")


      if card_status is None or type(card_status) is not(str):
         raise Error(status_code = 400, error_code = "Card05", error_message = "Card Status is required and should be String")

      if len(card_status) > 20:
         raise Error(status_code = 400, error_code = "Card06", error_message = "Card Status should not be more than 20 letters")  

        
      if list_id is None or type(list_id) is not(int):
         raise Error(status_code = 400, error_code = "Card07", error_message = "List Id is required and should be String")


      data_roll = db.session.query(Card).filter(Card.card_title == card_title).first()
      if data_roll:
        raise NotFoundError(status_code = 409)

    
      new_card = Card(card_title = card_title, card_content = card_content, card_deadline = card_deadline, card_status = card_status, list_id = list_id)
      db.session.add(new_card)
      db.session.commit()
    
      return {"card_title" : card_title, "card_content" : card_content, "card_deadline" : card_deadline, "card_status" : card_status, "list_id" :list_id}, 201








api.add_resource(UserCardApi, "/api/card/add", "/api/card/<card_id>")






if __name__ == '__main__':
  app.run()
