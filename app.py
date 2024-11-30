import os
import random
import string
import time
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.secret_key = "blog_secret_key"

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


@app.route("/post_blog", methods=["POST"])
def post_blog():
    """Handle blog posting."""
    data = request.json
    blog_id = ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=8))
    blogs[blog_id] = {
        "author": data["author"],
        "content": data["content"],
        "image": data["image"],
        "replies": [],
        "timestamp": time.time()
    }
    return jsonify({"status": "success", "blog_id": blog_id})


@app.route("/reply", methods=["POST"])
def reply():
    """Handle replies to blogs."""
    data = request.json
    blog_id = data["blog_id"]
    if blog_id in blogs:
        reply_id = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=8))
        blogs[blog_id]["replies"].append({
            "author": data["author"],
            "content": data["content"],
            "timestamp": time.time()
        })
        return jsonify({"status": "success", "reply_id": reply_id})
    return jsonify({"status": "error", "message": "Blog not found"})


@app.route("/get_blogs", methods=["GET"])
def get_blogs():
    """Retrieve all blogs."""
    current_time = time.time()
    to_delete = []
    for blog_id, blog in blogs.items():
        # Delete blogs older than 24 hours
        if current_time - blog["timestamp"] > 86400:  # 24 hours in seconds
            to_delete.append(blog_id)
    for blog_id in to_delete:
        del blogs[blog_id]
    return jsonify(blogs)


if __name__ == "__main__":
    app.run(debug=True)
