#!/bin/bash

# RDS connection details - 建议使用环境变量
DB_HOST="${DB_HOST:-lab-rds.cme2agzfgwiu.us-east-1.rds.amazonaws.com}"
DB_USER="${DB_USER:-admin}"
DB_PASSWORD="${DB_PASSWORD:-123c123C}"

SQL_COMMANDS=$(cat <<EOF
/*
  Database Creation Script for the Image Captioning App
*/

DROP DATABASE IF EXISTS image_caption_db;
CREATE DATABASE image_caption_db;
USE image_caption_db;

/* Create captions table to store image captions */
CREATE TABLE captions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    image_key VARCHAR(255) NOT NULL,
    caption TEXT DEFAULT 'Processing...',  -- 修正：允许NULL或设置默认值
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

/* 可选：创建索引提高查询性能 */
CREATE INDEX idx_uploaded_at ON captions(uploaded_at);
CREATE INDEX idx_image_key ON captions(image_key);
EOF
)

# Execute SQL commands
echo "Creating database and table..."
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" -e "$SQL_COMMANDS"

# Check if the previous command was successful
if [ $? -eq 0 ]; then
    echo "Database and table created successfully!"
    echo "Table structure:"
    mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" -e "USE image_caption_db; DESCRIBE captions;"
else
    echo "Error: Failed to create database and table. Please check the connection details and try again."
    exit 1
fi