from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import tempfile
import threading
import time
import uuid

app = Flask(__name__)

# Temporary storage for blogs
blogs = []
images_dir = tempfile.mkdtemp()

# Function to delete blogs and images after 24 hours


def cleanup():
    global blogs
    current_time = time.time()
    blogs = [blog for blog in blogs if current_time - blog['timestamp'] < 86400]

    for file in os.listdir(images_dir):
        file_path = os.path.join(images_dir, file)
        if current_time - os.path.getmtime(file_path) > 86400:
            os.remove(file_path)

    threading.Timer(3600, cleanup).start()


# Start the cleanup function
cleanup()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/blogs', methods=['GET', 'POST'])
def handle_blogs():
    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        image = request.files.get('image')
        username = request.form.get('username', 'Anonymous')

        # Validate content
        if not content and not image:
            return jsonify({'error': 'Blog content or an image is required!'}), 400

        image_filename = None
        if image:
            image_filename = f"{uuid.uuid4()}_{image.filename}"
            image.save(os.path.join(images_dir, image_filename))

        blogs.append({
            'id': str(uuid.uuid4()),
            'username': username,
            'content': content,
            'image': image_filename,
            'replies': [],
            'timestamp': time.time()
        })

        return jsonify({'message': 'Blog created successfully!'}), 201

    return jsonify(blogs)


@app.route('/blogs/<blog_id>/reply', methods=['POST'])
def handle_replies(blog_id):
    username = request.form.get('username', 'Anonymous')
    reply_content = request.form.get('content', '').strip()

    # Validate reply content
    if not reply_content:
        return jsonify({'error': 'Reply content is required!'}), 400

    for blog in blogs:
        if blog['id'] == blog_id:
            blog['replies'].append({
                'username': username,
                'content': reply_content,
                'timestamp': time.time()
            })
            return jsonify({'message': 'Reply added successfully!'}), 201

    return jsonify({'error': 'Blog not found!'}), 404


@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(images_dir, filename)


if __name__ == '__main__':
    app.run(debug=True)
