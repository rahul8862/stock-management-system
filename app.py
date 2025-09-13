from flask import Flask, request, jsonify
from models import db, Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/addProduct', methods=['POST'])
def add_product():
    data = request.get_json()
    product = Product(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        total_quantity=data['total_quantity'],
        available_quantity=data['available_quantity']
    )
    product.check_restock()
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product added successfully!"}), 201


@app.route('/getAllProduct', methods=['GET'])
def get_all_product():
    products = Product.query.all()
    product_list = []
    for p in products:
        product_list.append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "total_quantity": p.total_quantity,
            "available_quantity": p.available_quantity,
            "need_restock": p.need_restock
        })
    return jsonify(product_list)


@app.route('/getProductById/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "total_quantity": product.total_quantity,
        "available_quantity": product.available_quantity,
        "need_restock": product.need_restock
    })


@app.route('/updateProduct/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()

    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.total_quantity = data.get('total_quantity', product.total_quantity)
    product.available_quantity = data.get('available_quantity', product.available_quantity)

    product.check_restock()
    db.session.commit()
    return jsonify({"message": "Product updated successfully!"})


@app.route('/deleteProduct/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully!"})


@app.route('/restock/<int:id>', methods=['GET'])
def check_restock(id):
    product = Product.query.get_or_404(id)
    product.check_restock()
    db.session.commit()
    return jsonify({"id": product.id, "need_restock": product.need_restock})


@app.route('/restock/update/<int:id>', methods=['PUT'])
def update_restock_status(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    product.need_restock = data.get('need_restock', product.need_restock)
    db.session.commit()
    return jsonify({"message": "Restock status updated!"})


@app.route('/restock/list', methods=['GET'])
def get_restock_list():
    products = Product.query.filter_by(need_restock=True).all()
    product_list = []
    for p in products:
        product_list.append({
            "id": p.id,
            "name": p.name,
            "available_quantity": p.available_quantity,
            "total_quantity": p.total_quantity
        })
    return jsonify(product_list)


if __name__ == '__main__':
    app.run(debug=True)
