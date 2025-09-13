from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    total_quantity = db.Column(db.Integer, nullable=False)
    available_quantity = db.Column(db.Integer, nullable=False)
    need_restock = db.Column(db.Boolean, default=False)

    def check_restock(self):
        if self.total_quantity > 0:
            self.need_restock = self.available_quantity < (0.2 * self.total_quantity)
        else:
            self.need_restock = False
