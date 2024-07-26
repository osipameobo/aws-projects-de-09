from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./email.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String, primary_key=True, nullable=False)
    email = db.Column(db.String, nullable=True)

with app.app_context():
    db.drop_all()
    db.create_all()
    user = User(username="John", email="john@clarusway.com")
    db.session.add(user)
    db.session.commit()

def find_emails(keyword):
    with app.app_context():
        users = User.query.filter(User.username.like(f"%{keyword}%")).all()
        user_emails = [(user.username, user.email) for user in users]
        if not user_emails:
            user_emails = [("Not Found", "Not Found")]
        return user_emails

def insert_email(name, email):
    with app.app_context():
        response = ''
        if len(name) == 0 or len(email) == 0:
            response = 'Username or email cannot be empty!!'
        else:
            existing_user = User.query.filter_by(username=name).first()
            if existing_user is None:
                new_user = User(username=name, email=email)
                db.session.add(new_user)
                db.session.commit()
                response = f"User {name} and {email} have been added successfully"
            else:
                response = f"User {name} already exists"
        return response

@app.route('/', methods=['GET', 'POST'])
def emails():
    if request.method == 'POST':
        user_app_name = request.form['user_keyword']
        user_emails = find_emails(user_app_name)
        return render_template('emails.html', name_emails=user_emails, keyword=user_app_name, show_result=True)
    else:
        return render_template('emails.html', show_result=False)

@app.route('/add', methods=['GET', 'POST'])
def add_email():
    if request.method == 'POST':
        user_app_name = request.form['username']
        user_app_email = request.form['useremail']
        result_app = insert_email(user_app_name, user_app_email)
        return render_template('add-email.html', result_html=result_app, show_result=True)
    else:
        return render_template('add-email.html', show_result=False)

# Add a statement to run the Flask application which can be reached from any host on port 80.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
