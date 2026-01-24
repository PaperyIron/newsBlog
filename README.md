# newsBlog
newsBlog is a website that is designed to give people a more in depth view on news articles.  Users are able to create, edit, and comment on any blog within the site.  Every post requires a title, body, and url so that users can view the source article.  

# To Run
1. Clone this git repository to your local machine.  
2. Open a terminal window and cd into the 'news_blog_frontend' folder.
3. Run 'npm install' to install all required packages.
4. Run 'npm run dev' to start the front end of the application.
5. Follow the link provided in the terminal or goto 'http://localhost:5173/' to view the front-end.
6. Open a second terminal window.
7. Run 'pipenv shell' to start a virtual environment.
8. Run 'pipenv install' or 'pip3 install requirements.txt' to install all required dependencies.
9. CD into the 'server' folder.
10. Run 'python app.py' to start the server.
11. The database is empty at the start.  If you would like to seed the database with example data, run 'python seed.py'.

Now the full app is running.  Login in with an example user, or signup to add your own credentials to the database. The homepage lists all the blogs posted.  Click on a blog to open up the full text and view comments or add your own comment.  You can edit a blog by selecting your blog from the homepage. 

For future upgrades, I would like to add the ability to preview the news article from the homepage so that users can see the title of the article and then read the blog post. I would also like to include a reliablility meter so that users can see the amount of bias in a blog post. I think the best way to implement that would be an AI of some sort or a keyword finder that highlights typically biased words.
