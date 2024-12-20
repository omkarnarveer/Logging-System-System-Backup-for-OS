# Logging-System-System-Backup-for-OS

This project is a Flask-based application for managing backups and logging events, with a MySQL database for storage. It includes a user-friendly web interface created using Bootstrap 5.

## Features

- **Backup Functionality**: Accepts source and destination directories to create backups as `.zip` files.
- **Logging System**: Tracks application events (e.g., errors, successful backups) and stores them in a MySQL database.
- **Database Tables**:
  - `log_entry`: Stores log details such as timestamp, log level, and message.
  - `backup_record`: Tracks backup operations with source, destination, timestamp, and status.
- **Web Interface**:
  - View and search logs.
  - View backup records.

## Prerequisites

- Python 3.8+
- MySQL Server
- Flask Framework
- Bootstrap 5 (for UI)

## Setup Instructions

### 1. Clone the Repository

```bash
$ git clone https://github.com/omkarnarveer/Logging-System-and-System-Backup-for-OS.git
$ cd Logging-System-and-System-Backup-for-OS
```

### 2. Install Dependencies

Create a virtual environment and install the required Python packages:

```bash
$ python -m venv venv
$ source venv/bin/activate  # On Windows: venv\Scripts\activate
$ pip install -r requirements.txt
```

### 3. Configure MySQL Database

Create a MySQL database and update the `DB_CONFIG` in `app.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'logging_backup',
}
```

### 4. Initialize the Database

Run the application once to create necessary tables:

```bash
$ python app.py
```

### 5. Populate Sample Data

Insert initial data into the database if necessary:

```sql
-- Insert sample logs
INSERT INTO log_entry (timestamp, log_level, message) VALUES
(NOW(), 'ERROR', 'Sample log message 1'),
(NOW(), 'INFO', 'Sample log message 2');

-- Insert sample backup records
INSERT INTO backup_record (timestamp, source, destination, status) VALUES
(NOW(), 'C:/source1', 'C:/backup1', 'SUCCESS'),
(NOW(), 'C:/source2', 'C:/backup2', 'FAILED');
```

### 6. Run the Application

Start the Flask development server:

```bash
$ python app.py
```

The application will be accessible at `http://127.0.0.1:5000/`.

## File Structure

```
backup-logging-system/
├── app.py              # Main Flask application
├── templates/          # HTML templates for UI
│   ├── base.html       # Base layout template
│   ├── logs.html       # Log entries page
│   └── index.html      # Project main page
├── static/             # Static files (CSS, JS, etc.)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Usage

### Backup Files
1. Navigate to the home page.
2. Enter the source and destination directories.
3. Click "Create Backup" to generate a `.zip` file.

### View Logs
1. Navigate to `/logs`.
2. Browse log entries in an ascending order.

### View Backup Records
1. Navigate to `/backup-records`.
2. Browse backup operations and their statuses.

## Technologies Used

- **Backend**: Flask, MySQL, Python
- **Frontend**: Bootstrap 5
- **Database**: MySQL

## Future Enhancements

- Add user authentication for secured access.
- Implement real-time backup progress monitoring.
- Support scheduling backups at specific intervals.

