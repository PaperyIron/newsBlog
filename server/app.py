#app.py
from flask import Flask, request, session, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Resource, Api
from config import db, bcrypt
from models import User, Blog, Comment
import os

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'test-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username')
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')

        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        if password != password_confirmation:
            return jsonify({'error': 'Password does not match'}), 422
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 422
        
        new_user = User(username=username)
        new_user.password_hash = password
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id

        return jsonify(new_user.to_dict()), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        user = User.query.filter_by(username=username).first()

        if not user or not user.authenticate(password):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        session['user_id'] = user.id

        return jsonify(user.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 401
    
@app.route('/check_session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            return jsonify(user.to_dict()), 200
    return jsonify({}), 401

@app.route('/logout', methods=['DELETE'])
def logout():
    if 'user_id' not in session:
        return jsonify({'error': 'No active session'}), 401
    session.pop('user_id', None)
    return jsonify({}), 204

class BlogList(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        if per_page > 100:
            per_page = 100

        pagination = Blog.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        blogs = [blog.to_dict() for blog in pagination.items]

        return jsonify({
            'blogs': blogs,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        })
    
    def post(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Must be logged in'}, 401
        
        try:
            data = request.get_json()
            if not data:
                return {'error': 'No data provided'}, 400
            
            new_blog = Blog(
                title = data.get('title'),
                body_text = data.get('body_text'),
                url = data.get('url'),
                user_id = user_id
            )

            db.session.add(new_blog)
            db.session.commit()

            return new_blog.to_dict(), 201
        
        except ValueError as e:
            return {'error': str(e)}, 400
        
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400
        
class BlogEdit(Resource):
    def get(self, id):
        if 'user_id' not in session:
            return {'error': 'Not authorized'}, 401
        
        blog = Blog.query.get(id)
        if not blog:
            return {'error': 'Blog not found'}, 404
        
        if blog.user_id != session['user_id']:
            return {'error': 'Not authorized'}, 401
        
        return blog.to_dict(), 200
    
    def patch(self, id):
        if 'user_id' not in session:
            return {'error': 'Not authorized'}, 401
        
        blog = Blog.query.get(id)
        if not blog:
            return {'error': 'Blog not found'}, 404

        if blog.user_id != session['user_id']:
            return {'error': 'Not authorized'}, 401

        try:
            data = request.get_json()
            if not data:
                return {'error': 'No data provided'}, 400

            if 'title' in data:
                blog.title = data['title']
            if 'body_text' in data:
                blog.body_text = data['body_text']
            if 'url' in data:
                blog.url = data['url']        
            
            db.session.commit()

            return blog.to_dict(), 200
        
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400
        
    def delete(self, id):
        if 'user_id' not in session:
            return {'error': 'Not authroized'}, 401
        
        blog = Blog.query.get(id)
        if not blog:
            return {'error': 'Blog not found'}, 404
        
        if blog.user_id != session['user_id']:
            return {'error': 'Not authorized'}, 403
        
        try:
            db.session.delete(blog)
            db.session.commit()
            return {}, 204
        
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400
        
class CommentList(Resource):
    def get(self):
        blog_id = request.args.get('blog_id', type=int)
        if not blog_id:
            return {'error': 'Blog parameter required'}, 404
        
        comments = Comment.query.filter_by(blog_id=blog_id).all()
        return [comment.to_dict() for comment in comments], 200
    
    def post(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Must be logged in'}, 401
        
        try:
            data = request.get_json()
            if not data:
                return {'error': 'No data provided'}, 400
            
            new_comment = Comment(
                comment = data.get('comment'),
                user_id = user_id,
                blog_id = data.get('blog_id')
            )

            db.session.add(new_comment)
            db.session.commit()

            return new_comment.to_dict(), 201
        
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400
        
        
        
class CommentEdit(Resource):
    def get(self, id):
        if 'user_id' not in session:
            return {'error': 'Not authorized'}, 401
        
        comment = Comment.query.get(id)
        if not comment:
            return {'error': 'Comment not found'}, 404
        
        if comment.user_id != session['user_id']:
            return {'error': 'Not authorized'}, 401
        
        return comment.to_dict(), 200
    
    def patch(self, id):
        if 'user_id' not in session:
            return {'error': 'Not authorized'}, 401
        
        comment = Comment.query.get(id)
        if not comment:
            return {'error': 'Comment not found'}, 404

        if comment.user_id != session['user_id']:
            return {'error': 'Not authorized'}, 401

        try:
            data = request.get_json()
            if not data:
                return {'error': 'No data provided'}, 400

            if 'comment' in data:
                comment.title = data['comment']     
            
            db.session.commit()

            return comment.to_dict(), 200
        
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400
        
    def delete(self, id):
        if 'user_id' not in session:
            return {'error': 'Not authroized'}, 401
        
        comment = Comment.query.get(id)
        if not comment:
            return {'error': 'comment not found'}, 404
        
        if comment.user_id != session['user_id']:
            return {'error': 'Not authorized'}, 403
        
        try:
            db.session.delete(comment)
            db.session.commit()
            return {}, 204
        
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 400
        

api.add_resource(BlogList, '/blogs')
api.add_resource(BlogEdit, '/blogs/<int:id>')
api.add_resource(CommentList, '/comments')
api.add_resource(CommentEdit, '/comments/<int:id>')

if __name__ == '__main__':
    app.run(debug=True, port=5555)
        




