from types import MethodDescriptorType
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy, model
import os

app = Flask(__name__)

ENV = 'dev'
#SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
SQLALCHEMY_DATABASE_URI = 'sqlite:///messages.db'

if ENV == 'dev':
    app.debug = True
else:
    app.debug = False
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
        "://", "ql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class MessageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    message = db.Column(db.String(1000))
    claps = db.Column(db.Integer, default=0)


def validate(message, author):
    return len(author) > 0 and len(author) <= 30 and len(message) > 0 and len(message) <= 1000


@app.route('/', methods=['GET', 'POST'])
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    error = None
    if request.method == 'POST':
        sender = request.form['sender']
        message = request.form['message']

        if not validate(message,  sender):
            error = "Имя отправителя должно быть от 1 до 30 символов, а текст сообщения от 1 до 1000 символов"
        else:
            new_message = MessageModel(author=sender, message=message)
            db.session.add(new_message)
            db.session.commit()
            return redirect("/messages")

    messages = MessageModel.query.order_by(MessageModel.claps.desc()).all()
    return render_template('index.html', messages=messages, error=error)


@app.route('/messages/<int:messageId>', methods=['GET'])
def message_page(messageId):
    message = MessageModel.query.filter_by(id=messageId).first()
    if not message:
        return render_template('error.html', messageId=messageId)

    return render_template('message.html', message=message)


@app.route('/messages/<int:messageId>/claps', methods=['POST'])
def clap_message(messageId):
    message = MessageModel.query.filter_by(id=messageId).first()
    if not message:
        return f'Message {messageId} was not found'
    message.claps += 1
    db.session.commit()
    return redirect('/messages')


if __name__ == '__main__':
    app.run(debug=True)
