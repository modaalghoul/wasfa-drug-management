"""
================================================================================
Django Admin — Wasfa Drug Management System
================================================================================
Features:
  • Full inlines for all related models (DosageRule → RangeBasedDose, etc.)
  • autocomplete_fields for all FK/M2M selectors
  • list_select_related to prevent N+1 queries
  • Collapsible fieldsets for large forms
  • list_editable for quick inline editing
  • Readonly timestamps on all records
================================================================================
"""
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    PatientGroup, DrugCategory, DrugFamily, Manufacturer,
    GenericMedication, DosageRule, RangeBasedDose,
    TradeNameProduct, TradeNameComposition,
    DrugInteraction, MedicationAlternative,
    AgeWeightEstimate, Equation, EquationInput, SearchHistory,
)


# ══════════════════════════════════════════════════════════════
# Inlines
# ══════════════════════════════════════════════════════════════

class RangeBasedDoseInline(admin.TabularInline):
    model         = RangeBasedDose
    extra         = 1
    fields        = [
        'age_range_text', 'min_age_months', 'max_age_months',
        'weight_range_text', 'min_weight_kg', 'max_weight_kg',
        'dose_value', 'dose_description', 'display_order',
    ]
    ordering      = ['display_order']


class DosageRuleInline(admin.StackedInline):
    model         = DosageRule
    extra         = 0
    show_change_link = True          # allows opening the rule in its own page
    fields        = [
        ('label', 'patient_group', 'indication'),
        ('dose_calc_type', 'route'),
        ('formula_type', 'formula_factor', 'formula_divisor'),
        ('min_dose_mg', 'max_dose_mg', 'max_daily_dose_mg'),
        ('frequency_per_day', 'frequency_text'),
        ('min_age_months', 'max_age_months', 'age_limit_text'),
        ('min_weight_kg', 'max_weight_kg'),
        'usual_dose_text',
        'notes',
        'display_order',
    ]
    ordering      = ['display_order']


class TradeNameCompositionInline(admin.TabularInline):
    model               = TradeNameComposition
    extra               = 1
    autocomplete_fields = ['generic_medication']
    fields              = [
        'generic_medication', 'strength',
        'is_primary_ingredient', 'display_order',
    ]
    ordering            = ['display_order']


class EquationInputInline(admin.TabularInline):
    model    = EquationInput
    extra    = 1
    fields   = [
        'key', 'label', 'label_ar',
        'input_type', 'unit', 'options',
        'is_required', 'display_order',
    ]
    ordering = ['display_order']


# ══════════════════════════════════════════════════════════════
# 1. PatientGroup
# ══════════════════════════════════════════════════════════════
@admin.register(PatientGroup)
class PatientGroupAdmin(admin.ModelAdmin):
    list_display    = [
        'name', 'name_ar', 'display_order',
        'requires_weight_input', 'requires_age_input', 'created_at',
    ]
    list_editable   = ['display_order', 'requires_weight_input', 'requires_age_input']
    search_fields   = ['name', 'name_ar']
    readonly_fields = ['created_at']
    ordering        = ['display_order']
    fieldsets       = (
        (None, {
            'fields': ('name', 'name_ar', 'display_order', 'description', 'image_url')
        }),
        ('إعدادات الإدخال', {
            'fields': ('requires_weight_input', 'requires_age_input')
        }),
        ('معلومات النظام', {
            'classes': ('collapse',),
            'fields': ('created_at',)
        }),
    )


# ══════════════════════════════════════════════════════════════
# 2. DrugCategory
# ══════════════════════════════════════════════════════════════
@admin.register(DrugCategory)
class DrugCategoryAdmin(admin.ModelAdmin):
    list_display    = ['icon_display', 'name', 'name_ar', 'display_order', 'created_at']
    list_editable   = ['display_order']
    search_fields   = ['name', 'name_ar']
    readonly_fields = ['created_at']
    ordering        = ['display_order']
    fieldsets       = (
        (None, {
            'fields': ('name', 'name_ar', 'icon', 'display_order', 'description', 'image_url')
        }),
        ('معلومات النظام', {
            'classes': ('collapse',),
            'fields': ('created_at',)
        }),
    )

    @admin.display(description='أيقونة')
    def icon_display(self, obj):
        return format_html('<span style="font-size:1.4em">{}</span>', obj.icon or '💊')


# ══════════════════════════════════════════════════════════════
# 3. DrugFamily
# ══════════════════════════════════════════════════════════════
@admin.register(DrugFamily)
class DrugFamilyAdmin(admin.ModelAdmin):
    list_display        = ['name', 'name_ar', 'drug_category', 'display_order', 'created_at']
    list_filter         = ['drug_category']
    list_editable       = ['display_order']
    list_select_related = ['drug_category']
    search_fields       = ['name', 'name_ar']
    autocomplete_fields = ['drug_category']
    readonly_fields     = ['created_at']
    fieldsets           = (
        (None, {
            'fields': ('name', 'name_ar', 'drug_category', 'display_order', 'description')
        }),
        ('معلومات النظام', {
            'classes': ('collapse',),
            'fields': ('created_at',)
        }),
    )


# ══════════════════════════════════════════════════════════════
# 4. Manufacturer
# ══════════════════════════════════════════════════════════════
@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display    = ['name', 'name_ar', 'warehouse_name', 'country_of_manufacture', 'country_of_marketing']
    search_fields   = ['name', 'name_ar', 'warehouse_name']
    readonly_fields = ['created_at']
    fieldsets       = (
        ('المعلومات الأساسية', {
            'fields': ('name', 'name_ar', 'warehouse_name')
        }),
        ('الموقع', {
            'fields': ('country_of_manufacture', 'country_of_marketing', 'website')
        }),
        ('ملاحظات', {
            'classes': ('collapse',),
            'fields': ('notes',)
        }),
        ('معلومات النظام', {
            'classes': ('collapse',),
            'fields': ('created_at',)
        }),
    )


# ══════════════════════════════════════════════════════════════
# 5. GenericMedication
# ══════════════════════════════════════════════════════════════
@admin.register(GenericMedication)
class GenericMedicationAdmin(admin.ModelAdmin):
    list_display        = [
        'generic_name', 'generic_name_ar', 'drug_form',
        'drug_family', 'drug_category', 'patient_group',
        'pregnancy_category', 'updated_at',
    ]
    list_filter         = [
        'drug_category', 'patient_group', 'drug_form',
        'pregnancy_category', 'breastfeeding_compatible',
    ]
    list_select_related = ['drug_family', 'drug_category', 'patient_group']
    search_fields       = ['generic_name', 'generic_name_ar']
    autocomplete_fields = ['drug_family', 'drug_category', 'patient_group']
    readonly_fields     = ['created_at', 'updated_at']
    inlines             = [DosageRuleInline]
    list_per_page       = 30
    save_on_top         = True

    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': (
                ('generic_name', 'generic_name_ar'),
                ('drug_form', 'display_order_in_family'),
                ('drug_family', 'drug_category', 'patient_group'),
            )
        }),
        ('المعلومات الطبية', {
            'classes': ('collapse',),
            'fields': (
                'indications', 'contraindications', 'side_effects',
                'warnings', 'precautions', 'overdose_management',
            )
        }),
        ('الحمل والرضاعة', {
            'classes': ('collapse',),
            'fields': (
                ('pregnancy_category', 'breastfeeding_compatible'),
                'pregnancy_safety', 'lactation_safety', 'breastfeeding_notes',
            )
        }),
        ('ملاحظات الصيدلاني', {
            'classes': ('collapse',),
            'fields': ('notes', 'pharmacist_notes', 'show_estimated_weight')
        }),
        ('معلومات النظام', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )


# ══════════════════════════════════════════════════════════════
# 6. DosageRule (standalone — also editable via GenericMedication inline)
# ══════════════════════════════════════════════════════════════
@admin.register(DosageRule)
class DosageRuleAdmin(admin.ModelAdmin):
    list_display        = [
        'generic_medication', 'label', 'patient_group',
        'dose_calc_type', 'formula_type', 'formula_factor',
        'route', 'frequency_text', 'display_order',
    ]
    list_filter         = ['dose_calc_type', 'formula_type', 'route', 'patient_group']
    list_select_related = ['generic_medication', 'patient_group']
    search_fields       = [
        'generic_medication__generic_name',
        'generic_medication__generic_name_ar',
        'label', 'indication',
    ]
    autocomplete_fields = ['generic_medication', 'patient_group']
    readonly_fields     = ['created_at', 'updated_at']
    inlines             = [RangeBasedDoseInline]
    save_on_top         = True
    list_per_page       = 40

    fieldsets = (
        ('التصنيف', {
            'fields': (
                ('generic_medication', 'label'),
                ('patient_group', 'indication'),
                ('dose_calc_type', 'route'),
                'display_order',
            )
        }),
        ('المعادلة الحسابية', {
            'description': 'يُملأ عند اختيار "معادلة حسابية" كنوع حساب الجرعة.',
            'fields': (
                ('formula_type', 'formula_factor', 'formula_divisor'),
                ('min_dose_mg', 'max_dose_mg', 'max_daily_dose_mg'),
            )
        }),
        ('التكرار والمدة', {
            'fields': (
                ('frequency_per_day', 'frequency_text'),
                ('duration_days', 'duration_text'),
            )
        }),
        ('الحدود العمرية', {
            'classes': ('collapse',),
            'fields': (
                ('min_age_months', 'max_age_months', 'age_limit_text'),
                'age_below_limit_msg', 'age_above_limit_msg',
            )
        }),
        ('الحدود الوزنية', {
            'classes': ('collapse',),
            'fields': (
                ('min_weight_kg', 'max_weight_kg', 'weight_limit_text'),
                'weight_below_limit_msg', 'weight_above_limit_msg',
            )
        }),
        ('تحويل الوحدات', {
            'classes': ('collapse',),
            'fields': (
                'unit_conversion_enabled',
                ('unit_conversion_factor', 'unit_conversion_from', 'unit_conversion_to'),
            )
        }),
        ('الجرعة النصية (بالغين)', {
            'classes': ('collapse',),
            'fields': ('usual_dose_text', 'max_daily_dose_text')
        }),
        ('ملاحظات', {
            'classes': ('collapse',),
            'fields': ('notes',)
        }),
        ('معلومات النظام', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )


# ══════════════════════════════════════════════════════════════
# 7. TradeNameProduct
# ══════════════════════════════════════════════════════════════
@admin.register(TradeNameProduct)
class TradeNameProductAdmin(admin.ModelAdmin):
    list_display        = [
        'trade_name', 'trade_name_ar', 'drug_form', 'concentration',
        'drug_family', 'prescription_status', 'availability', 'price',
    ]
    list_filter         = [
        'drug_category', 'patient_group', 'drug_form',
        'prescription_status', 'availability',
    ]
    list_select_related = ['drug_family', 'drug_category', 'patient_group', 'manufacturer']
    search_fields       = ['trade_name', 'trade_name_ar', 'barcode']
    autocomplete_fields = ['manufacturer', 'drug_family', 'drug_category', 'patient_group']
    readonly_fields     = ['created_at', 'updated_at']
    inlines             = [TradeNameCompositionInline]
    save_on_top         = True
    list_per_page       = 40

    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': (
                ('trade_name', 'trade_name_ar'),
                ('drug_form', 'concentration'),
                ('drug_family', 'drug_category', 'patient_group'),
                ('manufacturer', 'display_order_in_family'),
            )
        }),
        ('البيع والسعر', {
            'fields': (
                ('prescription_status', 'availability'),
                ('price', 'price_with_tax'),
                ('package_size', 'barcode'),
                'prescription_status_notes',
            )
        }),
        ('الخصائص الفيزيائية', {
            'classes': ('collapse',),
            'fields': (
                ('can_be_crushed', 'can_be_cut', 'can_be_chewed'),
                'physical_modification_notes',
            )
        }),
        ('التخزين', {
            'classes': ('collapse',),
            'fields': (
                'storage_conditions', 'shelf_life', 'storage_after_opening'
            )
        }),
        ('الصور', {
            'classes': ('collapse',),
            'fields': ('package_image_url', 'leaflet_image_url', 'box_image_url')
        }),
        ('ملاحظات', {
            'classes': ('collapse',),
            'fields': ('notes', 'pharmacist_notes', 'show_estimated_weight')
        }),
        ('معلومات النظام', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )


# ══════════════════════════════════════════════════════════════
# 8. DrugInteraction
# ══════════════════════════════════════════════════════════════
@admin.register(DrugInteraction)
class DrugInteractionAdmin(admin.ModelAdmin):
    list_display        = ['drug_a', 'drug_b', 'severity_badge', 'reference']
    list_filter         = ['severity']
    list_select_related = ['drug_a', 'drug_b']
    search_fields       = [
        'drug_a__generic_name', 'drug_a__generic_name_ar',
        'drug_b__generic_name', 'drug_b__generic_name_ar',
    ]
    autocomplete_fields = ['drug_a', 'drug_b']
    readonly_fields     = ['created_at']

    SEVERITY_COLORS = {
        'mild': '#28a745',
        'moderate': '#fd7e14',
        'severe': '#dc3545',
        'contraindicated': '#6f0000',
    }

    @admin.display(description='الخطورة')
    def severity_badge(self, obj):
        color = self.SEVERITY_COLORS.get(obj.severity, '#666')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:4px;font-size:0.85em">{}</span>',
            color, obj.get_severity_display()
        )


# ══════════════════════════════════════════════════════════════
# 9. MedicationAlternative
# ══════════════════════════════════════════════════════════════
@admin.register(MedicationAlternative)
class MedicationAlternativeAdmin(admin.ModelAdmin):
    list_display        = [
        'source_generic', 'source_trade',
        'alternative_type',
        'alternative_generic', 'alternative_trade',
        'display_order',
    ]
    list_filter         = ['alternative_type']
    list_editable       = ['display_order']
    list_select_related = [
        'source_generic', 'source_trade',
        'alternative_generic', 'alternative_trade',
    ]
    autocomplete_fields = [
        'source_generic', 'source_trade',
        'alternative_generic', 'alternative_trade',
    ]
    readonly_fields     = ['created_at']
    search_fields       = [
        'source_generic__generic_name',
        'source_trade__trade_name',
        'alternative_generic__generic_name',
        'alternative_trade__trade_name',
    ]


# ══════════════════════════════════════════════════════════════
# 10. AgeWeightEstimate
# ══════════════════════════════════════════════════════════════
@admin.register(AgeWeightEstimate)
class AgeWeightEstimateAdmin(admin.ModelAdmin):
    list_display    = ['age_months', 'age_text', 'estimated_weight_kg', 'age_group']
    list_editable   = ['estimated_weight_kg', 'age_text']
    list_filter     = ['age_group']
    ordering        = ['age_months']
    readonly_fields = ['created_at']
    list_per_page   = 50


# ══════════════════════════════════════════════════════════════
# 11. Equation
# ══════════════════════════════════════════════════════════════
@admin.register(Equation)
class EquationAdmin(admin.ModelAdmin):
    list_display    = [
        'name', 'name_ar', 'category',
        'result_unit', 'display_order', 'is_active',
    ]
    list_filter     = ['category', 'is_active']
    list_editable   = ['display_order', 'is_active']
    search_fields   = ['name', 'name_ar', 'category']
    readonly_fields = ['created_at', 'updated_at']
    inlines         = [EquationInputInline]
    save_on_top     = True

    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': (
                ('name', 'name_ar'),
                ('category', 'display_order', 'is_active'),
                'formula_display',
                ('result_unit', 'result_label'),
            )
        }),
        ('الوصف', {
            'classes': ('collapse',),
            'fields': ('description', 'description_ar')
        }),
        ('التفسير', {
            'classes': ('collapse',),
            'fields': ('interpretation',),
            'description': 'JSON: [{"min":0,"max":30,"label":"Severe"},…]'
        }),
        ('المرجع العلمي', {
            'classes': ('collapse',),
            'fields': ('reference', 'reference_url')
        }),
        ('معلومات النظام', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )


# ══════════════════════════════════════════════════════════════
# 12. SearchHistory (read-only log)
# ══════════════════════════════════════════════════════════════
@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display    = ['search_query', 'search_type', 'result_count', 'searched_at']
    list_filter     = ['search_type']
    search_fields   = ['search_query']
    readonly_fields = ['search_query', 'search_type', 'result_count', 'searched_at']
    ordering        = ['-searched_at']

    def has_add_permission(self, request):
        return False  # log only — no manual entries
