# Flask Stock Management System


A simple **Flask-based REST API** for managing products in inventory.  
The system tracks products and includes restock logic to determine when a product needs to be replenished.

## Features
- Add, view, update, and delete products
- Auto-calculated **restock status** based on available vs. total quantity
- Endpoints for manual restock updates
- List products that require restocking
- SQLite database with SQLAlchemy ORM