<<<<<<< HEAD
# 🚍 Smart Transport Management System

A Django-based transport management system designed for students, drivers, and managers. The system provides bus trip assignments, driver management, payment automation, and real-time bus stop management using Google Maps API.

## 📌 Features

### ✅ Student Dashboard
- View assigned trips and vehicle details
- Track payment due dates and make payments

### ✅ Driver Dashboard
- View assigned trips and track onboard students
- Toggle student onboard status

### ✅ Manager Dashboard
- Assign drivers to vehicles and routes
- Manage student payments and vehicle assignments
- Add/Delete bus stops dynamically via Google Maps

### ✅ Automated Payment System
- Monthly recurring payments
- Overdue payment tracking and automatic account disabling

### ✅ Bus Stop Management
- Add, edit, and delete bus stops dynamically using Google Maps
- Fetch addresses using Google Geocoding API

## 🚀 Setup & Installation

### 1️⃣ Install Dependencies
Ensure you have Python 3.12+ and MySQL installed.

```bash
pip install -r requirements.txt
```
### 2️⃣ Database Setup (MySQL)
Ensure MySQL is installed and running. Then, create the database and a user:

```sql
CREATE DATABASE smart_transport;
CREATE USER 'smart_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON smart_transport.* TO 'smart_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3️⃣ Configure settings.py
Update the database configuration in settings.py:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'smart_transport',
        'USER': 'smart_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 4️⃣ Apply Migrations
Run the following commands to set up the database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create a Superuser (Admin)
To access the Django Admin Panel, create an admin user:

```bash
python manage.py createsuperuser
```
Follow the prompts to set up a username and password.

### 6️⃣ Run the Server
Start the Django development server:

```bash
python manage.py runserver
```
The system will be available at http://127.0.0.1:8000.




=======
# Smart-Transport-Management-System

The Smart Transport Management System is an AI-powered web application designed to enhance and modernize university transportation services. This system automates key processes, optimizes resource utilization, and ensures a seamless experience for students, staff, and administrators.

✨ Key Features
AI-Driven Route Optimization 🛣️

Analyzes real-time and historical traffic data to suggest the best routes, reducing travel time and fuel consumption.

Efficient Transport Administration 🚐

Simplifies vehicle assignments, route planning, and driver scheduling.

Provides real-time trip status updates and centralized transport records.

Student & Staff Convenience 🎓

Easy registration with personalized pick-up and drop-off preferences.

Real-time trip notifications and dynamic vehicle allocation based on availability.

Payment & Accountability System 💳

Tracks trip expenses and fee payments.

Ensures service availability only for users with cleared dues.

Driver & Admin Panel 🖥️

Allows drivers to update trip statuses in real time.

Enables administrators to monitor operations efficiently.

🎯 Why This Project?
University transportation management can be complex, with challenges like scheduling conflicts, inefficient routes, and payment tracking. This system integrates AI to provide a cost-effective, scalable, and user-friendly solution that ensures a smoother, more reliable experience for all users.

🚀 Streamline university transport operations with AI-powered efficiency!
>>>>>>> 5a2a1fbf12fc56344b6cc2b4d5917457e39f2722

