from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from .models import (
    PatientGroup, DrugCategory, DrugFamily, Manufacturer, GenericMedication,
    DosageRule, RangeBasedDose, TradeNameProduct, TradeNameComposition,
    DrugInteraction, MedicationAlternative, AgeWeightEstimate, Equation,
    EquationInput, SearchHistory
)


# ─── Shared widget helpers ────────────────────────────────────────────────────

def fc(extra='', **attrs):
    """Return form-control class attrs, merging extras."""
    return {'class': f'form-control {extra}'.strip(), **attrs}

def sel(**attrs):
    """Select with form-control + select2."""
    return {'class': 'form-control form-select select2', **attrs}

def ar_input(**attrs):
    """Text input styled for Arabic (RTL, Cairo font)."""
    return {'class': 'form-control arabic-field', 'dir': 'auto', **attrs}

def ar_area(rows=3, **attrs):
    """Textarea styled for Arabic."""
    return {'class': 'form-control arabic-field', 'dir': 'auto', 'rows': rows, **attrs}


# ─── PatientGroup ─────────────────────────────────────────────────────────────

class PatientGroupForm(forms.ModelForm):
    class Meta:
        model = PatientGroup
        fields = ['name', 'name_ar', 'description', 'image_url',
                  'display_order', 'requires_weight_input', 'requires_age_input']
        widgets = {
            'name':                  forms.TextInput(attrs=fc(placeholder=_('e.g. pediatric'))),
            'name_ar':               forms.TextInput(attrs=ar_input(placeholder='مثال: أطفال')),
            'description':           forms.Textarea(attrs=fc(rows=3)),
            'image_url':             forms.URLInput(attrs=fc()),
            'display_order':         forms.NumberInput(attrs=fc()),
            'requires_weight_input': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'requires_age_input':    forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ─── DrugCategory ─────────────────────────────────────────────────────────────

class DrugCategoryForm(forms.ModelForm):
    class Meta:
        model = DrugCategory
        fields = ['name', 'name_ar', 'description', 'icon', 'image_url', 'display_order']
        widgets = {
            'name':          forms.TextInput(attrs=fc(placeholder=_('e.g. Antibiotic Drugs'))),
            'name_ar':       forms.TextInput(attrs=ar_input(placeholder='مثال: المضادات الحيوية')),
            'description':   forms.Textarea(attrs=fc(rows=3)),
            'icon':          forms.TextInput(attrs=fc(placeholder='🦠')),
            'image_url':     forms.URLInput(attrs=fc()),
            'display_order': forms.NumberInput(attrs=fc()),
        }


# ─── DrugFamily ───────────────────────────────────────────────────────────────

class DrugFamilyForm(forms.ModelForm):
    class Meta:
        model = DrugFamily
        fields = ['name', 'name_ar', 'description', 'drug_category', 'display_order']
        widgets = {
            'name':          forms.TextInput(attrs=fc(placeholder=_('e.g. Penicillins'))),
            'name_ar':       forms.TextInput(attrs=ar_input(placeholder='مثال: بنسيلينات')),
            'description':   forms.Textarea(attrs=fc(rows=3)),
            'drug_category': forms.Select(attrs=sel()),
            'display_order': forms.NumberInput(attrs=fc()),
        }


# ─── Manufacturer ─────────────────────────────────────────────────────────────

class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ['name', 'name_ar', 'warehouse_name', 'country_of_manufacture',
                  'country_of_marketing', 'website', 'notes']
        widgets = {
            'name':                   forms.TextInput(attrs=fc()),
            'name_ar':                forms.TextInput(attrs=ar_input()),
            'warehouse_name':         forms.TextInput(attrs=fc()),
            'country_of_manufacture': forms.TextInput(attrs=fc()),
            'country_of_marketing':   forms.TextInput(attrs=fc()),
            'website':                forms.URLInput(attrs=fc()),
            'notes':                  forms.Textarea(attrs=fc(rows=3)),
        }


# ─── GenericMedication ────────────────────────────────────────────────────────

class GenericMedicationForm(forms.ModelForm):
    class Meta:
        model = GenericMedication
        fields = [
            'generic_name', 'generic_name_ar', 'drug_form',
            'drug_family', 'drug_category', 'patient_group',
            'display_order_in_family',
            'indications', 'contraindications', 'side_effects',
            'warnings', 'precautions', 'overdose_management',
            'pregnancy_category', 'pregnancy_safety', 'lactation_safety',
            'breastfeeding_compatible', 'breastfeeding_notes',
            'notes', 'pharmacist_notes', 'show_estimated_weight',
        ]
        widgets = {
            'generic_name':            forms.TextInput(attrs=fc(placeholder=_('e.g. Amoxicillin'))),
            'generic_name_ar':         forms.TextInput(attrs=ar_input(placeholder='مثال: أموكسيسيلين')),
            'drug_form':               forms.Select(attrs=sel()),
            'drug_family':             forms.Select(attrs=sel()),
            'drug_category':           forms.Select(attrs=sel()),
            'patient_group':           forms.Select(attrs=sel()),
            'display_order_in_family': forms.NumberInput(attrs=fc()),
            'indications':             forms.Textarea(attrs=fc(rows=3, placeholder=_('What conditions this drug treats...'))),
            'contraindications':       forms.Textarea(attrs=fc(rows=3)),
            'side_effects':            forms.Textarea(attrs=fc(rows=3)),
            'warnings':                forms.Textarea(attrs=fc(rows=3)),
            'precautions':             forms.Textarea(attrs=fc(rows=3)),
            'overdose_management':     forms.Textarea(attrs=fc(rows=3)),
            'pregnancy_category':      forms.Select(attrs=sel()),
            'pregnancy_safety':        forms.Textarea(attrs=fc(rows=2)),
            'lactation_safety':        forms.Textarea(attrs=fc(rows=2)),
            'breastfeeding_compatible':forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'breastfeeding_notes':     forms.Textarea(attrs=fc(rows=2)),
            'notes':                   forms.Textarea(attrs=fc(rows=2)),
            'pharmacist_notes':        forms.Textarea(attrs=fc(rows=2)),
            'show_estimated_weight':   forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ─── DosageRule (inline — no generic_medication field) ───────────────────────

class DosageRuleInlineForm(forms.ModelForm):
    class Meta:
        model = DosageRule
        fields = [
            'label', 'patient_group', 'indication',
            'dose_calc_type', 'route',
            'formula_type', 'formula_factor', 'formula_divisor',
            'min_dose_mg', 'max_dose_mg', 'max_daily_dose_mg',
            'usual_dose_text',
            'frequency_per_day', 'frequency_text',
            'duration_days', 'duration_text',
            'min_age_months', 'max_age_months',
            'min_weight_kg', 'max_weight_kg',
            'unit_conversion_enabled', 'unit_conversion_factor',
            'unit_conversion_from', 'unit_conversion_to',
            'notes', 'display_order',
        ]
        widgets = {
            'label':                   forms.TextInput(attrs=fc(placeholder=_('e.g. Children 2-12y'))),
            'patient_group':           forms.Select(attrs=sel()),
            'indication':              forms.TextInput(attrs=fc(placeholder=_('e.g. Ear infection'))),
            'dose_calc_type':          forms.Select(attrs=sel()),
            'route':                   forms.Select(attrs=sel()),
            'formula_type':            forms.Select(attrs=sel()),
            'formula_factor':          forms.NumberInput(attrs=fc(step='0.001', placeholder='e.g. 15')),
            'formula_divisor':         forms.NumberInput(attrs=fc(placeholder='doses/day')),
            'min_dose_mg':             forms.NumberInput(attrs=fc(step='0.01')),
            'max_dose_mg':             forms.NumberInput(attrs=fc(step='0.01')),
            'max_daily_dose_mg':       forms.NumberInput(attrs=fc(step='0.01')),
            'usual_dose_text':         forms.Textarea(attrs=fc(rows=2, placeholder=_('e.g. 500mg twice daily'))),
            'frequency_per_day':       forms.NumberInput(attrs=fc()),
            'frequency_text':          forms.TextInput(attrs=fc(placeholder='e.g. every 8 hours')),
            'duration_days':           forms.NumberInput(attrs=fc()),
            'duration_text':           forms.TextInput(attrs=fc(placeholder='e.g. 7-10 days')),
            'min_age_months':          forms.NumberInput(attrs=fc(placeholder='months')),
            'max_age_months':          forms.NumberInput(attrs=fc(placeholder='months')),
            'min_weight_kg':           forms.NumberInput(attrs=fc(step='0.1')),
            'max_weight_kg':           forms.NumberInput(attrs=fc(step='0.1')),
            'unit_conversion_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'unit_conversion_factor':  forms.NumberInput(attrs=fc(step='0.0001')),
            'unit_conversion_from':    forms.TextInput(attrs=fc(placeholder='ml')),
            'unit_conversion_to':      forms.TextInput(attrs=fc(placeholder='drops')),
            'notes':                   forms.Textarea(attrs=fc(rows=2)),
            'display_order':           forms.NumberInput(attrs=fc()),
        }


# Inline formset: GenericMedication → DosageRule
DosageRuleFormSet = inlineformset_factory(
    GenericMedication,
    DosageRule,
    form=DosageRuleInlineForm,
    extra=1,
    can_delete=True,
    min_num=0,
)


# ─── DosageRule (standalone form — keeps generic_medication) ──────────────────

class DosageRuleForm(DosageRuleInlineForm):
    class Meta(DosageRuleInlineForm.Meta):
        fields = ['generic_medication'] + DosageRuleInlineForm.Meta.fields
        widgets = {
            **DosageRuleInlineForm.Meta.widgets,
            'generic_medication': forms.Select(attrs=sel()),
        }


# ─── TradeNameProduct ─────────────────────────────────────────────────────────

class TradeNameProductForm(forms.ModelForm):
    class Meta:
        model = TradeNameProduct
        fields = [
            'trade_name', 'trade_name_ar', 'manufacturer', 'drug_form',
            'concentration', 'drug_family', 'drug_category', 'patient_group',
            'display_order_in_family', 'prescription_status',
            'prescription_status_notes', 'availability',
            'price', 'price_with_tax', 'package_size', 'barcode',
            'can_be_crushed', 'can_be_cut', 'can_be_chewed',
            'physical_modification_notes', 'storage_conditions',
            'shelf_life', 'storage_after_opening',
            'package_image_url', 'leaflet_image_url', 'box_image_url',
            'notes', 'pharmacist_notes', 'show_estimated_weight',
        ]
        widgets = {
            'trade_name':                   forms.TextInput(attrs=fc(placeholder=_('e.g. Augmentin'))),
            'trade_name_ar':                forms.TextInput(attrs=ar_input(placeholder='مثال: أوجمنتين')),
            'manufacturer':                 forms.Select(attrs=sel()),
            'drug_form':                    forms.Select(attrs=sel()),
            'concentration':                forms.TextInput(attrs=fc(placeholder='e.g. 250mg/5ml')),
            'drug_family':                  forms.Select(attrs=sel()),
            'drug_category':                forms.Select(attrs=sel()),
            'patient_group':                forms.Select(attrs=sel()),
            'display_order_in_family':      forms.NumberInput(attrs=fc()),
            'prescription_status':          forms.Select(attrs=sel()),
            'prescription_status_notes':    forms.Textarea(attrs=fc(rows=2)),
            'availability':                 forms.Select(attrs=sel()),
            'price':                        forms.NumberInput(attrs=fc(step='0.01')),
            'price_with_tax':               forms.NumberInput(attrs=fc(step='0.01')),
            'package_size':                 forms.TextInput(attrs=fc(placeholder='e.g. 20 tablets')),
            'barcode':                      forms.TextInput(attrs=fc()),
            'can_be_crushed':               forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_be_cut':                   forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_be_chewed':                forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'physical_modification_notes':  forms.Textarea(attrs=fc(rows=2)),
            'storage_conditions':           forms.Textarea(attrs=fc(rows=2)),
            'shelf_life':                   forms.TextInput(attrs=fc(placeholder='e.g. 24 months')),
            'storage_after_opening':        forms.TextInput(attrs=fc()),
            'package_image_url':            forms.URLInput(attrs=fc()),
            'leaflet_image_url':            forms.URLInput(attrs=fc()),
            'box_image_url':                forms.URLInput(attrs=fc()),
            'notes':                        forms.Textarea(attrs=fc(rows=2)),
            'pharmacist_notes':             forms.Textarea(attrs=fc(rows=2)),
            'show_estimated_weight':        forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ─── Equation ─────────────────────────────────────────────────────────────────

class EquationForm(forms.ModelForm):
    class Meta:
        model = Equation
        fields = ['name', 'name_ar', 'description', 'description_ar', 'formula_display',
                  'result_unit', 'result_label', 'interpretation', 'reference',
                  'reference_url', 'category', 'display_order', 'is_active']
        widgets = {
            'name':            forms.TextInput(attrs=fc(placeholder='e.g. Cockcroft-Gault')),
            'name_ar':         forms.TextInput(attrs=ar_input(placeholder='مثال: معادلة كوكروفت-غولت')),
            'description':     forms.Textarea(attrs=fc(rows=3)),
            'description_ar':  forms.Textarea(attrs=ar_area(rows=3)),
            'formula_display': forms.Textarea(attrs=fc(rows=2)),
            'result_unit':     forms.TextInput(attrs=fc(placeholder='e.g. ml/min')),
            'result_label':    forms.TextInput(attrs=fc()),
            'interpretation':  forms.Textarea(attrs=fc(rows=4, placeholder='[{"min":0,"max":30,"label":"Severe"},...]')),
            'reference':       forms.TextInput(attrs=fc()),
            'reference_url':   forms.URLInput(attrs=fc()),
            'category':        forms.TextInput(attrs=fc(placeholder='e.g. Renal')),
            'display_order':   forms.NumberInput(attrs=fc()),
            'is_active':       forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ─── AgeWeightEstimate ────────────────────────────────────────────────────────

class AgeWeightEstimateForm(forms.ModelForm):
    class Meta:
        model = AgeWeightEstimate
        fields = ['age_months', 'age_text', 'estimated_weight_kg', 'age_group']
        widgets = {
            'age_months':          forms.NumberInput(attrs=fc()),
            'age_text':            forms.TextInput(attrs=fc(placeholder='e.g. 2 months')),
            'estimated_weight_kg': forms.NumberInput(attrs=fc(step='0.01')),
            'age_group':           forms.TextInput(attrs=fc(placeholder='e.g. 0-1 years')),
        }


# ─── DrugInteraction ──────────────────────────────────────────────────────────

class DrugInteractionForm(forms.ModelForm):
    class Meta:
        model = DrugInteraction
        fields = ['drug_a', 'drug_b', 'severity', 'description', 'management', 'reference']
        widgets = {
            'drug_a':      forms.Select(attrs=sel()),
            'drug_b':      forms.Select(attrs=sel()),
            'severity':    forms.Select(attrs=sel()),
            'description': forms.Textarea(attrs=fc(rows=3)),
            'management':  forms.Textarea(attrs=fc(rows=3)),
            'reference':   forms.TextInput(attrs=fc()),
        }
