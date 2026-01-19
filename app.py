from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
import json
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# --------------------
# LOAD ENV VARIABLES
# --------------------
load_dotenv()

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
FROM_EMAIL = os.environ.get("FROM_EMAIL")  # must be verified in SendGrid

# --------------------
# APP SETUP
# --------------------
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fallback-secret-key")

# --------------------
# ROUTES
# --------------------

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

            # Email to yourself
            email_body = f"""
New Portfolio Inquiry 🚀

Name: {name}
Email: {email}
Service: {service}

Message:
{message}
"""

            mail = Mail(
                from_email=FROM_EMAIL,
                to_emails=FROM_EMAIL,
                subject=f"New Inquiry: {service}",
                plain_text_content=email_body,
            )
            mail.reply_to = email

            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(mail)
            print("SENDGRID RESPONSE STATUS:", response.status_code)

            # Confirmation email to user
            confirmation = Mail(
                from_email=FROM_EMAIL,
                to_emails=email,
                subject="Thanks for contacting Wira!",
                plain_text_content=f"Hi {name},\n\nThanks for reaching out about {service}. I'll get back to you soon!\n\n— Wira"
            )
            sg.send(confirmation)

            flash("Thank you! Your message has been sent successfully.")
            return redirect(url_for("contact"))

        except Exception as e:
            import traceback
            print("SENDGRID ERROR:", traceback.format_exc())
            flash("Something went wrong. Please try again later.")
            return redirect(url_for("contact"))

    return render_template("contact.html")


@app.route("/api/projects")
def projects():
    with open("data/projects.json", encoding="utf-8") as f:
        return jsonify(json.load(f))


# --------------------
# RUN SERVER
# --------------------
if __name__ == "__main__":
    app.run(debug=True)
