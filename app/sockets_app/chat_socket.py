from flask_socketio import emit
from flask import request
from ..extensions import socketio, db
from ..models.chat import Message

def init_socket_chat(socketio):
    @socketio.on('connect', namespace="/chat")
    def handle_connect():
        print(f"✅ Клиент подключился: {request.sid}")
        
        # Отправляем историю сообщений для чата
        messages = Message.query.order_by(Message.timestamp.asc()).all()
        history = [{'id': m.id, 'message': m.user_message} for m in messages]
        emit('chat_history', history)

    @socketio.on('disconnect', namespace="/chat")
    def handle_disconnect():
        print(f"❌ Клиент отключился: {request.sid}")

    @socketio.on('send_message', namespace="/chat")
    def handle_message(data):
        message_text = data.get('message', '').strip()
        
        if not message_text:
            return
        
        msg = Message(user_message=message_text)
        try:
            db.session.add(msg)
            db.session.commit()
            emit('receive_message', {
                'id': msg.id, 
                'message': msg.user_message
            }, broadcast=True)
        except Exception as e:
            print(f"Ошибка сохранения сообщения: {e}")
            db.session.rollback()

    @socketio.on('test_message')
    def handle_test_message(data):
        print(f"🎯 Сервер получил тестовое сообщение: {data}")
        
        emit('test_response', {
            'status': 'success', 
            'message': 'Сервер получил ваше сообщение!',
            'received_data': data
        })
        print("📤 Сервер отправил test_response")