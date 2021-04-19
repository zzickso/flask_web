from flask import Flask , render_template


app = Flask(__name__)

app.debug = True

@app.route('/', methods=['GET'])
def home():
    # return "Hello World"
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html", hello = "Gary Kim")

@app.route('/articles')
def articles():
    return render_template("articles.html", hello = "Gary Kim")

if __name__ == '__main__':
    app.run()