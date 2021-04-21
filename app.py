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
    curssor = db.cursor()
    # return "Hello World"
    return render_template("home.html")

@app.route('/about')
def about():
    curssor = db.cursor()
    return render_template("about.html", hello = "Gary Kim")

@app.route('/articles')
def articles():
    curssor = db.cursor()
    sql = 'select * from topic;'
    curssor.execute(sql)
    topics = curssor.fetchall()
    print(topics)
    # articles = Articles()
    # print(articles[0]['title'])
    return render_template("articles.html", articles = topics)

@app.route('/article/<int:id>')
def article(id):
    curssor = db.cursor()
    sql = 'select * from topic WHERE id={};'.format(id)
    curssor.execute(sql)
    topic = curssor.fetchone()
    print(topic)
    #articles = Articles()
    #article = articles[id-1]
    #print(articles[id-1])
    return render_template("article.html", article = topic) 

@app.route('/add_articles', methods = ["GET", "POST"])
def add_articles():
    curssor = db.cursor()
    if request.method == "POST":
        desc = request.form['desc']
        author = request.form['author']
        title = request.form['title']

        sql_1 = "INSERT INTO `topic` (`title`, `body`, `author`) VALUES (%s, %s, %s);"
        input_data = [title,desc,author]

        curssor.execute(sql_1, input_data)
        db.commit()
        print(curssor.rowcount)
        #db.close()

        return redirect("/articles")
    else:
        return render_template("add_articles.html")
    #return "<h1>글쓰기 페이지</h1>"

@app.route('/delete/<int:id>' , methods=['POST'])
def delete(id):
    curssor = db.cursor()
    sql = 'DELETE FROM topic WHERE id= %s;'
    id = [id]
    curssor.execute(sql, id)
    db.commit()
    return redirect("/articles")

@app.route('/edit/<int:id>', methods=["POST", "GET"])
def edit(id):
    cursor = db.cursor()
    if request.method == "POST":
        return "Success"

    else:
        sql = "SELECT * FROM topic WHERE id = {}".format(id)
        cursor.execute(sql)
        topic = cursor.fetchone()
        print(topic[1])
        return render_template("edit_article.html", article = topic)


if __name__ == '__main__':
    app.run()