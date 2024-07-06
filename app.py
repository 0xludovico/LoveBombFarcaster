from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sched, time
import threading

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lovebomb.db'
db = SQLAlchemy(app)

scheduler = sched.scheduler(time.time, time.sleep)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    image = db.Column(db.String(200))
    contributor = db.Column(db.String(100))
    recipient = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

db.create_all()

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    new_message = Message(
        text=data.get('text'),
        image=data.get('image'),
        contributor=data.get('contributor'),
        recipient=data.get('recipient')
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify({"message": "¡Envío exitoso!"})

@app.route('/schedule', methods=['POST'])
def schedule_delivery():
    data = request.json
    recipient = data.get('recipient')
    delivery_time = datetime.strptime(data.get('delivery_time'), '%Y-%m-%d %H:%M:%S')
    
    def deliver_love_bomb():
        messages = Message.query.filter_by(recipient=recipient).all()
        # Lógica para enviar los mensajes al destinatario
        print(f"Entregando Love Bomb a {recipient} con {len(messages)} mensajes.")
    
    delay = (delivery_time - datetime.utcnow()).total_seconds()
    scheduler.enter(delay, 1, deliver_love_bomb)
    threading.Thread(target=scheduler.run).start()
    
    return jsonify({"message": "¡Entrega programada!"})

if __name__ == '__main__':
    app.run(debug=True)
