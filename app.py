from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Настройка базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    membership = db.Column(db.String(50), default='None')  # Новый столбец для абонемента


# Главная страница
@app.route('/')
def home():
    return render_template('index.html')


# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('User already exists!', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please select a membership plan.', 'success')
        return redirect(url_for('membership'))  # Перенаправляем на выбор абонемента

    return render_template('register.html')


# Выбор абонемента
@app.route('/membership', methods=['GET', 'POST'])
def membership():
    if request.method == 'POST':
        selected_plan = request.form['plan']
        user = User.query.order_by(User.id.desc()).first()  # Последний зарегистрированный пользователь
        user.membership = selected_plan
        db.session.commit()

        flash(f'You selected the {selected_plan} plan!', 'success')
        return redirect(url_for('home'))

    return render_template('membership.html')


# Инициализация базы данных
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
