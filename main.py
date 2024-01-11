from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from dataclasses import dataclass
import requests
from producer import publish

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db/main'
CORS(app)

db = SQLAlchemy(app)

@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

class ProductUser(db.Model):
    # TO_DEBUG: UniqueConstraint is not working as expected. Correct it.
    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', name='user_product_unique'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

@app.route('/api/products')
def index():
    return jsonify(Product.query.all())

@app.route('/api/products/<int:pk>/like', methods=['POST'])
def like_product(pk):
    req = requests.get('http://docker.for.mac.localhost:8000/api/user/')
    json = req.json()
    print(json,pk)
    try:
        productUser = ProductUser(user_id=json['id'],product_id=pk)
        if productUser:
            db.session.add(productUser)
            db.session.commit()
            publish('product_liked', pk)
    except:
        abort(400, {"error": "You already liked this product"})
    return jsonify({
        'message': 'Successfully liked post'
    })



if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')