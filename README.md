# AWS AI Image Annotation Platform

An AWS-based image annotation platform for uploading images, storing them in Amazon S3, generating captions with Google Gemini, and managing annotation records through a web interface.

## Project Overview

This project implements an image annotation web application that combines:

- **Flask** for the web interface
- **Amazon S3** for image storage
- **MySQL / RDS** for metadata storage
- **Google Gemini API** for automatic image caption generation

The platform allows users to upload images, generate AI-based captions, and review stored annotation results through a browser-based application.

## Main Features

- Upload images through a web interface
- Store uploaded files in Amazon S3
- Generate image captions using Google Gemini
- Save image metadata and captions into a relational database
- Display uploaded images and generated captions in the application

## Project Structure

```text
.
├── Image-caption-app-V1.1/   # Original app source
├── final_app/                # Final application version
├── testing_pics/             # Sample test images
├── doc/                      # Documentation files
├── report/                   # Report materials
├── lambda_final              #lambda depends packages
└── README.md
```

## Technologies Used

- Python

- Flask

- Boto3

- Amazon S3

- MySQL / Amazon RDS

- Google Gemini API

## Environment Requirements

Before running the project, make sure the following are available:

- Python 3.9 or above

- AWS account and S3 bucket

- MySQL database or Amazon RDS instance

- Google Gemini API key

## Installation

Clone the repository:

```bash
git clone git@github.com:perry-yuepan/aws-ai-image-annotation-platform.git
cd aws-ai-image-annotation-platform
```
Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```
Install dependencies:
```bash
pip install flask boto3 pymysql google-generativeai werkzeug
```
## Configuration

Update the application configuration before running.

**1. Google Gemini API**

Set your API key in the Python application:
```env
GOOGLE_API_KEY = "your_google_api_key"
```
**2. AWS S3**

Set your S3 bucket information:
```env
S3_BUCKET = "your_bucket_name"
S3_REGION = "us-east-1"
```
**3. Database**

Set your MySQL or RDS connection details:
```env
DB_HOST = "your_database_endpoint"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_NAME = "your_database_name"
```
## Running the Application

Move into the application folder and run Flask:
```bash
cd Image-caption-app-V1.1
python app.py
```
Then open the local address shown in the terminal in your browser.

## Workflow

1. User uploads an image

2. The application sends the image to Amazon S3

3. The system generates a caption using Google Gemini

4. The image key, URL, and generated caption are stored in the database

5. The web interface displays the uploaded image and annotation result

## Notes

- Do not upload large dependency folders such as virtual environments or packaged libraries to GitHub.

- Sensitive credentials such as API keys, AWS credentials, and database passwords should not be committed to the repository.

- A ```.gitignore``` file should be used to exclude unnecessary files such as:

  - ```__pycache__/```

  - ```.DS_Store```
  
  - `.env`

  - `venv/`

  - `lambda-final/`

## Appendix
- Report:
- testing screenshoot from aws:
- video: 
