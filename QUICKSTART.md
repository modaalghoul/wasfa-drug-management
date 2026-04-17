# Quick Start Guide

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

## 1. Create Virtual Environment

```bash
python -m venv venv
```

## 2. Activate Virtual Environment

**Windows:**
```bash
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Create Database Migrations

```bash
python manage.py makemigrations
```

This generates migration files from your models.

## 5. Apply Migrations

```bash
python manage.py migrate
```

This creates the SQLite database (`db.sqlite3`) with all tables.

## 6. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account:
- Username: (e.g., admin)
- Email: (your email)
- Password: (your secure password)

## 7. Start Development Server

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

## 8. Access the Application

### English Interface
- Dashboard: http://localhost:8000/
- Django Admin: http://localhost:8000/admin/

### Arabic Interface
- Dashboard: http://localhost:8000/ar/
- Admin Login: http://localhost:8000/ar/admin/

### Default Credentials
- Username: (what you created in step 6)
- Password: (what you created in step 6)

## 9. Initial Data Entry

After logging in to the dashboard, create the foundational data:

### 1. Patient Groups (http://localhost:8000/patient-groups/)
Create patient categories like:
- Pediatric (نموذج الأطفال)
- Adult (البالغين)
- Pregnant Women (النساء الحوامل)
- Elderly (كبار السن)

### 2. Drug Categories (http://localhost:8000/drug-categories/)
Add therapeutic categories like:
- Antibiotics
- Analgesics
- GIT Drugs
- Respiratory Medications

### 3. Drug Families
Add families under each category (e.g., Penicillins under Antibiotics)

### 4. Manufacturers
Add pharmaceutical manufacturers

### 5. Generic Medications
Add active pharmaceutical ingredients with medical information

### 6. Trade Names
Link trade name products to generic medications

> **Tip:** Use the Django Admin panel (http://localhost:8000/admin/) for rapid bulk data entry

## 10. Language Switching

Click the language buttons in the top-right corner:
- **en** - English
- **العربية** - Arabic

The interface and database labels are fully bilingual.

## Project Structure

```
backend/
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── config/                    # Django project settings
│   ├── settings.py           # Main configuration
│   ├── urls.py               # URL routing
│   └── wsgi.py               # WSGI application
├── drug_management/           # Main Django app
│   ├── models.py             # Database schemas (15 models)
│   ├── forms.py              # Data entry forms
│   ├── views.py              # Business logic (40+ views)
│   ├── urls.py               # App URL routing
│   ├── admin.py              # Django admin configuration
│   └── templatetags/         # Custom template tags
├── templates/                 # HTML templates
│   ├── base.html             # Master template
│   └── drug_management/      # App-specific templates
└── db.sqlite3                # Database (created after migration)
```

## Common Commands

```bash
# Create migrations from models
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver

# Access shell for testing
python manage.py shell

# Create new app
python manage.py startapp appname

# Collect static files (production)
python manage.py collectstatic
```

## Troubleshooting

### Port Already in Use
If port 8000 is already in use:
```bash
python manage.py runserver 8001
```

### Database Issues
If you encounter database errors, reset the database:
```bash
# Delete the database file
rm db.sqlite3

# Recreate migrations
python manage.py makemigrations

# Rerun migrations
python manage.py migrate

# Create new superuser
python manage.py createsuperuser
```

### Template Not Found
Clear the template cache:
```bash
# Restart the development server
python manage.py runserver
```

### Import Errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt --force-reinstall
```

## Features Overview

### ✅ Implemented

- **Bilingual UI**: Arabic/English with RTL support
- **15 Database Models**: Complete pharmaceutical data structure
- **CRUD Operations**: Create, Read, Update, Delete for all models
- **Advanced Search**: Search medications, trade names, equations
- **Filtering**: Filter by category, family, severity, etc.
- **Pagination**: List views with page navigation
- **Dashboard**: Statistics and quick actions
- **Dosage Calculator**: Complex formula-based dose calculations
- **Drug Interactions**: Track interactions between medications
- **Age-Weight Estimates**: Reference growth charts
- **Medical Equations**: Clinical calculators (BSA, eGFR, etc.)
- **Responsive Design**: Works on desktop, tablet, mobile
- **Admin Panel**: Django admin for staff management

### 🔜 Future Enhancements

- API endpoints (REST/GraphQL)
- User roles and permissions
- Data export (PDF, Excel)
- Mobile app
- Clinical decision support alerts
- Multimedia support for patient education

## Support & Documentation

For detailed documentation, see [README.md](README.md)

For API route documentation, see [README.md - API Routes](README.md#api-routes)

## Production Deployment

For production deployment, see [README.md - Deployment](README.md#deployment--production)

---

**Created:** 2024
**Django Version:** 4.2.0
**Python Version:** 3.8+
