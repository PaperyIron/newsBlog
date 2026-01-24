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
            title='Lorem Ipsum Dolor Sit Amet Consectetur',
            body_text='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.',
            url='https://www.example.com/lorem-ipsum-1',
            user_id=user1.id
        )

        blog2 = Blog(
            title='Vestibulum Ante Ipsum Primis Faucibus',
            body_text='Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae. Donec velit neque, auctor sit amet aliquam vel, ullamcorper sit amet ligula. Curabitur non nulla sit amet nisl tempus convallis quis ac lectus. Pellentesque in ipsum id orci porta dapibus. Vivamus magna justo, lacinia eget consectetur sed, convallis at tellus.',
            url='https://www.example.com/vestibulum-ante',
            user_id=user1.id
        )

        blog3 = Blog(
            title='Praesent Sapien Massa Convallis Pellentesque',
            body_text='Praesent sapien massa, convallis a pellentesque nec, egestas non nisi. Nulla porttitor accumsan tincidunt. Mauris blandit aliquet elit, eget tincidunt nibh pulvinar a. Cras ultricies ligula sed magna dictum porta. Vivamus suscipit tortor eget felis porttitor volutpat. Sed porttitor lectus nibh. Donec sollicitudin molestie malesuada proin eget.',
            url='https://www.techblog.com/praesent-sapien',
            user_id=user2.id
        )

        blog4 = Blog(
            title='Quisque Velit Nisi Pretium Ut Lacinia',
            body_text='Quisque velit nisi, pretium ut lacinia in, elementum id enim. Curabitur arcu erat, accumsan id imperdiet et, porttitor at sem. Vivamus magna justo, lacinia eget consectetur sed, convallis at tellus. Curabitur aliquet quam id dui posuere blandit. Nulla quis lorem ut libero malesuada feugiat. Pellentesque in ipsum id orci porta dapibus in magna.',
            url='https://www.devnotes.com/quisque-velit',
            user_id=user2.id
        )

        blog5 = Blog(
            title='Sed Porttitor Lectus Nibh Donec Rutrum',
            body_text='Sed porttitor lectus nibh. Donec rutrum congue leo eget malesuada. Vestibulum ac diam sit amet quam vehicula elementum sed sit amet dui. Proin eget tortor risus. Curabitur non nulla sit amet nisl tempus convallis quis ac lectus. Vivamus suscipit tortor eget felis porttitor volutpat. Mauris blandit aliquet elit eget tincidunt nibh pulvinar.',
            url='https://www.securityblog.com/sed-porttitor',
            user_id=user3.id
        )

        blog6 = Blog(
            title='Nulla Porttitor Accumsan Tincidunt Mauris',
            body_text='Nulla porttitor accumsan tincidunt. Mauris blandit aliquet elit, eget tincidunt nibh pulvinar a. Vivamus magna justo, lacinia eget consectetur sed. Pellentesque in ipsum id orci porta dapibus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae. Donec velit neque auctor sit amet aliquam vel ullamcorper.',
            url='https://www.pythonpatterns.com/nulla-porttitor',
            user_id=user3.id
        )

        blog7 = Blog(
            title='Curabitur Aliquet Quam Id Dui Posuere',
            body_text='Curabitur aliquet quam id dui posuere blandit. Vestibulum ac diam sit amet quam vehicula elementum sed sit amet dui. Donec sollicitudin molestie malesuada. Vivamus suscipit tortor eget felis porttitor volutpat. Curabitur non nulla sit amet nisl tempus convallis quis ac lectus. Sed porttitor lectus nibh donec rutrum congue leo eget malesuada.',
            url='https://www.testingpython.com/curabitur-aliquet',
            user_id=user4.id
        )

        blog8 = Blog(
            title='Vivamus Magna Justo Lacinia Eget Consectetur',
            body_text='Vivamus magna justo, lacinia eget consectetur sed, convallis at tellus. Quisque velit nisi, pretium ut lacinia in, elementum id enim. Curabitur arcu erat, accumsan id imperdiet et, porttitor at sem. Proin eget tortor risus. Donec rutrum congue leo eget malesuada. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia.',
            url='https://www.deployguide.com/vivamus-magna',
            user_id=user4.id
        )

        db.session.add_all([blog1, blog2, blog3, blog4, blog5, blog6, blog7, blog8])
        db.session.commit()

        print("Creating comments...")
        comment1 = Comment(
            comment='Lorem ipsum dolor sit amet, consectetur adipiscing elit sed do eiusmod tempor.',
            user_id=user2.id,
            blog_id=blog1.id
        )

        comment2 = Comment(
            comment='Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae.',
            user_id=user3.id,
            blog_id=blog1.id
        )

        comment3 = Comment(
            comment='Praesent sapien massa, convallis a pellentesque nec, egestas non nisi porttitor.',
            user_id=user4.id,
            blog_id=blog2.id
        )

        comment4 = Comment(
            comment='Curabitur non nulla sit amet nisl tempus convallis quis ac lectus vivamus.',
            user_id=user1.id,
            blog_id=blog2.id
        )

        comment5 = Comment(
            comment='Mauris blandit aliquet elit, eget tincidunt nibh pulvinar a cras ultricies ligula.',
            user_id=user1.id,
            blog_id=blog3.id
        )

        comment6 = Comment(
            comment='Quisque velit nisi, pretium ut lacinia in, elementum id enim curabitur arcu erat.',
            user_id=user4.id,
            blog_id=blog3.id
        )

        comment7 = Comment(
            comment='Sed porttitor lectus nibh donec rutrum congue leo eget malesuada vestibulum.',
            user_id=user3.id,
            blog_id=blog4.id
        )

        comment8 = Comment(
            comment='Nulla porttitor accumsan tincidunt mauris blandit aliquet elit eget tincidunt.',
            user_id=user2.id,
            blog_id=blog5.id
        )

        comment9 = Comment(
            comment='Vivamus suscipit tortor eget felis porttitor volutpat curabitur aliquet quam id.',
            user_id=user4.id,
            blog_id=blog5.id
        )

        comment10 = Comment(
            comment='Pellentesque in ipsum id orci porta dapibus vestibulum ac diam sit amet quam.',
            user_id=user1.id,
            blog_id=blog6.id
        )

        comment11 = Comment(
            comment='Donec sollicitudin molestie malesuada proin eget tortor risus curabitur non nulla.',
            user_id=user2.id,
            blog_id=blog6.id
        )

        comment12 = Comment(
            comment='Curabitur arcu erat, accumsan id imperdiet et, porttitor at sem vivamus magna.',
            user_id=user3.id,
            blog_id=blog7.id
        )

        comment13 = Comment(
            comment='Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia.',
            user_id=user1.id,
            blog_id=blog7.id
        )

        comment14 = Comment(
            comment='Sed porttitor lectus nibh donec rutrum congue leo eget malesuada vestibulum ac.',
            user_id=user2.id,
            blog_id=blog8.id
        )

        comment15 = Comment(
            comment='Nulla quis lorem ut libero malesuada feugiat pellentesque in ipsum id orci porta.',
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
        
        print("\nSample login credentials:")
        print("Username: alice_tech | Password: password123")
        print("Username: bob_writes | Password: password123")
        print("Username: charlie_dev | Password: password123")
        print("Username: diana_blogger | Password: password123")

if __name__ == '__main__':
    seed_data()