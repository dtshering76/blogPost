import os
from flask import Flask, render_template, redirect, request,url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

####################DATABASE CONFIG########################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)
Migrate(app,db)
app.app_context().push()

###############CREATE BLOG POST MODELS############################################

class Posts(db.Model):
    
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __init__(self,title,author,slug,content):
        
        self.title = title
        self.author = author
        self.slug = slug
        self.content = content
    
    def __repr__(self):
        
        return f"Title:{self.title} Author:{self.author}"

#############CREATE A POSTS FORM###########################

class PostForm(FlaskForm):
    
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author',validators=[DataRequired()])
    slug = StringField('Slug',validators=[DataRequired()])
    content = StringField('Content',validators=[DataRequired()], widget=TextArea)
    submit = SubmitField('Add Post',validators=[DataRequired()])
###########Add Post Page####################

@app.route('/add_post',methods=['GET','POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        Posts(title=form.title.data, author=form.author.data, slug=form.slug.data,content=form.content.data)
    
##########Clear Content##################
        form.title.data = ""
        form.author.data = ""
        form.slug.data = ""
        form.content.data = ""
        
        flash('Blog Post Submitted Successfully!')
    return render_template('add_post.html', form=form)

###############VIEWS###############################
app.route('/')
def index():
    return render_template('index.html')


   
    
    
    
if __name__ == "__main__":
    app.run(debug=True)