from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog Post ' + str(self.id)

all_posts = [
    {
        'title': 'Post 1',
        'content': 'this is the content of post 1.laaalalalaalala.'
    },
    {
        'title': 'Post 2',
        'content': 'this is the content of post 2.laaalalalaalala'
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts', methods=['GET','POST'])
def posts():
    if request.method == "POST":
        post_title = request.form['title']
        post_content = request.form['content']
        new_post = BlogPost(title=post_title, content=post_content)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
    return render_template('posts.html', posts=all_posts)

@app.route('/home/<int:id>')
def hello(id):
    return 'hello, ' + str(id)

@app.route('/onlyget', methods=['GET'])
def get_req():
    return 'you can only get this webpage.1'

if __name__=='__main__':
    app.run(debug=True)
