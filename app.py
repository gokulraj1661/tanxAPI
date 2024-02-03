from flask import Flask, request, jsonify,flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
import websocket
import json
import os
import threading
import time
import smtplib
import logging
app = Flask(__name__)

ma = Marshmallow(app)

class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
class Alert(db.Model):
    user_email = db.Column(db.String,primary_key=True)
    target_price = db.Column(db.Float)
    symbol = db.Column(db.String)
    status=db.Column(db.String)
    
    def __init__(self, user_email, target_price, symbol, status):
        self.user_email = user_email
        self.target_price = target_price
        self.symbol = symbol
        self.status = status

class AlertSchema(ma.Schema):
    class Meta:
        fields = ('user_email', 'target_price', 'symbol', 'status')

alert_schema = AlertSchema()
alert_schemas = AlertSchema(many=True)

current_price = 0.0
price_lock = threading.Lock()

class WebSocketManager:
    def __init__(self, symbol):
        self.symbol = symbol
        self.ws_thread = threading.Thread(target=self.fetch_current_price)
        self.ws_thread.start()

    def fetch_current_price(self):
        websocket_url = f'wss://stream.binance.com:9443/ws/{self.symbol.lower()}@kline_1m'

        def on_message(ws, message):
            global current_price
            data = json.loads(message)
            current_price = float(data['k']['c'])
            print(f"Current Price: {current_price}")
        ws = websocket.WebSocketApp(websocket_url, on_message=on_message)
        ws.run_forever()
        
def send_email(recipient_email, subject, body):
    try:
        smtp_server = 'smtp.gmail.com'  # Update with your SMTP server
        smtp_port = 587  # Update with the appropriate port
        smtp_username = 'gokulraj.s2020@vitstudent.ac.in'  # Update with your email
        smtp_password = 'aazj lecr rvdq krwn'  # Update with your email password

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        msg = f'Subject: {subject}\n\n{body}'
        server.sendmail(smtp_username, recipient_email, msg)
        logging.info('Email sent successfully!')
    except Exception as e:
        logging.error(f'An error occurred while sending the email: {e}')
    finally:
        if 'server' in locals():  # Check if the 'server' variable is defined
            server.quit()
def check_alerts():
       with app.app_context():
           while True:
               alerts = Alert.query.all()
               for alert in alerts:
    
            
                  if current_price >= alert.target_price and alert.status == 'active':
                      subject = 'Alert Triggered'
                      body = f"Your alert for {alert.symbol} has been triggered. The current price is {current_price}."
                      send_email(alert.user_email, subject, body)


                      alert.status= 'trigerred'
                      db.session.commit()
                      
        
                  time.sleep(5)
def start_websocket_in_thread(symbol):
    WebSocketManager(symbol)

@app.route('/alerts/create', methods=['POST'])
def create_alert():
    target_price = request.json['target_price']
    user_email = request.json['user_email']
    symbol = request.json['symbol']
    status = request.json['status']
    new_alert = Alert(user_email, target_price, symbol, status)
    db.session.add(new_alert)
    db.session.commit()

    return jsonify({"message": f"new alert added"})

@app.route('/alerts/getalerts', methods=['GET'])
def get_alerts():
    all_alerts = Alert.query.all()
    result = alert_schemas.dump(all_alerts)
    return jsonify(result)

@app.route('/alerts/delete/<id>',methods=['DELETE'])

def delete_alert(id):
    res = Alert.query.get(id)
    if res:
        db.session.delete(res)
        db.session.commit()
        return jsonify({"message": f"Alert with email {id} has been deleted"})
    else:
        return jsonify({"message": "Alert not found"}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
       
    # Start a separate thread to manage the WebSocket and check alerts
    symbol_to_track = "btcusdt"
    start_websocket_in_thread(symbol_to_track)
    background_thread = threading.Thread(target=check_alerts)
    background_thread.start()   
    # Run the Flask app
    app.run(debug=True)
