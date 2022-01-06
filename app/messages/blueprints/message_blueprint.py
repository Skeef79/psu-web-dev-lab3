from re import template
from flask import Blueprint, render_template, request, redirect, url_for
from app.messages.services.message_service import get_all_messages, get_message_by_id, increment_messsage_claps_by_id, create_message

message_blueprint = Blueprint(
    'messages', __name__, template_folder='../templates')


@message_blueprint.get('/')
def index():
    messages = get_all_messages()
    return render_template('index.html', messages=messages)


@message_blueprint.post('/')
def add_message():
    sender = request.form['sender']
    message = request.form['message']
    added_message, error = create_message(author=sender, message=message)

    if error:
        messages = get_all_messages()
        return render_template('index.html',
                               messages=messages,
                               error=error,
                               new_sender=sender,
                               new_message=message
                               )
    return redirect(url_for('messages.index'))


@message_blueprint.get('/messages/<int:message_id>')
def message_page(message_id):
    message = get_message_by_id(message_id)
    if not message:
        return render_template('404.html', message_id=message_id)

    return render_template('message.html', message=message)

#redirect to the page where user made request (idk is this the best solution or not)
def redirect_url(default='messages.index'):
    return request.args.get('next') or \
        request.referrer or \
        url_for(default)


@message_blueprint.post('/messages/<int:message_id>/claps')
def clap_message(message_id):
    claps = increment_messsage_claps_by_id(message_id=message_id)
    if not claps:
        return render_template('404.html', message_id=message_id)

    return redirect(redirect_url())

