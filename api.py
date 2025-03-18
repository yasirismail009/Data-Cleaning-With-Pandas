from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with

app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"User(name={self.name}, email={self.email})"

user_args=reqparse.RequestParser()
user_args.add_argument("name", type=str, help="Name cannot be blank", required=True)
user_args.add_argument("email", type=str, help="Email cannot be blank", required=True)

userFields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}

class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        result = UserModel.query.all()
        return result
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args['name'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        return user, 201
class User(Resource):
    @marshal_with(userFields)
    def get(self, user_id):
        result = UserModel.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="Could not find user with that id")
        return result
    
    @marshal_with(userFields)
    def patch(self, user_id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="Could not find user with that id")
        user.name = args['name']
        user.email = args['email']
        db.session.commit()
        return user
    
    @marshal_with(userFields)
    def delete(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="Could not find user with that id")
        db.session.delete(user)
        db.session.commit()
        result = UserModel.query.all()
        return result, 200



api.add_resource(Users, "/api/users/")
api.add_resource(User, "/api/users/<int:user_id>")

        

@app.route('/')
def home():
    return"<h1>API is running</h1>"


if __name__=='__main__':
    app.run(debug=True)