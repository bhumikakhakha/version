from flask import Flask, render_template, url_for,flash,redirect,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import register,login,new
from flask_login import current_user
from flask_bcrypt import Bcrypt


app = Flask(__name__)

app.config['SECRET_KEY'] = '38c8058800ce1b60'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(15),nullable=False)

def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable= False, default=datetime.utcnow)


def __repr__(self):
    return f"Post('{self.title}')"


@app.route("/")
@app.route("/home")
def home():
  posts = Post.query.all()
  return render_template('home.html', posts=posts)


@app.route("/about")
def about():
  return render_template('about.html', title='About')

@app.route("/register",methods=['GET','POST'])
def reg():
    form = register()
    if form.validate_on_submit():
       hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
       user = User(username=form.username.data, email=form.email.data, password=hashed_password)
       db.session.add(user)
       db.session.commit()
       flash('Registration successful','success')
       return redirect(url_for('log'))
    
    return render_template('register.html', title='Register',form=form)

@app.route("/login",methods=['GET','POST'])
def log():
  form = login()
  if form.validate_on_submit:
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
        flash("Successfully logged in!",'success')
        return redirect(url_for('new_post')) 
    else:
        flash('Login Unsuccessful','danger')
        return redirect(url_for('log'))
    return render_template('login.html', title='Login',form=form)

@app.route("/post/create",methods=['GET','POST'])
def new_post():
    form = new()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        post = Post(title=title, content=content)

        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!!!','success')
        return redirect(url_for('home'))
    return render_template('create.html',title='Create Post',form=form)

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

if __name__ == '__main__':
   app.run(debug=True)
