from flask import Flask , render_template, request, redirect
from data import Articles
import pymysql
from passlib.hash import sha256_crypt

app = Flask(__name__)

app.debug = True

db = pymysql.connect(
  host='localhost',
  port = 3306,
  user = 'root',
  password = '1234',
  db = 'busan'
)


@app.route('/', methods=['GET'])
def home():
    # cursor = db.cursor()
    # return "Hello World"
    return render_template("home.html")

@app.route('/about')
def about():
    # cursor = db.cursor()
    return render_template("about.html", hello = "Gary Kim")

@app.route('/articles')
def articles():
    cursor = db.cursor()
    sql = 'select * from topic;'
    cursor.execute(sql)
    topics = cursor.fetchall()
    #print(topics)
    # articles = Articles()
    # print(articles[0]['title'])
    return render_template("articles.html", articles = topics)

@app.route('/article/<int:id>')
def article(id):
    cursor = db.cursor()
    sql = 'select * from topic WHERE id={};'.format(id)
    cursor.execute(sql)
    topic = cursor.fetchone()
    #print(topic)
    #articles = Articles()
    #article = articles[id-1]
    #print(articles[id-1])
    return render_template("article.html", article = topic) 

@app.route('/add_articles', methods = ["GET", "POST"])
def add_articles():
    cursor = db.cursor()
    if request.method == "POST":
        desc = request.form['desc']
        author = request.form['author']
        title = request.form['title']

        sql_1 = "INSERT INTO `topic` (`title`, `body`, `author`) VALUES (%s, %s, %s);"
        input_data = [title,desc,author]

        cursor.execute(sql_1, input_data)
        db.commit()
        #print(curssor.rowcount)
        #db.close()

        return redirect("/articles")
    else:
        return render_template("add_articles.html")
    #return "<h1>글쓰기 페이지</h1>"

@app.route('/delete/<int:id>' , methods=['POST'])
def delete(id):
    cursor = db.cursor()
    sql = 'DELETE FROM topic WHERE id= %s;'
    id = [id]
    cursor.execute(sql, id)
    db.commit()
    return redirect("/articles")

@app.route('/<int:id>/edit', methods=["POST", "GET"])
def edit(id):
    cursor = db.cursor()
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        author = request.form['author']
        sql = 'UPDATE topic SET title = %s, body = %s, author = %s WHERE id = {};'.format(id)
        input_data = [title, desc, author]
        cursor.execute(sql, input_data)
        db.commit()
        print(request.form['title'])
        return redirect("/articles")

    else:
        sql = "SELECT * FROM topic WHERE id = {}".format(id)
        cursor.execute(sql)
        topic = cursor.fetchone()
        #print(topic[1])
        return render_template("edit_article.html", article = topic)

@app.route('/register/', methods = ["GET", "POST"])
def register():
    cursor = db.cursor()
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        username =request.form['username']
        password = sha256_crypt.encrypt(request.form['password'])
        sql = "INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)"
        input_data = [name, email, username, password]
        cursor.execute(sql, input_data)
        db.commit()
        return redirect('/articles')
    else:
        return render_template("register.html")
        
@app.route('/login', methods = ["GET", "POST"])
def login():
    cursor = db.cursor()
    if request.method == "POST":
        usersname = request.form['username']
        password_1 = request.form['password']
        #print(password_1)
        #print(request.form['username'])
        sql = 'SELECT FROM users WHERE email = %s;'
        input_data = [usersname]
        cursor.execute(sql, input_data)
        password = cursor.fetchone()
        print(password[0])
        if sha256_crypt.verify(password_1, password[0]):
            return "SUCCESS" 
        else:
            return password[0]

if __name__ == '__main__':
    app.run()