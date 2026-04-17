# -*- coding: utf-8 -*-
"""
================================================================================
Management Command: seed_data
================================================================================
Usage:  python manage.py seed_data
        python manage.py seed_data --force   (re-runs even if data exists)
================================================================================
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from drug_management.models import (
    PatientGroup, DrugCategory, DrugFamily, AgeWeightEstimate,
    Equation, EquationInput,
)


class Command(BaseCommand):
    help = "Load initial / seed data into the database (skips records that already exist)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force re-seed: delete existing data and reload everything from scratch.',
        )

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------
    def _ok(self, msg):
        self.stdout.write(self.style.SUCCESS(f"  [OK] {msg}"))

    def _skip(self, msg):
        self.stdout.write(self.style.WARNING(f"  [--] {msg}"))

    def _section(self, msg):
        self.stdout.write(self.style.MIGRATE_HEADING(f"\n{msg}"))

    # ------------------------------------------------------------------
    # main
    # ------------------------------------------------------------------
    def handle(self, *args, **options):
        force = options['force']

        if force:
            self.stdout.write(self.style.WARNING(
                "\n[!] --force flag detected - wiping existing seed data ...\n"
            ))
            EquationInput.objects.all().delete()
            Equation.objects.all().delete()
            AgeWeightEstimate.objects.all().delete()
            DrugFamily.objects.all().delete()
            DrugCategory.objects.all().delete()
            PatientGroup.objects.all().delete()

        with transaction.atomic():
            self._seed_patient_groups()
            cat_map = self._seed_categories()
            self._seed_families(cat_map)
            self._seed_age_weight()
            self._seed_equations()

        self.stdout.write(self.style.SUCCESS("\n[DONE] All initial data loaded successfully!\n"))

    # ------------------------------------------------------------------
    # 1. PatientGroup
    # ------------------------------------------------------------------
    def _seed_patient_groups(self):
        self._section("1. PatientGroup")
        rows = [
            {'name': 'pediatric',     'name_ar': 'أطفال',        'display_order': 1,
             'requires_weight_input': True,  'requires_age_input': True},
            {'name': 'adult',         'name_ar': 'بالغين',        'display_order': 2,
             'requires_weight_input': False, 'requires_age_input': False},
            {'name': 'pregnant',      'name_ar': 'حوامل',         'display_order': 3,
             'requires_weight_input': False, 'requires_age_input': False},
            {'name': 'breastfeeding', 'name_ar': 'مرضعات',        'display_order': 4,
             'requires_weight_input': False, 'requires_age_input': False},
            {'name': 'elderly',       'name_ar': 'كبار السن',     'display_order': 5,
             'requires_weight_input': True,  'requires_age_input': True},
            {'name': 'renal',         'name_ar': 'قصور كلوي',     'display_order': 6,
             'requires_weight_input': True,  'requires_age_input': True},
        ]
        created_count = skipped_count = 0
        for row in rows:
            _, created = PatientGroup.objects.get_or_create(
                name=row['name'], defaults=row
            )
            if created:
                self._ok(f"Created PatientGroup: {row['name']}")
                created_count += 1
            else:
                self._skip(f"Already exists -- PatientGroup: {row['name']}")
                skipped_count += 1
        self.stdout.write(f"     -> {created_count} created, {skipped_count} skipped")

    # ------------------------------------------------------------------
    # 2. DrugCategory
    # ------------------------------------------------------------------
    def _seed_categories(self):
        self._section("2. DrugCategory")
        rows = [
            {'name': 'Antibiotic Drugs',
             'name_ar': 'المضادات الحيوية',
             'icon': '🦠', 'display_order': 1},
            {'name': 'Antipyretic & Analgesic',
             'name_ar': 'خافضات الحرارة والمسكنات',
             'icon': '🌡️', 'display_order': 2},
            {'name': 'Antihistamine & Corticosteroids',
             'name_ar': 'مضادات الهيستامين والكورتيزون',
             'icon': '💊', 'display_order': 3},
            {'name': 'GIT Drugs',
             'name_ar': 'أدوية الجهاز الهضمي',
             'icon': '🫀', 'display_order': 4},
            {'name': 'Respiratory Tract Drugs',
             'name_ar': 'أدوية الجهاز التنفسي',
             'icon': '🫁', 'display_order': 5},
            {'name': 'Equations & Resources',
             'name_ar': 'المعادلات والمراجع',
             'icon': '🧮', 'display_order': 6},
        ]
        cat_map = {}
        created_count = skipped_count = 0
        for row in rows:
            obj, created = DrugCategory.objects.get_or_create(
                name=row['name'], defaults=row
            )
            cat_map[row['name']] = obj
            if created:
                self._ok(f"Created DrugCategory: {row['name']}")
                created_count += 1
            else:
                self._skip(f"Already exists -- DrugCategory: {row['name']}")
                skipped_count += 1
        self.stdout.write(f"     -> {created_count} created, {skipped_count} skipped")
        return cat_map

    # ------------------------------------------------------------------
    # 3. DrugFamily
    # ------------------------------------------------------------------
    def _seed_families(self, cat_map):
        self._section("3. DrugFamily")
        rows = [
            # Antibiotics
            ('Penicillins',              'بنسيلينات',                     'Antibiotic Drugs', 1),
            ('Cephalosporins',           'سيفالوسبورينات',                'Antibiotic Drugs', 2),
            ('Macrolides',               'ماكروليدات',                    'Antibiotic Drugs', 3),
            ('Fluoroquinolones',         'فلوروكينولونات',                'Antibiotic Drugs', 4),
            ('Aminoglycosides',          'أمينوغليكوزيدات',               'Antibiotic Drugs', 5),
            ('Sulfonamides',             'سلفوناميدات',                   'Antibiotic Drugs', 6),
            # Antipyretic & Analgesic
            ('Paracetamol',              'باراسيتامول',                   'Antipyretic & Analgesic', 1),
            ('NSAIDs',                   'مضادات التهاب غير ستيرويدية',   'Antipyretic & Analgesic', 2),
            ('Ibuprofen',                'ايبوبروفين',                    'Antipyretic & Analgesic', 3),
            ('Opioid Analgesics',        'مسكنات أفيونية',                'Antipyretic & Analgesic', 4),
            # Antihistamine & Corticosteroids
            ('H1 Blockers (1st gen)',    'مضادات H1 الجيل الأول',         'Antihistamine & Corticosteroids', 1),
            ('H1 Blockers (2nd gen)',    'مضادات H1 الجيل الثاني',        'Antihistamine & Corticosteroids', 2),
            ('Systemic Corticosteroids', 'كورتيزونات جهازية',             'Antihistamine & Corticosteroids', 3),
            ('Topical Corticosteroids',  'كورتيزونات موضعية',             'Antihistamine & Corticosteroids', 4),
            # GIT
            ('Antacids',                 'مضادات الحموضة',                'GIT Drugs', 1),
            ('PPIs',                     'مثبطات مضخة البروتون',          'GIT Drugs', 2),
            ('H2 Blockers',              'مضادات H2',                     'GIT Drugs', 3),
            ('Antidiarrheal',            'مضادات الإسهال',                'GIT Drugs', 4),
            ('Laxatives',                'ملينات',                        'GIT Drugs', 5),
            ('Antiemetics',              'مضادات الغثيان',                'GIT Drugs', 6),
            # Respiratory
            ('Bronchodilators',          'موسعات القصبة',                 'Respiratory Tract Drugs', 1),
            ('Inhaled Steroids',         'كورتيزونات استنشاقية',          'Respiratory Tract Drugs', 2),
            ('Mucolytics',               'مذيبات البلغم',                 'Respiratory Tract Drugs', 3),
            ('Antitussives',             'مضادات السعال',                 'Respiratory Tract Drugs', 4),
            ('Decongestants',            'مزيلات الاحتقان',               'Respiratory Tract Drugs', 5),
        ]
        created_count = skipped_count = 0
        for name, name_ar, cat_name, order in rows:
            _, created = DrugFamily.objects.get_or_create(
                name=name,
                defaults={
                    'name_ar': name_ar,
                    'drug_category': cat_map.get(cat_name),
                    'display_order': order,
                },
            )
            if created:
                self._ok(f"Created DrugFamily: {name}")
                created_count += 1
            else:
                self._skip(f"Already exists -- DrugFamily: {name}")
                skipped_count += 1
        self.stdout.write(f"     -> {created_count} created, {skipped_count} skipped")

    # ------------------------------------------------------------------
    # 4. AgeWeightEstimate
    # ------------------------------------------------------------------
    def _seed_age_weight(self):
        self._section("4. AgeWeightEstimate (0 months -> 15 years)")
        rows = [
            (0,   'Newborn',    3.5,  '0-1 years'),
            (1,   '1 month',    4.5,  '0-1 years'),
            (2,   '2 months',   5.5,  '0-1 years'),
            (3,   '3 months',   6.4,  '0-1 years'),
            (4,   '4 months',   7.0,  '0-1 years'),
            (5,   '5 months',   7.5,  '0-1 years'),
            (6,   '6 months',   7.9,  '0-1 years'),
            (7,   '7 months',   8.3,  '0-1 years'),
            (8,   '8 months',   8.6,  '0-1 years'),
            (9,   '9 months',   8.9,  '0-1 years'),
            (10,  '10 months',  9.2,  '0-1 years'),
            (11,  '11 months',  9.4,  '0-1 years'),
            (12,  '1 year',     9.5,  '1-5 years'),
            (13,  '13 months',  9.7,  '1-5 years'),
            (14,  '14 months',  9.9,  '1-5 years'),
            (15,  '15 months', 10.1,  '1-5 years'),
            (16,  '16 months', 10.3,  '1-5 years'),
            (17,  '17 months', 10.5,  '1-5 years'),
            (18,  '18 months', 10.7,  '1-5 years'),
            (19,  '19 months', 11.0,  '1-5 years'),
            (20,  '20 months', 11.2,  '1-5 years'),
            (21,  '21 months', 11.4,  '1-5 years'),
            (22,  '22 months', 11.6,  '1-5 years'),
            (23,  '23 months', 11.8,  '1-5 years'),
            (24,  '2 years',   12.2,  '1-5 years'),
            (36,  '3 years',   14.1,  '1-5 years'),
            (48,  '4 years',   15.8,  '1-5 years'),
            (60,  '5 years',   18.1,  '1-5 years'),
            (72,  '6 years',   20.3,  '6-15 years'),
            (84,  '7 years',   22.7,  '6-15 years'),
            (96,  '8 years',   25.7,  '6-15 years'),
            (108, '9 years',   28.4,  '6-15 years'),
            (120, '10 years',  32.0,  '6-15 years'),
            (132, '11 years',  36.3,  '6-15 years'),
            (144, '12 years',  40.7,  '6-15 years'),
            (156, '13 years',  45.6,  '6-15 years'),
            (168, '14 years',  49.2,  '6-15 years'),
            (180, '15 years',  54.0,  '6-15 years'),
        ]
        created_count = skipped_count = 0
        for months, text, weight, group in rows:
            _, created = AgeWeightEstimate.objects.get_or_create(
                age_months=months,
                defaults={
                    'age_text': text,
                    'estimated_weight_kg': weight,
                    'age_group': group,
                },
            )
            if created:
                created_count += 1
            else:
                skipped_count += 1
        self._ok(f"AgeWeightEstimate: {created_count} created, {skipped_count} already existed")

    # ------------------------------------------------------------------
    # 5. Equations + EquationInputs
    # ------------------------------------------------------------------
    def _seed_equations(self):
        self._section("5. Equations")
        equations_data = [
            {
                'name': 'Cockcroft-Gault',
                'name_ar': 'معادلة كوكروفت-غولت (تصفية الكرياتينين)',
                'description': 'Estimates creatinine clearance (CrCl) used to adjust drug doses in renal impairment.',
                'description_ar': 'تقدير تصفية الكرياتينين لتعديل جرعات الأدوية في حالات القصور الكلوي.',
                'formula_display': 'CrCl = [(140 - Age) x Weight] / (72 x Cr)  x  0.85 (females)',
                'result_unit': 'ml/min',
                'result_label': 'Creatinine Clearance',
                'reference': 'Cockcroft DW, Gault MH. Nephron. 1976;16(1):31-41.',
                'category': 'Renal',
                'display_order': 1,
                'interpretation': [
                    {'min': 0,  'max': 15,  'label': 'Kidney failure (Stage 5)'},
                    {'min': 15, 'max': 30,  'label': 'Severe decrease (Stage 4)'},
                    {'min': 30, 'max': 60,  'label': 'Moderate decrease (Stage 3)'},
                    {'min': 60, 'max': 90,  'label': 'Mild decrease (Stage 2)'},
                    {'min': 90, 'max': 999, 'label': 'Normal (Stage 1)'},
                ],
                'inputs': [
                    {'key': 'age',        'label': 'Age',        'label_ar': 'العمر',         'input_type': 'number', 'unit': 'years', 'display_order': 1},
                    {'key': 'weight',     'label': 'Weight',     'label_ar': 'الوزن',         'input_type': 'number', 'unit': 'kg',    'display_order': 2},
                    {'key': 'creatinine', 'label': 'Creatinine', 'label_ar': 'الكرياتينين',   'input_type': 'number', 'unit': 'mg/dL', 'display_order': 3},
                    {'key': 'sex', 'label': 'Sex', 'label_ar': 'الجنس', 'input_type': 'select',
                     'options': [{'value': 'male', 'label': 'Male'}, {'value': 'female', 'label': 'Female'}],
                     'display_order': 4},
                ],
            },
            {
                'name': 'Mosteller BSA',
                'name_ar': 'مساحة سطح الجسم (Mosteller)',
                'description': 'Body Surface Area calculation used in chemotherapy dosing.',
                'description_ar': 'حساب مساحة سطح الجسم المستخدمة في جرعات الكيماوي.',
                'formula_display': 'BSA = sqrt(Height(cm) x Weight(kg) / 3600)',
                'result_unit': 'm2',
                'result_label': 'Body Surface Area',
                'reference': 'Mosteller RD. N Engl J Med. 1987;317(17):1098.',
                'category': 'General',
                'display_order': 2,
                'interpretation': [],
                'inputs': [
                    {'key': 'height', 'label': 'Height', 'label_ar': 'الطول', 'input_type': 'number', 'unit': 'cm', 'display_order': 1},
                    {'key': 'weight', 'label': 'Weight', 'label_ar': 'الوزن', 'input_type': 'number', 'unit': 'kg', 'display_order': 2},
                ],
            },
            {
                'name': 'IBW (Devine)',
                'name_ar': 'الوزن المثالي (Devine)',
                'description': 'Ideal Body Weight for dosing calculations.',
                'description_ar': 'الوزن المثالي لحساب الجرعات.',
                'formula_display': 'Male: IBW = 50 + 2.3 x (Height_inches - 60)\nFemale: IBW = 45.5 + 2.3 x (Height_inches - 60)',
                'result_unit': 'kg',
                'result_label': 'Ideal Body Weight',
                'reference': 'Devine BJ. Drug Intell Clin Pharm. 1974;8:650-655.',
                'category': 'General',
                'display_order': 3,
                'interpretation': [],
                'inputs': [
                    {'key': 'height', 'label': 'Height', 'label_ar': 'الطول', 'input_type': 'number', 'unit': 'cm', 'display_order': 1},
                    {'key': 'sex', 'label': 'Sex', 'label_ar': 'الجنس', 'input_type': 'select',
                     'options': [{'value': 'male', 'label': 'Male'}, {'value': 'female', 'label': 'Female'}],
                     'display_order': 2},
                ],
            },
            {
                'name': 'Holliday-Segar (Fluid Requirement)',
                'name_ar': 'احتياج السوائل اليومي للأطفال',
                'description': 'Daily maintenance fluid requirement for pediatric patients.',
                'description_ar': 'حساب احتياج السوائل اليومي للأطفال.',
                'formula_display': '0-10 kg: 100 ml/kg\n10-20 kg: 1000 ml + 50 ml/kg above 10\n>20 kg: 1500 ml + 20 ml/kg above 20',
                'result_unit': 'ml/day',
                'result_label': 'Maintenance Fluid',
                'reference': 'Holliday MA, Segar WE. Pediatrics. 1957;19(5):823-832.',
                'category': 'Pediatric',
                'display_order': 4,
                'interpretation': [],
                'inputs': [
                    {'key': 'weight', 'label': 'Weight', 'label_ar': 'الوزن', 'input_type': 'number', 'unit': 'kg', 'display_order': 1},
                ],
            },
            {
                'name': 'Rehydration Deficit',
                'name_ar': 'حساب نقص السوائل (الجفاف)',
                'description': 'Calculates fluid deficit in dehydrated patients.',
                'description_ar': 'حساب كمية السوائل المفقودة في حالات الجفاف.',
                'formula_display': 'Deficit (ml) = Weight(kg) x Dehydration% x 10',
                'result_unit': 'ml',
                'result_label': 'Fluid Deficit',
                'reference': 'Nelson Textbook of Pediatrics.',
                'category': 'Pediatric',
                'display_order': 5,
                'interpretation': [],
                'inputs': [
                    {'key': 'weight', 'label': 'Weight', 'label_ar': 'الوزن', 'input_type': 'number', 'unit': 'kg', 'display_order': 1},
                    {'key': 'dehydration_percent', 'label': 'Dehydration %', 'label_ar': 'نسبة الجفاف %',
                     'input_type': 'select',
                     'options': [
                         {'value': '5',  'label': '5% - Mild'},
                         {'value': '10', 'label': '10% - Moderate'},
                         {'value': '15', 'label': '15% - Severe'},
                     ],
                     'display_order': 2},
                ],
            },
        ]

        created_count = skipped_count = 0
        for eq_data in equations_data:
            inputs = eq_data.pop('inputs')
            eq, created = Equation.objects.get_or_create(
                name=eq_data['name'],
                defaults=eq_data,
            )
            if created:
                for inp in inputs:
                    EquationInput.objects.create(equation=eq, **inp)
                self._ok(f"Created Equation: {eq_data['name']} (+ {len(inputs)} inputs)")
                created_count += 1
            else:
                self._skip(f"Already exists -- Equation: {eq_data['name']}")
                skipped_count += 1
        self.stdout.write(f"     -> {created_count} created, {skipped_count} skipped")
