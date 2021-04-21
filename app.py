from flask import Flask , render_template, request, redirect
from data import Articles
import pymysql

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
    cursor = db.cursor()
    # return "Hello World"
    return render_template("home.html")

@app.route('/about')
def about():
    cursor = db.cursor()
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
        sql = 'UPDATE topic SET title = %s, body = %s WHERE id = {};'.format(id)
        input_data = [title, desc]
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


if __name__ == '__main__':
    app.run()