#importing libraries
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import request

#setting up flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#creating a database model 
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    number = db.Column(db.Integer)
    email = db.Column(db.String(100), unique=True)

    def __init__(self, name, number, email):
        self.name = name
        self.number = number
        self.email = email

#this command creates the db 
db.create_all()

#first post request which will create the user in the database
@app.route('/')
@app.route('/user_creation', methods=['POST'])
def createUser():
    if request.content_type == 'application/json':
        create_users = request.get_json()

        name = create_users.get('name')
        number = create_users.get('number')
        email = create_users.get('email')

        users = Person(name, number, email)

        db.session.add(users)
        db.session.commit()
        return jsonify("User created!")

#this get request will display the user details from the database
@app.route('/')
@app.route('/user_details', methods=['GET'])
def userDetails():
    user_details = db.session.query(Person.name, Person.number, Person.email).all()
    return jsonify(str(user_details))

#this route will delete the user from the database
@app.route('/')
@app.route('/user_delete/<id>', methods=['DELETE'])
def deleteUser(id):
    delete_users = db.session.query(Person).get(id)
    db.session.delete(delete_users)
    db.session.commit()
    return jsonify("User deleted!")

#updating the user details
@app.route('/')
@app.route('/user_update/<id>', methods=['PUT'])
def updateUser(id):
    if request.content_type == 'application/json':
        update_user = request.get_json()
        name = update_user.get('name')
        number = update_user.get('number')
        email= update_user.get('email')

        updating = db.session.query(Person).get(id)

        updating.name = name
        updating.number = number
        updating.email = email
        db.session.commit()
        return jsonify("Updated!")

if __name__ == '__main__':
    app.run(debug=True)

