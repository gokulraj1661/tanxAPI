from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import websocket
import json
import os
import threading

app = Flask(__name__)

ma = Marshmallow(app)

class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app.config.from_object(Config)
db = SQLAlchemy(app)
class Alert(db.Model):
    user_email = db.Column(db.String, primary_key=True)
    target_price = db.Column(db.Float)
    symbol = db.Column(db.String)

    def __init__(self, user_email, target_price, symbol):
        self.user_email = user_email
        self.target_price = target_price
        self.symbol = symbol

class AlertSchema(ma.Schema):
    class Meta:
        fields = ('user_email', 'target_price', 'symbol')

alert_schema = AlertSchema()
alert_schemas = AlertSchema(many=True)

def check_price_and_notify(symbol, current_price):
    for alert in Alert.query.all():
        if current_price <= alert.target_price:
            print(f"Target Reached {alert.user_email}")

def start_websocket(symbol):
    websocket_url = f'wss://stream.binance.com:9443/ws/{symbol.lower()}@kline_1m'

    def on_message(ws, message):
        data = json.loads(message)
        current_price = float(data['k']['c'])
        print(f"Current Price: {current_price}")
        check_price_and_notify(symbol, current_price)

    ws = websocket.WebSocketApp(websocket_url, on_message=on_message)
    ws_thread = threading.Thread(target=ws.run_forever)
    ws_thread.start()

@app.route('/alerts/create', methods=['POST'])
def create_alert():
    target_price = request.json['target_price']
    user_email = request.json['user_email']
    symbol = request.json['symbol']

    new_alert = Alert(user_email, target_price, symbol)
    db.session.add(new_alert)
    db.session.commit()

    start_websocket(symbol)
    return jsonify({"message": f"new alert added"})
@app.route('/alerts/getalerts', methods=['GET'])
def get_alerts():
    all_alerts=Alert.query.all()
    resukt=alert_schemas.dump(all_alerts)
    return jsonify(resukt)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
