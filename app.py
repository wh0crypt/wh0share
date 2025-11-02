import os

from dotenv import load_dotenv
from flask import (
    Flask,
    Response,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

import utils

load_dotenv(".env")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
SITE_INDEX = os.getenv("SITE_INDEX", "/")
UPLOAD_FOLDER = os.path.abspath(os.getenv("UPLOAD_FOLDER", "./uploads"))
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
ALLOWED_EXTENSIONS = set(
    ext.strip().lower()
    for ext in os.getenv("ALLOWED_EXTENSIONS", "txt,pdf,png,jpg,jpeg,gif").split(",")
)
MAX_CONTENT_LENGTH_MB = int(os.getenv("MAX_CONTENT_LENGTH_MB", "1024").strip())
MAX_STORAGE_SIZE_MB = int(os.getenv("MAX_STORAGE_SIZE_MB", "10240").strip())
MAX_CONTENT_LENGTH = MAX_CONTENT_LENGTH_MB * 1024**2
MAX_STORAGE_SIZE_BYTES = MAX_STORAGE_SIZE_MB * 1024**2

check, disk_free_bytes = utils.check_available_storage(
    UPLOAD_FOLDER, MAX_STORAGE_SIZE_BYTES
)

if not check:
    raise ValueError(
        f"MAX_STORAGE_SIZE ({MAX_STORAGE_SIZE_MB} MB) exceeds available disk space "
        f"minus margin (available: {(disk_free_bytes)//(1024**2)} MB)."
    )

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH


@app.route(SITE_INDEX)
def index() -> str:
    """
    Render the main page with the list of uploaded files.

    Returns:
        str: HTML content for the index page.
    """

    files = os.listdir(app.config["UPLOAD_FOLDER"])
    used = utils.get_folder_size(app.config["UPLOAD_FOLDER"])
    free = max(MAX_STORAGE_SIZE_BYTES - used, 0)
    used_percent = round((used / MAX_STORAGE_SIZE_BYTES) * 100, 2)
    gb_divisor = 1024**3
    return render_template(
        "index.html",
        files=files,
        disk_used=round(used / gb_divisor, 2),
        disk_total=round(MAX_STORAGE_SIZE_BYTES / gb_divisor, 2),
        disk_free=round(free / gb_divisor, 2),
        used_percent=used_percent,
    )


@app.route("/upload", methods=["POST"])
def upload_file() -> Response:
    """
    Handle file uploads from the web interface.

    Validates the uploaded file type and flashes an error message if invalid.

    Returns:
        Response: Redirects to the index page after upload.
    """

    if "file" not in request.files:
        flash("No file part in the request", "error")
        return redirect(url_for("index"))

    file = request.files["file"]
    if not file or file.filename == "":
        flash("No file selected", "error")
        return redirect(url_for("index"))

    filename = secure_filename(file.filename)
    if not utils.allowed_file(file.filename, ALLOWED_EXTENSIONS):
        flash(
            f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}",
            "error",
        )
        return redirect(url_for("index"))

    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    if (
        utils.get_folder_size(app.config["UPLOAD_FOLDER"]) + file_size
        > MAX_STORAGE_SIZE_BYTES
    ):
        flash(
            f"Storage limit reached ({MAX_STORAGE_SIZE_MB} MB). Delete some files first.",
            "error",
        )
        return redirect(url_for("index"))

    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    flash(f"File '{filename}' uploaded successfully!", "success")
    return redirect(url_for("index"))


@app.route("/download/<filename>")
def download_file(filename: str) -> Response:
    """
    Serve a file for download.

    Args:
        filename (str): Name of the file to download.

    Returns:
        Response: Flask response to send the file as an attachment.
    """

    return send_from_directory(
        app.config["UPLOAD_FOLDER"], filename, as_attachment=True
    )


@app.route("/uploads/<filename>")
def view_file(filename: str) -> Response:
    """
    Serve a file for inline viewing in the browser.

    Args:
        filename (str): Name of the file to serve.

    Returns:
        Response: Flask response to send the file.
    """

    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename: str) -> Response:
    """
    Handle file deletion requests.

    Args:
        filename (str): Name of the file to delete.

    Returns:
        Response: Redirects to the index page after deletion.
    """

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f"File '{filename}' deleted successfully!", "success")
    else:
        flash(f"File '{filename}' not found.", "error")

    return redirect(url_for("index"))


@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    flash(f"File too large (max {MAX_CONTENT_LENGTH_MB} MB).", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=DEBUG, host="0.0.0.0", port=8000)
