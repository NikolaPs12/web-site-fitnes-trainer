from flask import Blueprint, render_template, request, jsonify, flash
from ..models.chat import Message
from ..extensions import db, socketio
from flask import current_app 
from ..forms import ChatForm
from flask_socketio import emit

chat_bp = Blueprint('chat', __name__, template_folder='templates')

@chat_bp.route('/chat', methods=['POST', 'GET'])
def chat():
    form = ChatForm()
    messages = Message.query.order_by(Message.timestamp.asc()).all()
    return render_template('chat/chat.html', form=form, messages=messages)


@chat_bp.route('/messages')
def get_messages():
    msgs = Message.query.order_by(Message.timestamp.asc()).all()
    data = [{'id': m.id, 'text': m.user_message} for m in msgs]
    return jsonify(data)
