"""
================================================================================
نظام إدارة الأدوية - Drug Management System
Django Models - Enhanced Version
================================================================================
التحسينات عن النسخة السابقة (SQLite):
  1. PatientGroup  ← إعادة تسمية categories لتجنب الالتباس
  2. DrugCategory  ← الأقسام الدوائية (Antibiotics / GIT / Respiratory…)
  3. DosageRule    ← جدول مستقل بدلاً من حقول مدمجة في generic_medications
  4. FormulaType   ← حقول منظمة بدلاً من dose_formula نصي حر
  5. DrugInteraction ← جدول منفصل بدلاً من حقل نصي
  6. Equation      ← جدول المعادلات الطبية (Creatinine Clearance, BSA…)
  7. حذف جدول users (تطبيق mobile محلي بمستخدم واحد)
================================================================================
"""

from django.db import models
from django.core.validators import MinValueValidator


# ============================================================
# Choices (بديل عن ENUM في SQLite)
# ============================================================

class DosageFormChoices(models.TextChoices):
    SUSPENSION  = 'suspension',  'معلق - Suspension'
    DROPS       = 'drops',       'نقط - Drops'
    SYRUP       = 'syrup',       'شراب - Syrup'
    SUPPOSITORY = 'suppository', 'تحاميل - Suppository'
    TABLET      = 'tablet',      'أقراص - Tablet'
    CAPSULE     = 'capsule',     'كبسول - Capsule'
    INJECTION   = 'injection',   'حقن - Injection'
    CREAM       = 'cream',       'كريم - Cream'
    OINTMENT    = 'ointment',    'مرهم - Ointment'
    INHALER     = 'inhaler',     'بخاخ - Inhaler'
    PATCH       = 'patch',       'لصقة - Patch'
    SOLUTION    = 'solution',    'محلول - Solution'
    OTHER       = 'other',       'أخرى - Other'


class RouteChoices(models.TextChoices):
    ORAL     = 'oral',     'فموي - Oral'
    IV       = 'iv',       'وريدي - IV'
    IM       = 'im',       'عضلي - IM'
    SC       = 'sc',       'تحت الجلد - SC'
    TOPICAL  = 'topical',  'موضعي - Topical'
    RECTAL   = 'rectal',   'مستقيمي - Rectal'
    INHALED  = 'inhaled',  'استنشاق - Inhaled'
    NASAL    = 'nasal',    'أنفي - Nasal'
    OPHTHALMIC = 'ophthalmic', 'عيني - Ophthalmic'
    OTIC     = 'otic',     'أذني - Otic'


class FormulaTypeChoices(models.TextChoices):
    PER_KG          = 'per_kg',          'mg/kg مرة واحدة'
    PER_KG_DIVIDED  = 'per_kg_divided',  'mg/kg مقسّمة على الجرعات'
    FIXED_RANGE     = 'fixed_range',     'جرعة ثابتة محددة'
    AGE_BASED       = 'age_based',       'حسب العمر فقط'


class DoseCalcTypeChoices(models.TextChoices):
    FORMULA     = 'formula',     'معادلة حسابية'
    TEXT        = 'text',        'نصي (للبالغين)'
    RANGE_BASED = 'range_based', 'نطاقات محددة (تحاميل…)'


class AlternativeTypeChoices(models.TextChoices):
    EQUIVALENT        = 'equivalent',        'مكافئ تماماً'
    THERAPEUTIC       = 'therapeutic',       'بديل علاجي'
    COST_EFFECTIVE    = 'cost_effective',     'بديل اقتصادي'


class SeverityChoices(models.TextChoices):
    MILD     = 'mild',     'خفيف'
    MODERATE = 'moderate', 'متوسط'
    SEVERE   = 'severe',   'شديد'


class AvailabilityChoices(models.TextChoices):
    GOOD        = 'good',        'متوفر جيد'
    MEDIUM      = 'medium',      'متوفر متوسط'
    UNAVAILABLE = 'unavailable', 'غير متوفر'


class PrescriptionStatusChoices(models.TextChoices):
    OTC        = 'OTC',        'بدون وصفة'
    RX         = 'RX',         'بوصفة طبية'
    CONTROLLED = 'controlled', 'مراقب'


class PregnancyCategoryChoices(models.TextChoices):
    A = 'A', 'Category A - آمن'
    B = 'B', 'Category B - آمن على الأرجح'
    C = 'C', 'Category C - احتياط'
    D = 'D', 'Category D - خطر موثق'
    X = 'X', 'Category X - ممنوع'


class InteractionSeverityChoices(models.TextChoices):
    MILD         = 'mild',         'خفيف - لا يستدعي تعديل'
    MODERATE     = 'moderate',     'متوسط - يستدعي متابعة'
    SEVERE       = 'severe',       'شديد - يستدعي تجنب الدمج'
    CONTRAINDICATED = 'contraindicated', 'ممنوع - لا يجمعان أبداً'


class EquationInputTypeChoices(models.TextChoices):
    NUMBER  = 'number',  'رقم'
    SELECT  = 'select',  'اختيار (ذكر/أنثى…)'
    BOOLEAN = 'boolean', 'نعم / لا'


# ============================================================
# 1. PatientGroup — فئات المرضى
# ============================================================
class PatientGroup(models.Model):
    name                   = models.CharField(max_length=100, unique=True)
    name_ar                = models.CharField(max_length=100, blank=True)
    description            = models.TextField(blank=True)
    image_url              = models.TextField(blank=True)
    display_order          = models.PositiveIntegerField(default=0)
    requires_weight_input  = models.BooleanField(default=False)
    requires_age_input     = models.BooleanField(default=False)
    created_at             = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'فئة مريض'
        verbose_name_plural = 'فئات المرضى'

    def __str__(self):
        return self.name_ar or self.name


# ============================================================
# 2. DrugCategory — الأقسام الدوائية
# ============================================================
class DrugCategory(models.Model):
    name          = models.CharField(max_length=100, unique=True)
    name_ar       = models.CharField(max_length=100, blank=True)
    description   = models.TextField(blank=True)
    icon          = models.CharField(max_length=100, blank=True)
    image_url     = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'قسم دوائي'
        verbose_name_plural = 'الأقسام الدوائية'

    def __str__(self):
        return self.name_ar or self.name


# ============================================================
# 3. DrugFamily — العائلات الدوائية
# ============================================================
class DrugFamily(models.Model):
    name          = models.CharField(max_length=200)
    name_ar       = models.CharField(max_length=200, blank=True)
    description   = models.TextField(blank=True)
    drug_category = models.ForeignKey(
        DrugCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='families'
    )
    display_order = models.PositiveIntegerField(default=0)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['drug_category', 'display_order', 'name']
        verbose_name = 'عائلة دوائية'
        verbose_name_plural = 'العائلات الدوائية'

    def __str__(self):
        return f"{self.name_ar or self.name}"


# ============================================================
# 4. Manufacturer — الشركات المصنّعة
# ============================================================
class Manufacturer(models.Model):
    name                      = models.CharField(max_length=200, unique=True)
    name_ar                   = models.CharField(max_length=200, blank=True)
    warehouse_name            = models.CharField(max_length=200, blank=True)
    country_of_manufacture    = models.CharField(max_length=100, blank=True)
    country_of_marketing      = models.CharField(max_length=100, blank=True)
    website                   = models.URLField(blank=True)
    notes                     = models.TextField(blank=True)
    created_at                = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'شركة مصنّعة'
        verbose_name_plural = 'الشركات المصنّعة'

    def __str__(self):
        return self.name_ar or self.name


# ============================================================
# 5. GenericMedication — الاسم العلمي / المادة الفعّالة
# ============================================================
class GenericMedication(models.Model):
    generic_name    = models.CharField(max_length=300)
    generic_name_ar = models.CharField(max_length=300, blank=True)
    drug_form       = models.CharField(
        max_length=100,
        choices=DosageFormChoices.choices,
        blank=True
    )
    drug_family     = models.ForeignKey(
        DrugFamily,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='medications'
    )
    drug_category   = models.ForeignKey(
        DrugCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='medications'
    )
    patient_group   = models.ForeignKey(
        PatientGroup,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='medications'
    )
    display_order_in_family = models.PositiveIntegerField(default=0)

    indications            = models.TextField(blank=True)
    contraindications      = models.TextField(blank=True)
    side_effects           = models.TextField(blank=True)
    warnings               = models.TextField(blank=True)
    precautions            = models.TextField(blank=True)
    overdose_management    = models.TextField(blank=True)

    pregnancy_category     = models.CharField(
        max_length=5,
        choices=PregnancyCategoryChoices.choices,
        blank=True
    )
    pregnancy_safety       = models.TextField(blank=True)
    lactation_safety       = models.TextField(blank=True)
    breastfeeding_compatible = models.BooleanField(null=True, blank=True)
    breastfeeding_notes    = models.TextField(blank=True)

    notes                  = models.TextField(blank=True)
    pharmacist_notes       = models.TextField(blank=True)
    show_estimated_weight  = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['drug_family', 'display_order_in_family', 'generic_name']
        verbose_name = 'دواء (اسم علمي)'
        verbose_name_plural = 'الأدوية (أسماء علمية)'

    def __str__(self):
        return f"{self.generic_name} ({self.drug_form})"


# ============================================================
# 6. DosageRule — قواعد الجرعة
# ============================================================
class DosageRule(models.Model):
    generic_medication = models.ForeignKey(
        GenericMedication,
        on_delete=models.CASCADE,
        related_name='dosage_rules'
    )

    label         = models.CharField(max_length=200, blank=True)
    patient_group = models.ForeignKey(
        PatientGroup,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='dosage_rules'
    )
    indication    = models.CharField(max_length=300, blank=True)

    dose_calc_type = models.CharField(
        max_length=20,
        choices=DoseCalcTypeChoices.choices,
        default=DoseCalcTypeChoices.FORMULA
    )

    formula_type    = models.CharField(
        max_length=30,
        choices=FormulaTypeChoices.choices,
        blank=True
    )
    formula_factor  = models.DecimalField(
        max_digits=8, decimal_places=3,
        null=True, blank=True
    )
    formula_divisor = models.PositiveIntegerField(
        null=True, blank=True
    )
    min_dose_mg     = models.DecimalField(
        max_digits=8, decimal_places=2,
        null=True, blank=True
    )
    max_dose_mg     = models.DecimalField(
        max_digits=8, decimal_places=2,
        null=True, blank=True
    )
    max_daily_dose_mg = models.DecimalField(
        max_digits=8, decimal_places=2,
        null=True, blank=True
    )

    usual_dose_text     = models.TextField(blank=True)
    max_daily_dose_text = models.TextField(blank=True)

    frequency_per_day = models.PositiveIntegerField(
        null=True, blank=True
    )
    frequency_text    = models.CharField(max_length=200, blank=True)
    duration_days     = models.PositiveIntegerField(null=True, blank=True)
    duration_text     = models.CharField(max_length=200, blank=True)

    route = models.CharField(
        max_length=20,
        choices=RouteChoices.choices,
        default=RouteChoices.ORAL
    )

    min_age_months        = models.PositiveIntegerField(null=True, blank=True)
    max_age_months        = models.PositiveIntegerField(null=True, blank=True)
    age_limit_text        = models.CharField(max_length=200, blank=True)
    age_below_limit_msg   = models.TextField(blank=True)
    age_above_limit_msg   = models.TextField(blank=True)

    min_weight_kg         = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True
    )
    max_weight_kg         = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True
    )
    weight_limit_text     = models.CharField(max_length=200, blank=True)
    weight_below_limit_msg = models.TextField(blank=True)
    weight_above_limit_msg = models.TextField(blank=True)

    unit_conversion_enabled  = models.BooleanField(default=False)
    unit_conversion_factor   = models.DecimalField(
        max_digits=8, decimal_places=4,
        null=True, blank=True
    )
    unit_conversion_from     = models.CharField(max_length=50, blank=True)
    unit_conversion_to       = models.CharField(max_length=50, blank=True)

    notes          = models.TextField(blank=True)
    display_order  = models.PositiveIntegerField(default=0)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['generic_medication', 'display_order']
        verbose_name = 'قاعدة جرعة'
        verbose_name_plural = 'قواعد الجرعات'

    def __str__(self):
        return f"{self.generic_medication} — {self.label or self.dose_calc_type}"

    def calculate_dose(self, weight_kg: float) -> dict:
        if self.dose_calc_type != DoseCalcTypeChoices.FORMULA:
            return {}

        factor  = float(self.formula_factor or 0)
        divisor = self.formula_divisor or 1

        if self.formula_type == FormulaTypeChoices.PER_KG:
            single_dose = factor * weight_kg
        elif self.formula_type == FormulaTypeChoices.PER_KG_DIVIDED:
            single_dose = (factor * weight_kg) / divisor
        else:
            return {}

        if self.min_dose_mg:
            single_dose = max(single_dose, float(self.min_dose_mg))
        if self.max_dose_mg:
            single_dose = min(single_dose, float(self.max_dose_mg))

        daily_dose = single_dose * (self.frequency_per_day or divisor)
        if self.max_daily_dose_mg:
            daily_dose = min(daily_dose, float(self.max_daily_dose_mg))

        return {
            'single_dose_mg': round(single_dose, 2),
            'daily_dose_mg':  round(daily_dose, 2),
            'frequency':      self.frequency_text or f"{self.frequency_per_day}x/day",
        }


# ============================================================
# 7. RangeBasedDose — الجرعات بالنطاق
# ============================================================
class RangeBasedDose(models.Model):
    dosage_rule    = models.ForeignKey(
        DosageRule,
        on_delete=models.CASCADE,
        related_name='range_doses'
    )

    min_age_months  = models.PositiveIntegerField(null=True, blank=True)
    max_age_months  = models.PositiveIntegerField(null=True, blank=True)
    age_range_text  = models.CharField(max_length=100, blank=True)

    min_weight_kg   = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    max_weight_kg   = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight_range_text = models.CharField(max_length=100, blank=True)

    dose_value      = models.CharField(max_length=100)
    dose_description = models.TextField(blank=True)
    display_order   = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['dosage_rule', 'display_order']
        verbose_name = 'جرعة بالنطاق'
        verbose_name_plural = 'جرعات بالنطاق'

    def __str__(self):
        return f"{self.dosage_rule} | {self.age_range_text or self.weight_range_text} → {self.dose_value}"


# ============================================================
# 8. TradeNameProduct — الأسماء التجارية
# ============================================================
class TradeNameProduct(models.Model):
    trade_name    = models.CharField(max_length=300)
    trade_name_ar = models.CharField(max_length=300, blank=True)
    manufacturer  = models.ForeignKey(
        Manufacturer,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='products'
    )
    drug_form     = models.CharField(
        max_length=100,
        choices=DosageFormChoices.choices,
        blank=True
    )
    concentration = models.CharField(max_length=100, blank=True)
    drug_family   = models.ForeignKey(
        DrugFamily,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='trade_products'
    )
    drug_category = models.ForeignKey(
        DrugCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='trade_products'
    )
    patient_group = models.ForeignKey(
        PatientGroup,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='trade_products'
    )
    display_order_in_family = models.PositiveIntegerField(default=0)

    prescription_status = models.CharField(
        max_length=20,
        choices=PrescriptionStatusChoices.choices,
        default=PrescriptionStatusChoices.OTC
    )
    prescription_status_notes = models.TextField(blank=True)
    availability = models.CharField(
        max_length=20,
        choices=AvailabilityChoices.choices,
        default=AvailabilityChoices.GOOD
    )
    price          = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_with_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    package_size   = models.CharField(max_length=100, blank=True)
    barcode        = models.CharField(max_length=100, blank=True)

    can_be_crushed  = models.BooleanField(null=True, blank=True)
    can_be_cut      = models.BooleanField(null=True, blank=True)
    can_be_chewed   = models.BooleanField(null=True, blank=True)
    physical_modification_notes = models.TextField(blank=True)

    storage_conditions    = models.TextField(blank=True)
    shelf_life            = models.CharField(max_length=100, blank=True)
    storage_after_opening = models.CharField(max_length=200, blank=True)

    package_image_url  = models.TextField(blank=True)
    leaflet_image_url  = models.TextField(blank=True)
    box_image_url      = models.TextField(blank=True)

    notes            = models.TextField(blank=True)
    pharmacist_notes = models.TextField(blank=True)
    show_estimated_weight = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['drug_family', 'display_order_in_family', 'trade_name']
        verbose_name = 'اسم تجاري'
        verbose_name_plural = 'الأسماء التجارية'

    def __str__(self):
        return f"{self.trade_name} ({self.drug_form})"


# ============================================================
# 9. TradeNameComposition — تركيبة الاسم التجاري
# ============================================================
class TradeNameComposition(models.Model):
    trade_name          = models.ForeignKey(
        TradeNameProduct,
        on_delete=models.CASCADE,
        related_name='compositions'
    )
    generic_medication  = models.ForeignKey(
        GenericMedication,
        on_delete=models.CASCADE,
        related_name='in_products'
    )
    strength            = models.CharField(max_length=100, blank=True)
    is_primary_ingredient = models.BooleanField(default=False)
    display_order       = models.PositiveIntegerField(default=0)
    created_at          = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('trade_name', 'generic_medication')
        ordering = ['trade_name', 'display_order']
        verbose_name = 'تركيبة اسم تجاري'
        verbose_name_plural = 'تركيبات الأسماء التجارية'

    def __str__(self):
        return f"{self.trade_name} ← {self.generic_medication} ({self.strength})"


# ============================================================
# 10. DrugInteraction — التفاعلات الدوائية
# ============================================================
class DrugInteraction(models.Model):
    drug_a      = models.ForeignKey(
        GenericMedication,
        on_delete=models.CASCADE,
        related_name='interactions_as_a'
    )
    drug_b      = models.ForeignKey(
        GenericMedication,
        on_delete=models.CASCADE,
        related_name='interactions_as_b'
    )
    severity    = models.CharField(
        max_length=20,
        choices=InteractionSeverityChoices.choices
    )
    description = models.TextField()
    management  = models.TextField(blank=True)
    reference   = models.CharField(max_length=300, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('drug_a', 'drug_b')
        ordering = ['-severity']
        verbose_name = 'تفاعل دوائي'
        verbose_name_plural = 'التفاعلات الدوائية'

    def __str__(self):
        return f"{self.drug_a.generic_name} ↔ {self.drug_b.generic_name} ({self.severity})"


# ============================================================
# 11. MedicationAlternative — البدائل الدوائية
# ============================================================
class MedicationAlternative(models.Model):
    source_generic      = models.ForeignKey(
        GenericMedication,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='alternatives_as_source'
    )
    source_trade        = models.ForeignKey(
        TradeNameProduct,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='alternatives_as_source'
    )
    alternative_generic = models.ForeignKey(
        GenericMedication,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='alternatives_as_target'
    )
    alternative_trade   = models.ForeignKey(
        TradeNameProduct,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='alternatives_as_target'
    )
    alternative_type    = models.CharField(
        max_length=30,
        choices=AlternativeTypeChoices.choices
    )
    notes         = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order']
        verbose_name = 'بديل دوائي'
        verbose_name_plural = 'البدائل الدوائية'

    def __str__(self):
        src = self.source_generic or self.source_trade
        alt = self.alternative_generic or self.alternative_trade
        return f"{src} → {alt} ({self.alternative_type})"


# ============================================================
# 12. AgeWeightEstimate — تقدير الوزن حسب العمر
# ============================================================
class AgeWeightEstimate(models.Model):
    age_months          = models.PositiveIntegerField(unique=True)
    age_text            = models.CharField(max_length=50, blank=True)
    estimated_weight_kg = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    age_group = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['age_months']
        verbose_name = 'تقدير وزن حسب العمر'
        verbose_name_plural = 'تقديرات الأوزان حسب العمر'

    def __str__(self):
        return f"{self.age_text} → {self.estimated_weight_kg} kg"


# ============================================================
# 13. EquationInput — مدخلات المعادلة
# ============================================================
class EquationInput(models.Model):
    equation    = models.ForeignKey(
        'Equation',
        on_delete=models.CASCADE,
        related_name='inputs'
    )
    key         = models.CharField(max_length=50)
    label       = models.CharField(max_length=100)
    label_ar    = models.CharField(max_length=100, blank=True)
    input_type  = models.CharField(
        max_length=20,
        choices=EquationInputTypeChoices.choices,
        default=EquationInputTypeChoices.NUMBER
    )
    unit        = models.CharField(max_length=30, blank=True)
    options     = models.JSONField(null=True, blank=True)
    is_required = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['equation', 'display_order']

    def __str__(self):
        return f"{self.equation} → {self.key} ({self.unit})"


# ============================================================
# 14. Equation — المعادلات الطبية
# ============================================================
class Equation(models.Model):
    name         = models.CharField(max_length=200)
    name_ar      = models.CharField(max_length=200, blank=True)
    description  = models.TextField(blank=True)
    description_ar = models.TextField(blank=True)

    formula_display = models.TextField(blank=True)

    result_unit  = models.CharField(max_length=50, blank=True)
    result_label = models.CharField(max_length=100, blank=True)

    interpretation = models.JSONField(null=True, blank=True)

    reference    = models.CharField(max_length=500, blank=True)
    reference_url = models.URLField(blank=True)

    category     = models.CharField(max_length=100, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active    = models.BooleanField(default=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'معادلة طبية'
        verbose_name_plural = 'المعادلات الطبية'

    def __str__(self):
        return self.name_ar or self.name


# ============================================================
# 15. SearchHistory — سجل البحث
# ============================================================
class SearchHistory(models.Model):
    search_query = models.CharField(max_length=500)
    search_type  = models.CharField(max_length=50, blank=True)
    result_count = models.PositiveIntegerField(default=0)
    searched_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-searched_at']
        verbose_name = 'سجل بحث'
        verbose_name_plural = 'سجل البحث'

    def __str__(self):
        return f'"{self.search_query}" ({self.searched_at.strftime("%Y-%m-%d")})'
