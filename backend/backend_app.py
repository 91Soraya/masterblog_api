from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def create_id():
    """Create a new unique id for a new post"""
    all_ids = []
    for post in POSTS:
        all_ids.append(post["id"])
    return max(all_ids) + 1


def create_new_post():
    """Create a new blog post"""
    new_id = create_id()
    new_post = request.get_json()
    new_post["id"] = new_id
    return new_post


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    """GET or POST blog posts"""
    if request.method == "GET":
        sorting_method = request.args.get("sort")
        sorting_direction = request.args.get("direction")

        if sorting_method and sorting_direction:
            if sorting_method == "title" or sorting_method == "content":
                if sorting_direction == "asc":
                    return jsonify(sorted(POSTS, key=lambda x: x[sorting_method]))
                if sorting_direction == "desc":
                    return jsonify(sorted(POSTS, key=lambda x: x[sorting_method], reverse=True))

        if sorting_method != "title":
            return "Invalid sorting method", 400
        if sorting_direction != "content":
            return "Invalid sorting direction", 400

    if request.method == "POST":
        post_to_add = create_new_post()
        if len(post_to_add["title"]) < 1 and len(post_to_add["content"]) < 1:
            error_detail = "Both title and content are missing."
            return jsonify(error_detail), 400
        elif len(post_to_add["title"]) < 1:
            error_detail = "Title is missing"
            return jsonify(error_detail), 400
        elif len(post_to_add["content"]) < 1:
            error_detail = "Content is missing"
            return jsonify(error_detail), 400
        print(post_to_add)
        POSTS.append(post_to_add)
        return jsonify(POSTS), 201

    return jsonify(POSTS)


@app.route("/api/posts/<blog_id>", methods=["DELETE"])
def delete_post(blog_id):
    """Delete blog post"""
    for post in POSTS:
        if post["id"] == int(blog_id):
            POSTS.remove(post)
            message = jsonify({"message": f"Post with id {blog_id} has been deleted successfully."})
            return message, 200

        return "Post not found", 404


@app.route("/api/posts/<blog_id>", methods=["PUT"])
def update_post(blog_id):
    """Update a blog´s title or content"""
    data = request.get_json()
    for post in POSTS:
        if post["id"] == int(blog_id):
            if data["title"]:
                post["title"] = data["title"]
            if data["content"]:
                post["content"] = data["content"]
            return jsonify(post), 200
    return "Not found", 404


@app.route("/api/posts/search", methods=["GET"])
def search():
    """Gets a string to find in title or content and returns all posts with this string"""
    posts_found = []
    # noinspection PyBroadException
    try:
        search_title = request.args.get("title")
        for post in POSTS:
            if search_title in post["title"]:
                posts_found.append(post)
    except Exception:
        pass
    try:
        search_content = request.args.get("content")
        for post in POSTS:
            if search_content in post["content"]:
                posts_found.append(post)
    except Exception:
        pass

    return jsonify(posts_found)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
