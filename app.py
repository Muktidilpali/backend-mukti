from flask import Flask,request, jsonify
import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS


app=Flask(__name__)
CORS(app)
basedir= os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///'+ os.path.join('mukti.sqlite')

db= SQLAlchemy(app)
ma=Marshmallow(app)
class Product(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, nullable=False)
    price=db.Column(db.Float, nullable=False)
    sku= db.Column(db.String, nullable=False)
    photo= db.Column(db.String, nullable=False)
    def __init__(self,name, price,sku,photo):
        self.name=name
        self.price=price
        self.sku=sku
        self.photo=photo


class ProductSchema(ma.Schema):
    class Meta:
        fields=("id","name", "price","sku", "photo")


product_schema=ProductSchema()
products_schema=ProductSchema(many=True)


@app.route("/product", methods=["POST"])
def insert_product():
    name= request.json.get("name")
    price= request.json.get("price")
    sku= request.json.get("sku")
    photo=request.json.get("photo")
    record= Product(name,price,sku,photo)
    db.session.add(record)
    db.session.commit()

    return jsonify(product_schema.dump(record))


@app.route("/products",methods=["GET"])
def products():
    all_products=Product.query.all()
    return jsonify(products_schema.dump(all_products))

@app.route("/product/<id>",methods=["GET"])
def product(id):
    product=Product.query.get(id)
    return product_schema.jsonify(product)

@app.route("/product/<id>",methods=["PUT"])
def update(id):
    product=Product.query.get(id)
    name= request.json.get("name")
    price= request.json.get("price")
    sku= request.json.get("sku")
    photo=request.json.get("photo")
    
    product.name=name
    product.price=price

    db.session.commit()

    return product_schema.jsonify(product)

   
@app.route("/product/<id>",methods=["DELETE"])
def delete(id):    
    product=Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return "Product delete"

if __name__ == "__main__":
    app.run(debug=True)