from flask import Flask, render_template, request, redirect, session
from models.models import db, Admin, Student, Company
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "placement_secret"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def home():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]
        user_type = request.form["type"]

        if user_type == "admin":
            user = Admin.query.filter_by(username=email).first()

        elif user_type == "student":
            user = Student.query.filter_by(email=email).first()

        else:
            user = Company.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            session["id"] = user.id
            session["type"] = user_type

            if user_type == "admin":
                return redirect("/admin_dashboard")

            if user_type == "student":
                return redirect("/student_dashboard")

            if user_type == "company":
                return redirect("/company_dashboard")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        student = Student(name=name, email=email, password=password)

        db.session.add(student)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


@app.route("/admin_dashboard")
def admin_dashboard():

    if session.get("type") != "admin":
        return redirect("/login")

    return render_template("admin_dashboard.html")


@app.route("/student_dashboard")
def student_dashboard():

    if session.get("type") != "student":
        return redirect("/login")

    return render_template("student_dashboard.html")


@app.route("/company_dashboard")
def company_dashboard():

    if session.get("type") != "company":
        return redirect("/login")

    return render_template("company_dashboard.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        admin = Admin.query.first()

        if not admin:
            admin = Admin(
                username="admin",
                password=generate_password_hash("admin123")
            )
            db.session.add(admin)
            db.session.commit()

    app.run(debug=True)