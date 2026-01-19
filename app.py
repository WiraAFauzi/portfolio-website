from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
import json
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "super-secret-key"

GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_PASS = os.environ.get("GMAIL_PASS")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            service = request.form["service"]
            message = request.form["message"]

            msg = EmailMessage()
            msg["Subject"] = f"New Inquiry: {service}"
            msg["From"] = GMAIL_USER              # MUST be your Gmail
            msg["To"] = GMAIL_USER
            msg["Reply-To"] = email               # User email goes here

            msg.set_content(f"""
Name: {name}
Email: {email}
Service: {service}

Message:
{message}
""")

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(GMAIL_USER, GMAIL_PASS)
                smtp.send_message(msg)

            flash("Thank you! Your message has been sent successfully.")
            return redirect(url_for("contact"))

        except Exception as e:
            print("EMAIL ERROR:", e)
            flash("Something went wrong. Please try again later.")
            return redirect(url_for("contact"))

    return render_template("contact.html")

@app.route("/api/projects")
def projects():
    with open("data/projects.json", encoding="utf-8") as f:
        return jsonify(json.load(f))


if __name__ == "__main__":
    app.run(debug=True)
