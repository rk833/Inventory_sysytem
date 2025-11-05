from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

# Initialize Flask app and configure settings
app = Flask(__name__)
app.config['SECRET_KEY'] = 'adchgdngsghjgmjhedthncgstnxhtrdfyt'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)  
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# User model for authentication
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Base model for stock items
class StockItem(db.Model):
    __tablename__ = 'stock_item'
    id = db.Column(db.Integer, primary_key=True)
    stock_code = db.Column(db.String(50), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50))  # Polymorphic type field

    __mapper_args__ = {
        'polymorphic_identity': 'stock_item',
        'polymorphic_on': type
    }

    @property
    def get_price_with_vat(self):
        """Calculate the price including VAT."""
        return self.price * (1 + self.get_vat / 100)

    @property
    def get_vat(self):
        """Return the VAT percentage."""
        return 17.5

    @property
    def get_stock_name(self):
        """Return the stock name."""
        return "Unknown Stock Name"

    @property
    def get_stock_description(self):
        """Return the stock description."""
        return "Unknown Stock Description"

# Derived model for Navigation Systems
class NavSys(StockItem):
    __tablename__ = 'nav_sys'
    id = db.Column(db.Integer, db.ForeignKey('stock_item.id'), primary_key=True)
    brand = db.Column(db.String(100), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'nav_sys'
    }

    @property
    def get_stock_name(self):
        """Return the stock name."""
        return "Navigation system"

    @property
    def get_stock_description(self):
        """Return the stock description."""
        return "GeoVision Sat Nav"

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('main'))
            else:
                return {'error': 'Invalid username or password'}, 401
        except Exception as e:
            return {'error': str(e)}, 500
    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        return redirect(url_for('login'))
    except Exception as e:
        return {'error': str(e)}, 500

# Main page route
@app.route('/')
@login_required
def main():
    items = StockItem.query.all()
    page = request.args.get('page', 1, type=int)  
    per_page = 10 
    pagination = StockItem.query.paginate(page=page, per_page=per_page) 
    return render_template('main.html', items=pagination.items, pagination=pagination)

# View item route
@app.route('/view/<int:item_id>', methods=['GET'])
@login_required
def view_item(item_id):
    item = StockItem.query.get_or_404(item_id)
    return render_template('view.html', item=item)


# Add item route
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        try:
            stock_type = request.form.get('type')
            stock_code = request.form.get('stock_code')
            quantity = int(request.form.get('quantity'))
            price = float(request.form.get('price'))
            
            # Validate input data
            if quantity < 0 and price < 0:
                flash('Quantity and price should not be negative!', 'danger')
                return redirect(url_for('add_item'))
            
            if quantity < 0:
                flash('Quantity should not be negative!', 'danger')
                return redirect(url_for('add_item'))
            
            if price < 0:
                flash('Price should not be negative!', 'danger')
                return redirect(url_for('add_item'))
            
            # Validate quantity does not exceed max quantity
            max_quantity = 100  
            if quantity > max_quantity:
                flash('Quantity exceeds the maximum allowed quantity!', 'danger')
                return redirect(url_for('add_item'))
            
            # Check if stock code already exists
            existing_item = StockItem.query.filter_by(stock_code=stock_code).first()
            if existing_item:
                flash('Stock code already exists!', 'danger')
                return redirect(url_for('add_item'))
            
            # Add item to the database
            if stock_type == 'NavSys':
                brand = request.form.get('brand')
                item = NavSys(stock_code=stock_code, quantity=quantity, price=price, brand=brand)
            else:
                item = StockItem(stock_code=stock_code, quantity=quantity, price=price)

            db.session.add(item)
            db.session.commit()
            flash("Item added successfully!", "success")
            return redirect(url_for('main'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('add_item'))

    return render_template('add.html')

# Update item route
@app.route('/update/<int:item_id>', methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    item = StockItem.query.get_or_404(item_id)

    if request.method == 'POST':
        try:
            quantity = int(request.form.get('quantity'))
            price = float(request.form.get('price'))

            # Validate input data
            if quantity < 0 and price < 0:
                flash('Quantity and price should not be negative!', 'danger')
                return redirect(url_for('update_item', item_id=item_id))
            
            if quantity < 0:
                flash('Quantity should not be negative!', 'danger')
                return redirect(url_for('update_item', item_id=item_id))
            
            if price < 0:
                flash('Price should not be negative!', 'danger')
                return redirect(url_for('update_item', item_id=item_id))
            
            # Validate quantity does not exceed max quantity
            max_quantity = 100  
            if quantity > max_quantity:
                flash('Quantity exceeds the maximum allowed quantity!', 'danger')
                return redirect(url_for('update_item', item_id=item_id))

            # Update item details
            item.quantity = quantity
            item.price = price
            if isinstance(item, NavSys):
                item.brand = request.form.get('brand')
            db.session.commit()
            flash("Item updated successfully!", "success")
            return redirect(url_for('main'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('update_item', item_id=item_id))

    return render_template('update.html', item=item)

# Delete item route
@app.route('/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    try:
        item = StockItem.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        flash('Item deleted successfully!', 'success')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')
    return redirect(url_for('main'))

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
