
from flask import Flask, render_template, request, jsonify
import secrets
import string

# Create Flask Application
app = Flask(__name__)


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Secure Password Generator API
@app.route("/api/generate", methods=["POST"])
def generate_password():

    try:

        # Receive data from JavaScript
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "error": "Invalid request data"
            }), 400

        length = data.get("length", 16)

        # Validate password length
        if type(length) is not int or not 8 <= length <= 32:
            return jsonify({
                "error": "Password length must be between 8 and 32"
            }), 400

        # Character groups
        character_groups = []

        if data.get("uppercase") is True:
            character_groups.append(string.ascii_uppercase)

        if data.get("lowercase") is True:
            character_groups.append(string.ascii_lowercase)

        if data.get("numbers") is True:
            character_groups.append(string.digits)

        if data.get("symbols") is True:
            character_groups.append("!@#$%^&*()_+-=")

        # Check selection
        if not character_groups:
            return jsonify({
                "error": "Select at least one character type"
            }), 400

        if length < len(character_groups):
            return jsonify({
                "error": "Length is too short for selected options"
            }), 400

        # Add one character from each selected group
        password_chars = [
            secrets.choice(group)
            for group in character_groups
        ]

        # Combine all selected characters
        all_characters = "".join(character_groups)

        # Fill remaining password length
        while len(password_chars) < length:

            password_chars.append(
                secrets.choice(all_characters)
            )

        # Securely shuffle characters
        secrets.SystemRandom().shuffle(password_chars)

        # Final password
        password = "".join(password_chars)

        return jsonify({
            "password": password,
            "length": len(password),
            "message": "Password generated successfully"
        })

    except Exception:
        return jsonify({
            "error": "Password generation failed"
        }), 500


# Run Flask Server
if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
