import os
import boto3
import mysql.connector
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import base64
from io import BytesIO
import google.generativeai as genai

app = Flask(__name__)

# ========== 从环境变量读取配置 ==========
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
S3_REGION = os.environ.get("AWS_REGION", "us-east-1")
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME", "image_caption_db")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

# 配置 Gemini API
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# ========== 工具函数 ==========

def get_s3_client():
    return boto3.client("s3", region_name=S3_REGION)

def get_db_connection():
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
    except mysql.connector.Error as err:
        print("Error connecting to database:", err)
        return None

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ========== 路由 ==========

@app.route("/")
def upload_form():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if "file" not in request.files:
            return render_template("upload.html", error="No file selected")

        file = request.files["file"]
        if file.filename == "":
            return render_template("upload.html", error="No file selected")
        if not allowed_file(file.filename):
            return render_template("upload.html", error="Invalid file type")

        filename = secure_filename(file.filename)
        file_data = file.read()

        try:
            s3 = get_s3_client()
            s3.upload_fileobj(BytesIO(file_data), S3_BUCKET, filename)
        except Exception as e:
            return render_template("upload.html", error=f"S3 Upload Error: {str(e)}")

        try:
            connection = get_db_connection()
            if connection is None:
                return render_template("upload.html", error="Database Error")
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO captions (image_key, caption) VALUES (%s, %s)",
                (filename, "Processing...")
            )
            connection.commit()
            connection.close()
        except Exception as e:
            return render_template("upload.html", error=f"Database Error: {str(e)}")

        encoded_image = base64.b64encode(file_data).decode("utf-8")
        file_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{filename}"
        caption = "Processing... (Lambda will update this soon)"

        return render_template("upload.html", image_data=encoded_image, file_url=file_url, caption=caption)

    return render_template("upload.html")

@app.route("/gallery")
def gallery():
    try:
        connection = get_db_connection()
        if connection is None:
            return render_template("gallery.html", error="Database Error")
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT image_key, caption FROM captions ORDER BY uploaded_at DESC")
        results = cursor.fetchall()
        connection.close()

        images_with_captions = []
        s3_client = get_s3_client()
        
        for row in results:
            try:
                # 生成原图预签名链接
                url = s3_client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": S3_BUCKET, "Key": row["image_key"]},
                    ExpiresIn=3600,
                )
                # 生成缩略图预签名链接
                thumbnail_key = f"thumbnails/{row['image_key']}"
                thumbnail_url = s3_client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": S3_BUCKET, "Key": thumbnail_key},
                    ExpiresIn=3600,
                )
                images_with_captions.append({
                    "url": url,
                    "thumbnail_url": thumbnail_url,
                    "image_key": row["image_key"],
                    "caption": row["caption"] if row["caption"] else "Processing..."
                })
            except Exception as e:
                print(f"Error generating URLs for {row['image_key']}: {str(e)}")
                continue

        return render_template(
            "gallery.html",
            images=images_with_captions
        )

    except Exception as e:
        return render_template("gallery.html", error=f"Error: {str(e)}")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
