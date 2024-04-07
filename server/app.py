from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route("/")
def index():
    return "<h1>Welcome to my Chatterbox</h1>"

@app.route('/messages')
def messages():
    my_messages = Message.query.order_by(Message.created_at.asc()).all()

    message_list = []

    for message in my_messages:
        message_list.append(message.to_dict())

    response = make_response(
        message_list,
        200
    )

    return response

@app.route("/messages", methods=["POST"])
def create_message():
    data = request.get_json()
    
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()

    return make_response(
        new_message.to_dict(),
        200
    )

@app.route('/messages/<int:id>', methods=["PATCH"])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    data = request.get_json()
    message.body = data['body']
    db.session.commit()
    return make_response(
        message.to_dict(),
         200
    )

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.filter(Message.id == id).first()
    db.session.delete(message)
    db.session.commit()
    return make_response(
        {"message": "Message deleted successfully"},
        200
        )

if __name__ == '__main__':
    app.run(port=5555)
