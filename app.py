from flask import Flask, redirect, render_template, request, session 
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash

from others import login_required
from datetime import timedelta

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


db = SQL("sqlite:///data.db")

@app.route("/", methods=["GET","POST"])
@login_required
def home():
    if request.method == "GET":
        amount = db.execute("SELECT amount FROM users WHERE id = ?",session["user_id"])[0]["amount"]
        holds = db.execute("""
                                SELECT l.*, h.quantity
                                FROM live l
                                LEFT JOIN holdings h ON l.symbol = h.symbol
                                WHERE h.uid = ?
                            """, session["user_id"])

        ltp_balance = sum(stock['quantity'] * stock['ltp'] for stock in holds)
        pcp = sum(stock['quantity'] * stock['p_close'] for stock in holds)
        return render_template("index.html",inHome= True, amt = amount,pcp_balance=pcp,ltp_balance=ltp_balance,holdings = holds)

@app.route("/login", methods=["GET","POST"])
def login():

     # Forget any user_id
    session.clear()

    if request.method == "POST":
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("uName"))

        if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], request.form.get("pass")):
            return render_template("login.html",show_alert=True, alert_message="Password Not Match !")
        else:
            session["user_id"] = rows[0]["id"]
            if request.form.get("remember"):
                session.permanent = True  
                app.permanent_session_lifetime = timedelta(days=30)  
            else:
                session.permanent = False 

            
            return redirect("/")     
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        row = db.execute("SELECT * FROM users WHERE username = ?",request.form.get("uName"))

        if not request.form.get("name"):
            return  render_template("signup.html",show_alert=True, alert_message="Name is blank !")
        elif not request.form.get("uName"):
            return  render_template("signup.html",show_alert=True, alert_message="User name is blank !")
        elif not request.form.get("email"):
            return  render_template("signup.html",show_alert=True, alert_message="email is blank !")
        elif not request.form.get("number"):
            return  render_template("signup.html",show_alert=True, alert_message="Number is blank !")
        elif request.form.get("pass") != request.form.get("repass"):
            return  render_template("signup.html",show_alert=True, alert_message="Passwords doesnot match !")
        elif len(row) == 1:
            return  render_template("signup.html",show_alert=True, alert_message="User Already exist !")
        else:
           db.execute("""
                INSERT INTO users (full_name, username, email, phone, password_hash)
                VALUES (?, ?, ?, ?, ?)
            """, 
            request.form.get("name"),
            request.form.get("uName"),
            request.form.get("email"),
            request.form.get("number"),
            generate_password_hash(request.form.get("pass"))
        )

        return  render_template("login.html",show_alert=True, alert_message="Registered successful !")
    else:
        return render_template("signup.html")
    
@app.route("/live", methods=["GET","POST"])
def live():
    if request.method == "GET":
        search = request.args.get("search", "")
        if search:
            rows = db.execute("SELECT * FROM live WHERE symbol LIKE :search", search=f"%{search}%")
        else:
            rows = db.execute("SELECT * FROM live")
        return render_template("live.html",loggedin = False, live = True,stocks=rows)
    



if __name__ == "__main__":
    app.run(debug=True)

