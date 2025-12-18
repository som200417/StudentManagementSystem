🎓 Student Management System

A Student Management System built using Django, Django REST Framework, and MySQL.
This project manages students, courses, and teachers with secure authentication, role-based access, activity logging, CSV import/export, soft delete functionality, and RESTful APIs.

🚀 Features

Student, Course & Teacher CRUD operations

Soft delete (mark inactive instead of permanent delete)

CSV import with validation & row-wise error reporting

CSV export of student data

Activity logging (stored in DB & accessible via API)

Role-based authentication (Admin / Staff)

Dashboard with student statistics

REST APIs returning clean JSON responses

MySQL database integration

🛠 Tech Stack

Python

Django

Django REST Framework

MySQL

HTML, Bootstrap

📊 Dashboard Reports

Total active students

Students count per course

🔐 Authentication & Permissions

Login / Logout / Register

Admin-only actions

Permission-based access using Django permissions

📁 CSV Import / Export

Import

Upload student data via CSV

Validates name, email, age, phone, and course

Shows errors for invalid rows

Export

Download all active students as CSV

📜 Activity Logs

Logs Create, Update, Delete actions

Stores user, action, model, and timestamp

Available via REST API (/activity-logs/)
