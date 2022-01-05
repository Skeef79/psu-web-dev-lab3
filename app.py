from flask import Flask, render_template, request, redirect, url_for
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


@app.get('/')
def index():
    messages = MessageModel.query.order_by(MessageModel.claps.desc()).all()
    return render_template('index.html', messages=messages)


@app.post('/')
def add_message():
    errors = []

    if not request.form['sender']:
        errors.append('Требуется ввести имя отправителя')

    if not request.form['message']:
        errors.append('Требуется ввести сообщение')

    sender = request.form['sender']
    message = request.form['message']

    if sender and len(sender) > 30:
        errors.append('Имя автора должно быть от 1 до 30 символов')
    if message and len(message) > 1000:
        errors.append('Текст сообщения должен быть от 1 до 1000 символов')

    if errors:
        messages = MessageModel.query.order_by(MessageModel.claps.desc()).all()
        return render_template('index.html',
                               messages=messages,
                               errors=errors,
                               new_sender=sender,
                               new_message=message
                               )

    db.session.add(MessageModel(author=sender, message=message))
    db.session.commit()
    return redirect(url_for('index'))


@app.get('/messages/<int:messageId>')
def message_page(messageId):
    message = MessageModel.query.filter_by(id=messageId).first()
    if not message:
        return render_template('404.html', messageId=messageId)

    return render_template('message.html', message=message)


@app.post('/messages/<int:messageId>/claps')
def clap_message(messageId):
    message = MessageModel.query.filter_by(id=messageId).first()
    if not message:
        return render_template('404.html', messageId=messageId)
    message.claps += 1
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
