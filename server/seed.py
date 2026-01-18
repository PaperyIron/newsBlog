from app import app
from config import db
from models import User, Blog, Comment

def seed_data():
    with app.app_context():
        print("Clearing existing data...")
        Comment.query.delete()
        Blog.query.delete()
        User.query.delete()
        db.session.commit()

        print("Creating users...")
        user1 = User(username='alice_tech')
        user1.password_hash = 'password123'
        
        user2 = User(username='bob_writes')
        user2.password_hash = 'password123'
        
        user3 = User(username='charlie_dev')
        user3.password_hash = 'password123'
        
        user4 = User(username='diana_blogger')
        user4.password_hash = 'password123'

        db.session.add_all([user1, user2, user3, user4])
        db.session.commit()

        print("Creating blogs...")
        blog1 = Blog(
            title='Getting Started with Python Flask',
            body_text='Flask is a lightweight and powerful web framework for Python. It provides the tools and libraries needed to build web applications quickly and efficiently. In this post, we will explore the basics of Flask and how to set up your first application.',
            url='https://www.example.com/flask-tutorial',
            user_id=user1.id
        )

        blog2 = Blog(
            title='Understanding SQLAlchemy ORM',
            body_text='SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives developers the full power and flexibility of SQL. It provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access.',
            url='https://www.example.com/sqlalchemy-guide',
            user_id=user1.id
        )

        blog3 = Blog(
            title='Building RESTful APIs with Flask-RESTful',
            body_text='Flask-RESTful is an extension for Flask that adds support for quickly building REST APIs. It encourages best practices with minimal setup. This tutorial will guide you through creating a complete REST API with proper HTTP methods and status codes.',
            url='https://www.techblog.com/flask-restful-apis',
            user_id=user2.id
        )

        blog4 = Blog(
            title='Database Migrations with Flask-Migrate',
            body_text='Flask-Migrate is an extension that handles SQLAlchemy database migrations for Flask applications using Alembic. It makes it easy to keep your database schema in sync with your models as your application evolves over time. Learn how to set up and use migrations effectively.',
            url='https://www.devnotes.com/flask-migrate-tutorial',
            user_id=user2.id
        )

        blog5 = Blog(
            title='Authentication and Authorization in Flask',
            body_text='Security is crucial in web applications. This comprehensive guide covers implementing user authentication and authorization in Flask applications. We will discuss password hashing, session management, and protecting routes from unauthorized access.',
            url='https://www.securityblog.com/flask-auth-guide',
            user_id=user3.id
        )

        blog6 = Blog(
            title='Best Practices for Flask Application Structure',
            body_text='As your Flask application grows, organizing your code becomes increasingly important. This article explores best practices for structuring larger Flask applications, including blueprints, application factory pattern, and separating concerns effectively.',
            url='https://www.pythonpatterns.com/flask-structure',
            user_id=user3.id
        )

        blog7 = Blog(
            title='Testing Flask Applications',
            body_text='Testing is an essential part of developing robust applications. Learn how to write unit tests and integration tests for your Flask applications using pytest. We will cover testing routes, database operations, and API endpoints to ensure your application works as expected.',
            url='https://www.testingpython.com/flask-testing',
            user_id=user4.id
        )

        blog8 = Blog(
            title='Deploying Flask Apps to Production',
            body_text='Moving from development to production requires careful planning and configuration. This guide covers deploying Flask applications using various platforms and tools, including Gunicorn, Nginx, Docker, and cloud platforms like Heroku and AWS.',
            url='https://www.deployguide.com/flask-production',
            user_id=user4.id
        )

        db.session.add_all([blog1, blog2, blog3, blog4, blog5, blog6, blog7, blog8])
        db.session.commit()

        print("Creating comments...")
        comment1 = Comment(
            comment='Great introduction! This really helped me understand Flask basics.',
            user_id=user2.id,
            blog_id=blog1.id
        )

        comment2 = Comment(
            comment='Thanks for sharing this. Do you have any tips for debugging Flask applications?',
            user_id=user3.id,
            blog_id=blog1.id
        )

        comment3 = Comment(
            comment='Very comprehensive guide. The examples are clear and easy to follow.',
            user_id=user4.id,
            blog_id=blog2.id
        )

        comment4 = Comment(
            comment='I was struggling with ORM concepts, but this post cleared things up for me.',
            user_id=user1.id,
            blog_id=blog2.id
        )

        comment5 = Comment(
            comment='Excellent tutorial! The step-by-step approach made it easy to implement.',
            user_id=user1.id,
            blog_id=blog3.id
        )

        comment6 = Comment(
            comment='Could you cover error handling in REST APIs in a follow-up post?',
            user_id=user4.id,
            blog_id=blog3.id
        )

        comment7 = Comment(
            comment='This saved me so much time! Migrations are much clearer now.',
            user_id=user3.id,
            blog_id=blog4.id
        )

        comment8 = Comment(
            comment='Really helpful article on authentication. Security is so important!',
            user_id=user2.id,
            blog_id=blog5.id
        )

        comment9 = Comment(
            comment='I implemented this in my project and it works perfectly. Thanks!',
            user_id=user4.id,
            blog_id=blog5.id
        )

        comment10 = Comment(
            comment='The blueprint pattern has made my code so much more organized.',
            user_id=user1.id,
            blog_id=blog6.id
        )

        comment11 = Comment(
            comment='Great insights on application structure. Very practical advice.',
            user_id=user2.id,
            blog_id=blog6.id
        )

        comment12 = Comment(
            comment='Testing has always intimidated me, but this makes it approachable.',
            user_id=user3.id,
            blog_id=blog7.id
        )

        comment13 = Comment(
            comment='The pytest examples are really useful. Looking forward to more testing content.',
            user_id=user1.id,
            blog_id=blog7.id
        )

        comment14 = Comment(
            comment='Just deployed my first Flask app using this guide. It went smoothly!',
            user_id=user2.id,
            blog_id=blog8.id
        )

        comment15 = Comment(
            comment='Very thorough deployment guide. The Docker section was particularly helpful.',
            user_id=user3.id,
            blog_id=blog8.id
        )

        db.session.add_all([
            comment1, comment2, comment3, comment4, comment5,
            comment6, comment7, comment8, comment9, comment10,
            comment11, comment12, comment13, comment14, comment15
        ])
        db.session.commit()

        print("Database seeded successfully!")
        print(f"Created {User.query.count()} users")
        print(f"Created {Blog.query.count()} blogs")
        print(f"Created {Comment.query.count()} comments")

if __name__ == '__main__':
    seed_data()