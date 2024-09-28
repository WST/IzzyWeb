from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from config import DB_CONFIG, SECRET_KEY

app = Flask(__name__)

# Configure MySQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY

db = SQLAlchemy(app)

class CryptoPair(db.Model):
    symbol = db.Column(db.String(20), primary_key=True)
    icon_class = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<CryptoPair {self.symbol}>'

@app.route('/api/glitter.jsp', methods=['GET'])
def api_handler():
    call = request.args.get('call')
    if call == 'pairs':
        return get_pairs()
    elif call == 'pair':
        symbol = request.args.get('symbol')
        return get_pair(symbol)
    else:
        return jsonify({'error': 'Invalid call parameter'}), 400

def get_pairs():
    pairs = CryptoPair.query.all()
    return jsonify([{
        'symbol': pair.symbol,
        'icon_class': pair.icon_class
    } for pair in pairs])

def get_pair(symbol):
    pair = CryptoPair.query.get_or_404(symbol)
    return jsonify({
        'symbol': pair.symbol,
        'icon_class': pair.icon_class
    })

def insert_initial_pairs():
    pairs = [
        ('BTCUSDT', 'fab fa-bitcoin'),
        ('ETHUSDT', 'fab fa-ethereum'),
        ('SOLUSDT', 'fas fa-sun'),
        ('XMRUSDT', 'fas fa-user-secret'),
        ('AVAXUSDT', 'fas fa-mountain'),
        ('POPCATUSDT', 'fas fa-cat'),
        ('SUIUSDT', 'fas fa-cube'),
        ('WIFUSDT', 'fas fa-wifi')
    ]
    
    for pair in pairs:
        existing_pair = CryptoPair.query.get(pair[0])
        if not existing_pair:
            new_pair = CryptoPair(symbol=pair[0], icon_class=pair[1])
            db.session.add(new_pair)
    
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This will create the table if it doesn't exist
        insert_initial_pairs()
    app.run(debug=True, host='127.0.0.1', port=5000)