from flask import (
    Flask,
    render_template,
    flash,
    redirect,
    url_for,
    session,
    logging,
    request,
)
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps


# USER LOGIN DECORATOR
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first", "danger")
            return redirect(url_for("login"))

    return decorated_function


# USER REGISTRATION FORM
class RegisterForm(Form):
    name = StringField("Name", validators=[validators.Length(min=4, max=25)])
    surname = StringField("Surname", validators=[validators.Length(min=4, max=25)])
    nickname = StringField("Username", validators=[validators.Length(min=5, max=35)])
    position = StringField("Position", validators=[validators.Length(min=4, max=25)])
    mail = StringField(
        "Email Adress",
        validators=[validators.Email(message="Please enter a valid email.")],
    )
    password = PasswordField(
        "Password:",
        validators=[
            validators.DataRequired(message="Please set a password"),
            validators.EqualTo(
                fieldname="confirm", message="Your password does not match."
            ),
        ],
    )
    confirm = PasswordField("Confirm Password")


# SIGN IN FORM
class LoginForm(Form):
    username = StringField("Username")
    password = StringField("Password")


##############################################################################
app = Flask(__name__)
app.secret_key = "astrof"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "astrof"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

##############################################################################

# MAIN PAGE
@app.route("/")
def index():
    return render_template("index3.html")


# ABOUT US PAGE
@app.route("/about")
def about():
    return render_template("about.html")


# BLOG PAGE
@app.route("/dashboard")
@login_required
def dashboard():
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM games where author = %s"
    result = cursor.execute(query, (session["username"],))

    if result > 0:
        articles = cursor.fetchall()
        return render_template("dashboard.html", articles=articles)
    else:
        return render_template("dashboard.html")


# ARTICLE DETAILS
@app.route("/article/<string:id>")
def detail(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM games WHERE id = %s"
    result = cursor.execute(query, (id,))

    if result > 0:
        article = cursor.fetchone()
        return render_template("article.html", article=article)
    else:
        return render_template("article.html")


# ARTICLES PAGE
@app.route("/articles")
def articles():
    cursor = mysql.connection.cursor()

    query = "SELECT * FROM games"
    result = cursor.execute(query)
    if result > 0:
        articles = cursor.fetchall()
        return render_template("articles.html", articles=articles)
    else:
        return render_template("articles.html")


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.nickname.data
        email = form.mail.data
        password = sha256_crypt.encrypt(form.password.data)

        cursor = mysql.connection.cursor()

        query = (
            "INSERT INTO users(name, username, email, password) VALUES(%s, %s, %s, %s)"
        )
        cursor.execute(query, (name, username, email, password))
        mysql.connection.commit()

        cursor.close()
        flash("Register Successful", "success")

        return redirect(url_for("login"))
    else:
        return render_template("register.html", form=form)


# SIGN IN
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password = form.password.data

        cursor = mysql.connection.cursor()
        query = "SELECT * FROM users WHERE username = %s"

        result = cursor.execute(query, (username,))

        if result > 0:
            data = cursor.fetchone()
            real_password = data["password"]
            if sha256_crypt.verify(password, real_password):
                flash("Login Successful", "success")
                session["logged_in"] = True
                session["username"] = username

                return redirect(url_for("index"))
            else:
                flash("Wrong Password", "danger")
                return redirect(url_for("login"))
        else:
            flash("User not found", "danger")
            return redirect(url_for("login"))

    return render_template("login.html", form=form)


# LOG OUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# DELETE ARTICLE
@app.route("/delete/<string:id>")
@login_required
def delete(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM games WHERE author = %s and id = %s"
    result = cursor.execute(query, (session["username"], id))
    if result > 0:
        query2 = "DELETE FROM games WHERE id = %s"
        cursor.execute(query2, (id,))
        mysql.connection.commit()

        return redirect(url_for("dashboard"))
    else:
        flash("You are not authorized for this action", "danger")
        return redirect(url_for("index"))


# UPDATE ARTICLE
@app.route("/edit/<string:id>", methods=["GET", "POST"])
@login_required
def update(id):
    if request.method == "GET":
        cursor = mysql.connection.cursor()

        query = "SELECT * FROM games WHERE id = %s and author = %s"
        result = cursor.execute(query, (id, session["username"]))

        if result == 0:
            flash("There is no article with this id", "danger")
            return redirect(url_for("index"))
        else:
            article = cursor.fetchone()
            form = ArticleForm()

            form.title.data = article["title"]
            form.content.data = article["content"]
            return render_template("update.html", form=form)
    else:  # POST REQUEST
        form = ArticleForm(request.form)

        newTitle = form.title.data
        newContent = form.content.data

        query2 = "UPDATE games SET title = %s, content = %s WHERE id = %s"
        cursor = mysql.connection.cursor()
        cursor.execute(query2, (newTitle, newContent, id))
        mysql.connection.commit()

        flash("Article Updated", "success")

        return redirect(url_for("dashboard"))


# ADD ARTICLE
@app.route("/addarticle", methods=["GET", "POST"])
def addarticle():
    form = ArticleForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        content = form.content.data

        cursor = mysql.connection.cursor()
        query = "INSERT INTO games(title, author,content) VALUES(%s, %s, %s)"
        cursor.execute(query, (title, session["username"], content))

        mysql.connection.commit()
        cursor.close()

        flash("Article Added Successfully", "success")

        return redirect(url_for("dashboard"))

    return render_template("addarticle.html", form=form)


# ARTICLE FORM CLASS
class ArticleForm(Form):
    title = StringField("Game Name", validators=[validators.Length(min=4, max=25)])
    content = TextAreaField("Content", validators=[validators.Length(min=20)])


# SEARCH
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return redirect(url_for("index"))
    else:
        keyword = request.form.get("keyword")

        cursor = mysql.connection.cursor()
        query = "SELECT * FROM games WHERE title LIKE '%" + keyword + "%'"
        result = cursor.execute(query)

        if result == 0:
            flash("No Articles Found", "warning")
            return redirect(url_for("games"))
        else:
            articles = cursor.fetchall()
            return render_template("articles.html", articles=articles)


if __name__ == "__main__":  # For running the app
    app.run(debug=True)
