from sqlalchemy import validates, hybrid_property, relationship
from config import db, bcrypt
import re

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), unique=True, nullable=False)
    _password_hash = db.Column(db.string(100), nullable=False)

    #Relationships
    blogs = relationship('Blog', back_populates='user', cascade='all, delete-orphan')
    comments = relationship('Comment', back_populates='user', cascade='all, delete-orphan')

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes cannot be viewed')
    
    @password_hash.setter
    def password_hash(self, password):
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters')
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)
    
    def __repr__(self):
        return f'<User: {self.username}>'
    

class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body_text = db.Column(db.Text, nullable=False)
    url = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    #Relationships
    user = relationship('User', back_populates='blogs')
    comments = relationship('Comment', back_populates='blog', cascade='all, delete-orphan')

    @validates('title')
    def validate_title(self, key, title):
        if not title or len(title.strip()) == 0:
            raise ValueError('Title cannot be empty')
        if len(title) > 100:
            raise ValueError('Title has to be less than 100 characters.')
        return title.strip()
    
    @validates('body_text')
    def validate_body_text(self, key, body_text):
        if not body_text or len(body_text.strip()) == 0:
            raise ValueError('Body cannot be empty')
        if len(body_text) < 50:
            raise ValueError('Body must be at least 50 characters')
        return body_text.strip()
        
    @validates('url')
    def validate_url(self, key, url):
        if not url or len(url.strip()) == 0:
            raise ValueError('URL cannot be empty')
        if not re.match(r'https?://(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', url.strip()):
            raise ValueError('Must be a valid URL and contain http:// or https://')
        return url.strip()
    
    def __repr__(self):
        return f'<Blog: {self.title}>'
    

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)

    user = relationship('User', back_populates='comments')
    blog = relationship('Blog', back_populates='comments')

    @validates('comment')
    def validate_comment(self, key, comment):
        if not comment or len(comment.strip()) == 0:
            raise ValueError('Comment cannot be empty')
        return comment.strip()
    
    def __repr__(self):
        return f'<Comment by user: {self.user_id} on blog: {self.blog_id}>'


    
        