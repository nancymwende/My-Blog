from . import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))
        
class User(UserMixin, db.Model):
        __tablename__ = 'users'
        
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(255))
        email = db.Column(db.String(255), unique=True, index=True)
        bio = db.Column(db.String(255))
        profile_pic_path = db.Column(db.String())
        password_hash = db.Column(db.String(255))

        @property
        def password(self):
                raise AttributeError('You cannot read the password attribute')

        @password.setter
        def password(self, password):
                self.password_hash = generate_password_hash(password)

        def verify_password(self, password):
                return check_password_hash(self.password_hash, password)

        def __repr__(self):
                return f'User {self.username}'
        
        
class Quote:
        '''
        quotes class to define quotes objects
        ''' 
        def __init__(self,author,quote,permalink):
                self.author = author
                self.quote = quote
                self.permalink = permalink 
        
class Blog(db.Model):
        _tablename_='blogs'
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(255))
        category = db.Column(db.String(255))
        content= db.Column(db.String(255))
        created_by= db.Column(db.String(255))
        date_posted = db.Column(db.DateTime, default=datetime.utcnow)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

        def save_blog(self):
                db.session.add(self)
                db.session.commit()
                
        def delete_blog(self):
                db.session.delete(self)
                db.session.commit()        
                
        @classmethod
        def get_blogs(cls,id):
                blogs =Blog.query.filter_by(blog_id=id).all()
                return blogs 
        @classmethod
        def get_current_blog(cls,user_id):
                blogs =Blog.query.filter_by(user_id=user_id)
                return blogs 
        
        def __repr__(self):
                return f'Blog {self.title}'


        
        
class Post(db.Model):
        _tablename_ = 'posts'
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(255))
        category = db.Column(db.String)
        content = db.Column(db.Text)
        date_posted = db.Column(db.DateTime, default=datetime.utcnow)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

        def save_post(self):
                db.session.add(self)
                db.session.commit()
        
        def __repr__(self):
                return f'Post {self.title}'

class Comment(db.Model):
        __tablename__ = 'comments'
        id = db.Column(db.Integer, primary_key=True)
        comment = db.Column(db.String(255))
        user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
        blog_id = db.Column(db.Integer, db.ForeignKey("blog.id"))


        def save_comment(self):
                db.session.add(self)
                db.session.commit()
        
        @classmethod
        def get_comments(cls, blog_id):
                comments = Comment.query.filter_by(blog_id=blog_id).all()
                return comments
        
        
        @classmethod
        def get_comment_author(cls, user_id):
                author = User.query.filter_by(id=user_id).first()

                return author
                
        @classmethod
        def delete_comment(id):
                comment = Comment.query.filter_by(id=id).first()
                db.session.delete(comment)
                db.session.commit() 
                
class Subscriber(db.Model):
        __tablename__ = 'subscribers'
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(255), unique=True, index=True)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)

        def save_subscriber(self):
                db.session.add(self)
                db.session.commit()

        @classmethod
        def get_subscribers(cls):
                subscribers = Subscriber.query.all()
                return subscribers

        def __repr__(self):
                return f'Subscriber {self.email}'                


