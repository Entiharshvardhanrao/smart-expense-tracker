from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# -------------------- DATABASE CONFIG --------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expense.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -------------------- MODEL --------------------
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# -------------------- HOME --------------------

@app.route("/")
def home():
    expenses = Expense.query.all()
    total = sum(exp.amount for exp in expenses)

    # category-wise total
    category_data = {}
    for exp in expenses:
        if exp.category in category_data:
            category_data[exp.category] += exp.amount
        else:
            category_data[exp.category] = exp.amount

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        category_data=category_data
    )

# -------------------- ADD EXPENSE --------------------
@app.route("/add", methods=["POST"])
def add_expense():
    amount = request.form["amount"]
    category = request.form["category"]

    new_expense = Expense(
        amount=float(amount),
        category=category
    )

    db.session.add(new_expense)
    db.session.commit()

    return redirect(url_for("home"))

# -------------------- DELETE EXPENSE --------------------
@app.route("/delete/<int:id>")
def delete_expense(id):
    expense = Expense.query.get(id)
    if expense:
        db.session.delete(expense)
        db.session.commit()
    return redirect(url_for("home"))

# -------------------- RUN APP --------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
