
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

MONGO_URI = "mongodb+srv://testuser:testpassword123@cluster0.7igmtqz.mongodb.net/?appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["expense_db"]
collection = db["expenses"]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        expense = {
            "amount": float(request.form["amount"]),
            "category": request.form["category"],
            "date": datetime.now()
        }
        collection.insert_one(expense)
        return redirect("/")

    expenses = list(collection.find().sort("date", -1))

    # ✅ TOTAL EXPENSE CALCULATION
    total_expense = sum(expense["amount"] for expense in expenses)

    return render_template(
        "index.html",
        expenses=expenses,
        total=total_expense
    )

if __name__ == "__main__":
    app.run(debug=True)
