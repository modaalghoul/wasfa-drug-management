from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    PatientGroup, DrugCategory, DrugFamily, Manufacturer,
    GenericMedication, DosageRule, RangeBasedDose,
    TradeNameProduct, TradeNameComposition,
    DrugInteraction, MedicationAlternative,
    AgeWeightEstimate, Equation, EquationInput, SearchHistory,
)


# ── Inlines ──────────────────────────────────────────────────

class EquationInputInline(admin.TabularInline):
    model   = EquationInput
    extra   = 1
    fields  = ['key', 'label', 'label_ar', 'input_type', 'unit', 'is_required', 'display_order']
    ordering = ['display_order']


class DosageRuleInline(admin.StackedInline):
    model   = DosageRule
    extra   = 0
    fields  = [
        'label', 'patient_group', 'indication', 'dose_calc_type',
        'formula_type', 'formula_factor', 'formula_divisor',
        'min_dose_mg', 'max_dose_mg', 'max_daily_dose_mg',
        'frequency_per_day', 'frequency_text', 'route',
        'min_age_months', 'max_age_months',
        'min_weight_kg', 'max_weight_kg',
        'usual_dose_text', 'notes',
    ]


class RangeBasedDoseInline(admin.TabularInline):
    model   = RangeBasedDose
    extra   = 1
    fields  = ['age_range_text', 'weight_range_text', 'dose_value', 'dose_description', 'display_order']


class TradeNameCompositionInline(admin.TabularInline):
    model   = TradeNameComposition
    extra   = 1
    fields  = ['generic_medication', 'strength', 'is_primary_ingredient', 'display_order']


# ── ModelAdmins ──────────────────────────────────────────────

@admin.register(PatientGroup)
class PatientGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_ar', 'requires_weight_input', 'requires_age_input', 'display_order')
    list_filter = ('requires_weight_input', 'requires_age_input')
    search_fields = ('name', 'name_ar')
    fieldsets = (
        (_('Basic Info'), {
            'fields': ('name', 'name_ar', 'display_order')
        }),
        (_('Settings'), {
            'fields': ('requires_weight_input', 'requires_age_input', 'description')
        }),
        (_('Media'), {
            'fields': ('image_url',)
        }),
    )


@admin.register(DrugCategory)
class DrugCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_ar', 'icon', 'display_order')
    list_filter = ('display_order',)
    search_fields = ('name', 'name_ar')
    fieldsets = (
        (_('Basic Info'), {
            'fields': ('name', 'name_ar', 'display_order')
        }),
        (_('Details'), {
            'fields': ('icon', 'description', 'image_url')
        }),
    )


@admin.register(DrugFamily)
class DrugFamilyAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_ar', 'drug_category', 'display_order')
    list_filter = ('drug_category', 'display_order')
    search_fields = ('name', 'name_ar')
    fieldsets = (
        (_('Basic Info'), {
            'fields': ('name', 'name_ar', 'drug_category', 'display_order')
        }),
        (_('Details'), {
            'fields': ('description',)
        }),
    )


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_ar', 'country_of_manufacture')
    list_filter = ('country_of_manufacture',)
    search_fields = ('name', 'name_ar')
    fieldsets = (
        (_('Basic Info'), {
            'fields': ('name', 'name_ar')
        }),
        (_('Address'), {
            'fields': ('warehouse_name', 'country_of_manufacture', 'country_of_marketing')
        }),
        (_('Contact'), {
            'fields': ('website',)
        }),
        (_('Notes'), {
            'fields': ('notes',)
        }),
    )


@admin.register(GenericMedication)
class GenericMedicationAdmin(admin.ModelAdmin):
    list_display = ('generic_name', 'generic_name_ar', 'drug_form', 'drug_category', 'drug_family')
    list_filter = ('drug_form', 'drug_category', 'drug_family')
    search_fields = ('generic_name', 'generic_name_ar')
    inlines = [DosageRuleInline]
    fieldsets = (
        (_('Basic Info'), {
            'fields': ('generic_name', 'generic_name_ar', 'drug_form', 'drug_category', 'drug_family', 'patient_group', 'display_order_in_family')
        }),
        (_('Medical Info'), {
            'fields': ('indications', 'contraindications', 'side_effects', 'warnings', 'precautions', 'overdose_management')
        }),
        (_('Pregnancy & Lactation'), {
            'fields': ('pregnancy_category', 'pregnancy_safety', 'breastfeeding_compatible', 'lactation_safety', 'breastfeeding_notes')
        }),
        (_('Notes'), {
            'fields': ('notes', 'pharmacist_notes', 'show_estimated_weight'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DosageRule)
class DosageRuleAdmin(admin.ModelAdmin):
    list_display = ('generic_medication', 'label', 'patient_group', 'route', 'dose_calc_type')
    list_filter = ('dose_calc_type', 'route', 'patient_group')
    search_fields = ('label', 'generic_medication__generic_name')
    inlines = [RangeBasedDoseInline]
    fieldsets = (
        (_('Medication'), {
            'fields': ('generic_medication', 'label', 'patient_group', 'indication')
        }),
        (_('Dose Calculation'), {
            'fields': ('dose_calc_type', 'formula_type', 'formula_factor', 'formula_divisor')
        }),
        (_('Dose Limits'), {
            'fields': ('min_dose_mg', 'max_dose_mg', 'max_daily_dose_mg'),
            'classes': ('collapse',)
        }),
        (_('Route & Frequency'), {
            'fields': ('route', 'frequency_per_day', 'frequency_text', 'duration_days', 'duration_text')
        }),
        (_('Age Limits'), {
            'fields': ('min_age_months', 'max_age_months', 'age_limit_text', 'age_below_limit_msg', 'age_above_limit_msg'),
            'classes': ('collapse',)
        }),
        (_('Weight Limits'), {
            'fields': ('min_weight_kg', 'max_weight_kg', 'weight_limit_text', 'weight_below_limit_msg', 'weight_above_limit_msg'),
            'classes': ('collapse',)
        }),
        (_('Unit Conversion'), {
            'fields': ('unit_conversion_enabled', 'unit_conversion_factor', 'unit_conversion_from', 'unit_conversion_to'),
            'classes': ('collapse',)
        }),
        (_('Notes'), {
            'fields': ('notes', 'display_order'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TradeNameProduct)
class TradeNameProductAdmin(admin.ModelAdmin):
    list_display = ('trade_name', 'trade_name_ar', 'manufacturer', 'availability', 'price')
    list_filter = ('availability', 'prescription_status', 'manufacturer')
    search_fields = ('trade_name', 'trade_name_ar')
    inlines = [TradeNameCompositionInline]
    fieldsets = (
        (_('Product Info'), {
            'fields': ('trade_name', 'trade_name_ar', 'manufacturer', 'drug_form', 'concentration', 'drug_category', 'drug_family')
        }),
        (_('Sales Info'), {
            'fields': ('prescription_status', 'prescription_status_notes', 'availability', 'price', 'price_with_tax', 'package_size', 'barcode')
        }),
        (_('Physical Properties'), {
            'fields': ('can_be_crushed', 'can_be_cut', 'can_be_chewed', 'physical_modification_notes'),
            'classes': ('collapse',)
        }),
        (_('Storage'), {
            'fields': ('storage_conditions', 'shelf_life', 'storage_after_opening'),
            'classes': ('collapse',)
        }),
        (_('Images'), {
            'fields': ('package_image_url', 'leaflet_image_url', 'box_image_url'),
            'classes': ('collapse',)
        }),
        (_('Notes'), {
            'fields': ('notes', 'pharmacist_notes', 'show_estimated_weight', 'display_order_in_family'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RangeBasedDose)
class RangeBasedDoseAdmin(admin.ModelAdmin):
    list_display = ('dosage_rule', 'age_range_text', 'weight_range_text', 'dose_value')
    list_filter = ('dosage_rule',)
    search_fields = ('dosage_rule__generic_medication__generic_name',)


@admin.register(TradeNameComposition)
class TradeNameCompositionAdmin(admin.ModelAdmin):
    list_display = ('trade_name', 'generic_medication', 'strength', 'is_primary_ingredient')
    list_filter = ('is_primary_ingredient',)
    search_fields = ('trade_name__trade_name', 'generic_medication__generic_name')


@admin.register(DrugInteraction)
class DrugInteractionAdmin(admin.ModelAdmin):
    list_display = ('drug_a', 'drug_b', 'severity')
    list_filter = ('severity',)
    search_fields = ('drug_a__generic_name', 'drug_b__generic_name')
    fieldsets = (
        (_('Drugs'), {
            'fields': ('drug_a', 'drug_b')
        }),
        (_('Interaction Details'), {
            'fields': ('severity', 'description', 'management', 'reference')
        }),
    )


@admin.register(MedicationAlternative)
class MedicationAlternativeAdmin(admin.ModelAdmin):
    list_display = ('source_generic', 'source_trade', 'alternative_type')
    list_filter = ('alternative_type',)
    search_fields = ('source_generic__generic_name', 'source_trade__trade_name')


@admin.register(AgeWeightEstimate)
class AgeWeightEstimateAdmin(admin.ModelAdmin):
    list_display = ('age_months', 'age_text', 'estimated_weight_kg', 'age_group')
    list_filter = ('age_group',)
    search_fields = ('age_text',)
    ordering = ('age_months',)


@admin.register(Equation)
class EquationAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_ar', 'result_label', 'is_active')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'name_ar')
    inlines = [EquationInputInline]
    fieldsets = (
        (_('Basic Info'), {
            'fields': ('name', 'name_ar', 'category', 'is_active')
        }),
        (_('Description'), {
            'fields': ('description', 'description_ar')
        }),
        (_('Formula'), {
            'fields': ('formula_display', 'result_unit', 'result_label')
        }),
        (_('Interpretation'), {
            'fields': ('interpretation',)
        }),
        (_('Reference'), {
            'fields': ('reference', 'reference_url')
        }),
        (_('Display'), {
            'fields': ('display_order',)
        }),
    )


@admin.register(EquationInput)
class EquationInputAdmin(admin.ModelAdmin):
    list_display = ('equation', 'key', 'label', 'input_type', 'is_required')
    list_filter = ('equation', 'input_type', 'is_required')
    search_fields = ('key', 'label')
    ordering = ('equation', 'display_order')


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('search_query', 'search_type', 'result_count', 'searched_at')
    list_filter = ('search_type', 'searched_at')
    search_fields = ('search_query',)
    readonly_fields = ('search_query', 'search_type', 'result_count', 'searched_at')
    ordering = ('-searched_at',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
