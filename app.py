from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
import json
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email

# --------------------
# LOAD ENV VARIABLES
# --------------------
load_dotenv()

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
FROM_EMAIL = os.environ.get("FROM_EMAIL")
SECRET_KEY = os.environ.get("SECRET_KEY")

# Fail fast in production if critical env vars missing
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set")

# --------------------
# APP SETUP
# --------------------
app = Flask(__name__)
app.secret_key = SECRET_KEY

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
            if not SENDGRID_API_KEY or not FROM_EMAIL:
                raise RuntimeError("SendGrid configuration missing")

            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()
            service = request.form.get("service", "").strip()
            message = request.form.get("message", "").strip()

            if not name or not email or not message:
                flash("Please fill in all required fields.")
                return redirect(url_for("contact"))

            email_body = f"""
New Portfolio Inquiry

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

            # Proper reply-to handling
            mail.reply_to = Email(email)

            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(mail)

            print("SENDGRID STATUS:", response.status_code)

            if 200 <= response.status_code < 300:
                flash("Thank you! Your message has been sent successfully.")
            else:
                flash("Email failed to send. Please try again later.")

            return redirect(url_for("contact"))

        except Exception as e:
            import traceback
            print("SENDGRID ERROR:", traceback.format_exc())
            flash("Something went wrong. Please try again later.")
            return redirect(url_for("contact"))

    return render_template("contact.html")


@app.route("/api/projects")
def projects():
    try:
        projects_path = os.path.join(BASE_DIR, "data", "projects.json")
        with open(projects_path, encoding="utf-8") as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": "Unable to load projects"}), 500


@app.route("/health")
def health():
    return {"status": "ok"}, 200


# --------------------
# RUN SERVER (Local Dev Only)
# --------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)