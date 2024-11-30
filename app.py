import os
import random
import string
import time
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# In-memory storage for blogs
blogs = {}


def generate_random_name():
    """Generate a random username."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


@app.route("/")
def home():
    """Serve the homepage."""
    username = generate_random_name()
    return render_template("index.html", username=username)


@app.route("/get_blogs", methods=["GET"])
def get_blogs():
    """Retrieve all blogs."""
    return jsonify(blogs)


@app.route("/post_blog", methods=["POST"])
def post_blog():
    """Handle new blog posts."""
    data = request.json
    blog_id = ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=8))
    blogs[blog_id] = {
        "author": data["author"],
        "content": data["content"],
        "image": data["image"],
        "replies": [],
        "timestamp": time.time(),
    }
    return jsonify({"success": True, "blog_id": blog_id, "blog": blogs[blog_id]})


@app.route("/post_reply", methods=["POST"])
def post_reply():
    """Handle new replies to blogs."""
    data = request.json
    blog_id = data["blog_id"]
    if blog_id in blogs:
        reply = {
            "author": data["author"],
            "content": data["content"],
            "timestamp": time.time(),
        }
        blogs[blog_id]["replies"].append(reply)
        return jsonify({"success": True, "reply": reply})
    return jsonify({"success": False, "error": "Blog not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
