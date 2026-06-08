# Dashboardz

A full-stack dashboard and record management web application built with **Python, Django, MySQL, Tailwind CSS, JavaScript, and Chart.js**.

Dashboardz allows users to securely manage custom datasets, perform complete CRUD operations, visualize records through interactive charts, and export data in multiple formats.

---

## Features

### Authentication & Security

* User Registration
* User Login & Logout
* Email Verification
* Password Reset via Email
* Real-Time Form Validation
* Session-Based Authentication
* Protected Routes using Django Authentication
* Environment Variable Configuration using `.env`

### Data Management

* Create Custom Tables
* Edit Existing Tables
* Delete Tables
* Add Records
* Update Records
* Delete Records
* Category Management
* Search Functionality
* Pagination Support

### Data Visualization

* Interactive Charts using Chart.js
* Dynamic Chart Selection
* Real-Time Dashboard Updates
* Category-wise Data Analysis
* Trend Visualization

### Data Export

* CSV Export
* Excel Export
* PDF Export

### User Experience

* Responsive UI
* Tailwind CSS Styling
* Reusable Django Templates
* Success/Error Notifications using Django Messages Framework

---

# Tech Stack

## Backend

* Python
* Django

## Frontend

* HTML
* Tailwind CSS
* JavaScript
* Django Template Language (DTL)

## Database

* MySQL

## Visualization

* Chart.js

## Additional Tools

* SMTP Email Service
* Django Messages Framework
* Fetch API
* Pagination
* Environment Variables

---

# Database Design

The database was designed using ER diagrams before implementation and then forward-engineered in MySQL Workbench.

The application is centered around four primary entities.

## RecordsName

Stores the name of a user-created dataset.

Examples:

* Expenses
* Investments
* Monthly Budget

---

## FieldNames

Stores dynamic column definitions for a dataset.

Examples:

* Amount
* Category
* Date

---

## Field2Names

Stores categories associated with a dataset.

Examples:

* Food
* Travel
* Salary
* Utilities

---

## FieldValues

Stores actual user-entered records.

Example:

| Amount | Category | Date       | Description |
| ------ | -------- | ---------- | ----------- |
| 500    | Food     | 2025-02-01 | Dinner      |

---

# Authentication Module

The authentication system is implemented in the `authentication` app.

## Functionalities

### Registration

* User account creation
* Input validation
* Duplicate user prevention

### Login

* Credential verification
* Session management

### Logout

* Secure session termination

### Email Verification

* Token-based account activation
* Email verification links

### Password Reset

* Email-based password recovery
* Secure token validation

---

# Real-Time Validation

Implemented using:

* JavaScript
* Event Listeners
* Fetch API
* AJAX Requests

Validation includes:

* Username availability
* Email validation
* Password validation

The submit button remains disabled until all validations pass successfully.

---

# CRUD Operations

The `records` application handles all record-management operations.

## Table Management

Users can:

* Create custom tables
* Define custom fields
* Manage categories
* Edit table configuration
* Delete tables

## Record Management

Users can:

* Create records
* View records
* Update records
* Delete records

All records are associated with the authenticated user.

---

# Search & Pagination

To improve performance and usability:

* Search functionality allows quick filtering of records.
* Pagination prevents large datasets from loading on a single page.

---

# Dynamic Data Visualization

Dashboardz uses **Chart.js** to generate interactive visualizations.

Supported capabilities include:

* Dynamic chart rendering
* Dropdown-based chart selection
* Category analysis
* Trend analysis
* Interactive user dashboards

---

# Export Functionality

Users can export their data in multiple formats.

### Supported Formats

* CSV
* Excel
* PDF

This enables offline reporting and further analysis.

---

# Security Measures

### Environment Variables

Sensitive information is stored outside the source code:

* Database Credentials
* Email Credentials
* Secret Keys

### Django Authentication

Used for:

* Password Hashing
* Session Management
* User Authorization

### Protected Views

Authenticated access is enforced through Django's authentication system.

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/dashboardz.git
cd dashboardz
```

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create a `.env` file:

```env
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_password
```

## Run Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# Key Learnings

This project provided practical experience in:

* Django MVT Architecture
* MySQL Database Design
* Authentication & Authorization
* AJAX & Fetch API
* Chart.js Integration
* CRUD Application Development
* Email Automation
* Data Export Pipelines
* Full-Stack Development
* Secure Web Application Design

---

# Future Enhancements

* REST API Integration
* User Role Management
* Advanced Analytics Dashboard
* Dark Mode Support
* Chart Customization
* Cloud Deployment
* Docker Support
* Automated Testing

---

# Author

**Vaibhav Tiwari**

Punjab Engineering College

Interested in Data Analytics, Data Engineering, Backend Development, and Full-Stack Web Development.
