from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import zipfile
import mysql.connector

app = Flask(__name__)
# Database Configuration
DB_CONFIG = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'logging_backup',
}


# Database Initialization
def initialize_database():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS backup_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            folder_path VARCHAR(255),
            backup_path VARCHAR(255),
            status ENUM('SUCCESS', 'FAILURE'),
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Utility Functions
def create_zip(folder_path, backup_path):
    """
    Creates a ZIP archive of the specified folder.
    Args:
        folder_path (str): Path to the folder to be backed up.
        backup_path (str): Path to the backup directory.
    Returns:
        str: Full path to the created ZIP file.
    """
    # Normalize paths for Windows
    folder_path = os.path.normpath(folder_path.strip('"'))  # Remove extra quotes and normalize
    backup_path = os.path.normpath(backup_path.strip('"'))

    # Ensure the backup directory exists
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)

    # Define the ZIP file name
    zip_filename = os.path.join(backup_path, 'backup.zip')

    # Create the ZIP file
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

    return zip_filename

def save_log(folder_path, backup_path, status):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO backup_logs (folder_path, backup_path, status) 
        VALUES (%s, %s, %s)
    """, (folder_path, backup_path, status))
    conn.commit()
    cursor.close()
    conn.close()

def fetch_logs():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM backup_logs ORDER BY timestamp ASC")
    logs = cursor.fetchall()
    cursor.close()
    conn.close()
    return logs

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/backup', methods=['POST'])
def backup():
    folder_path = request.form['folder_path']
    backup_path = request.form['backup_path']
    try:
        zip_file_path = create_zip(folder_path, backup_path)
        save_log(folder_path, backup_path, 'SUCCESS')
        return render_template('backup_records.html', success=True, backup_file=zip_file_path)
    except Exception as e:
        save_log(folder_path, backup_path, 'FAILURE')
        return render_template('backup_records.html', success=False, error=str(e))

@app.route('/logs')
def logs():
    log_records = fetch_logs()
    return render_template('logs.html', logs=log_records)

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)