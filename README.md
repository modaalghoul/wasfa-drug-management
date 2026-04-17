# Drug Management System - Django App

A comprehensive Django web application for managing pharmaceutical drugs, dosages, trade names, drug interactions, and medical equations. Features a bilingual UI supporting both English and Arabic.

## Features

- **Drug Management**: Create and manage generic medications with detailed medical information
- **Trade Name Products**: Manage commercial drug products with manufacturer details
- **Dosage Rules**: Define complex dosage calculations based on patient characteristics
- **Drug Categories & Families**: Organize drugs by therapeutic categories and families
- **Drug Interactions**: Track and manage interactions between medications
- **Medical Equations**: Store and calculate medical formulas (Cockcroft-Gault, BSA, etc.)
- **Age-Weight Estimates**: Maintain pediatric age-to-weight conversion charts
- **Bilingual Support**: Full Arabic and English interface
- **Responsive UI**: Bootstrap 5 based modern, mobile-friendly interface

## Project Structure

```
backend/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── db.sqlite3               # SQLite database (created after first run)
├── config/                  # Django project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI application
├── drug_management/         # Main Django app
│   ├── models.py            # Database models
│   ├── forms.py             # Django forms for data entry
│   ├── views.py             # View logic
│   ├── urls.py              # App URL routing
│   ├── admin.py             # Django admin configuration
│   ├── apps.py              # App configuration
│   └── templatetags/        # Custom template tags
├── static/                  # Static files (CSS, JS, images)
├── templates/               # HTML templates
│   ├── base.html            # Base template with navigation
│   └── drug_management/     # App-specific templates
├── locale/                  # Translation files
└── media/                   # Uploaded media files
```

## Installation & Setup

### 1. Prerequisites
- Python 3.8+
- pip (Python package manager)

### 2. Create Virtual Environment

```bash
cd c:\Users\Hasan\Desktop\backend
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

```bash
python manage.py migrate
```

This will create the SQLite database and apply all migrations.

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 6. Start Development Server

```bash
python manage.py runserver
```

The application will be available at: `http://localhost:8000`

### 7. Access the Application

- **Main App**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin
- **Language Switching**: Use the language selector in the top navigation

## Usage

### Adding Data

1. **Generic Medications**: Navigate to "Medications" → "Add New Medication"
   - Enter English and Arabic names
   - Select drug form, category, and family
   - Add medical information such as indications, contraindications, side effects
   - Include pregnancy and lactation safety information

2. **Trade Name Products**: Go to "Trade Names" → "Add New Product"
   - Link to generic medications
   - Add manufacturer information
   - Set availability and pricing

3. **Dosage Rules**: Create dosage calculations for medications
   - Define dose formulas (per kg, fixed range, etc.)
   - Set age and weight limits
   - Configure unit conversions (ml to drops)

4. **Drug Categories & Families**: Organize the drug database hierarchy
   - Categories: Antibiotics, GIT drugs, etc.
   - Families: Penicillins, Cephalosporins, etc.

5. **Drug Interactions**: Document interactions between medications
   - Specify severity level
   - Add management guidelines

6. **Medical Equations**: Store calculation formulas
   - Examples: Creatinine Clearance, BSA, Renal dosing

## Models Overview

### Core Models

- **PatientGroup**: Categories of patients (pediatric, adult, pregnant, etc.)
- **DrugCategory**: Main therapeutic categories (Antibiotics, Analgesics, etc.)
- **DrugFamily**: Sub-classification within categories
- **GenericMedication**: Active pharmaceutical ingredients
- **TradeNameProduct**: Commercial branded products
- **Manufacturer**: Drug manufacturers
- **DosageRule**: Dosage calculation rules for each medication
- **RangeBasedDose**: Predefined doses for age/weight ranges

### Support Models

- **DrugInteraction**: Drug-drug interaction records
- **MedicationAlternative**: Alternative medications
- **Equation**: Medical calculation formulas
- **EquationInput**: Input parameters for equations
- **AgeWeightEstimate**: Pediatric age-to-weight data
- **SearchHistory**: User search activity logs

## File Structure for Models

The models.py file includes:

1. **Choice Classes**: DosageFormChoices, RouteChoices, PregnancyCategoryChoices, etc.
2. **Model Classes**: Complete with validation, relationships, and custom methods
3. **Meta Classes**: Database indexing, ordering, and admin display settings

## Bilingual Support

### Accessing Arabic Interface

1. Click "العربية" button in the top navigation
2. The interface will switch to RTL (Right-to-Left) layout
3. All field labels and placeholders support Arabic

### Adding Arabic Content

- Each major model has parallel fields: `name` and `name_ar`
- Fill both fields to provide complete bilingual support
- Search functionality works in both languages

## Features in Detail

### Dosage Calculation

The `DosageRule` model supports multiple calculation types:

```python
# Weight-based calculation (mg/kg)
formula_type = 'per_kg'
formula_factor = 15  # 15mg/kg
formula_divisor = 1

# Split dosing (mg/kg split into multiple doses)
formula_type = 'per_kg_divided'
formula_factor = 20  # 20mg/kg total
formula_divisor = 3  # divided into 3 doses

# Minimal dose constraints
min_dose_mg = 250
max_dose_mg = 500
max_daily_dose_mg = 1000
```

### Drug Interactions

Track severity levels:
- **MILD**: Monitor, no action needed
- **MODERATE**: Monitor closely
- **SEVERE**: Avoid combination
- **CONTRAINDICATED**: Never combine

### Medical Equations

Supports parametric equations with various input types:

```python
# Example: Cockcroft-Gault for CrCl calculation
inputs = [
    {'key': 'age', 'type': 'number', 'unit': 'years'},
    {'key': 'weight', 'type': 'number', 'unit': 'kg'},
    {'key': 'creatinine', 'type': 'number', 'unit': 'mg/dL'},
    {'key': 'sex', 'type': 'select', 'options': [{'value': 'M'}, {'value': 'F'}]}
]
```

## Customization

### Adding New Fields

To add fields to existing models:

1. Edit `drug_management/models.py`
2. Add fields to the relevant model class
3. Create a migration: `python manage.py makemigrations`
4. Apply migration: `python manage.py migrate`
5. Update the corresponding form in `forms.py`
6. Update templates as needed

### Styling

The application uses Bootstrap 5. Custom CSS is in the `<style>` section of `base.html`.

To customize:
1. Edit the CSS variables at the top of `base.html`
2. Add custom CSS classes
3. Update template classes to use new styles

### Adding New Views

1. Create view function or class in `views.py`
2. Add URL pattern to `urls.py`
3. Create corresponding template
4. Add navigation link to `base.html` sidebar

## Troubleshooting

### Database Issues

Reset database:
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Static Files Not Loading

```bash
python manage.py collectstatic
```

### Port Already in Use

Use a different port:
```bash
python manage.py runserver 8080
```

### Translation Not Working

Ensure you've selected a language using the language switcher in the top navigation.

## API Routes

### Main Routes

- `/` - Dashboard
- `/admin/` - Django admin panel

### Patient Groups
- `/patient-groups/` - List
- `/patient-groups/create/` - Create
- `/patient-groups/<id>/edit/` - Edit
- `/patient-groups/<id>/delete/` - Delete

### Drug Categories
- `/categories/` - List
- `/categories/create/` - Create
- `/categories/<id>/edit/` - Edit
- `/categories/<id>/delete/` - Delete

### Medications
- `/medications/` - List
- `/medications/create/` - Create
- `/medications/<id>/` - Detail
- `/medications/<id>/edit/` - Edit
- `/medications/<id>/delete/` - Delete

### Trade Names
- `/trade-names/` - List
- `/trade-names/create/` - Create
- `/trade-names/<id>/` - Detail
- `/trade-names/<id>/edit/` - Edit
- `/trade-names/<id>/delete/` - Delete

### More Routes
- `/families/` - Drug families
- `/manufacturers/` - Manufacturers
- `/dosage-rules/` - Dosage rules
- `/equations/` - Medical equations
- `/age-weight/` - Age-weight estimates
- `/interactions/` - Drug interactions

## Performance Tips

1. **Database Queries**: Use `select_related()` and `prefetch_related()` for foreign keys
2. **Pagination**: Implement pagination for large lists (already done in views)
3. **Caching**: Consider adding Django cache framework for frequently accessed data
4. **Indexing**: Ensure database indexes on frequently filtered fields (see Meta classes)

## Future Enhancements

- [ ] REST API for mobile app integration
- [ ] Advanced search and filtering
- [ ] PDF export functionality
- [ ] Bulk import/export
- [ ] User permission system
- [ ] Audit logging
- [ ] Drug-disease interaction warnings
- [ ] Pregnancy/lactation safety ratings
- [ ] Mobile app (Flutter/React Native)

## Support & Documentation

For Django documentation: https://docs.djangoproject.com/
For Bootstrap documentation: https://getbootstrap.com/docs/

## License

Internal project for pharmaceutical management.

## Contact

For issues or questions, refer to the project documentation or contact the development team.
