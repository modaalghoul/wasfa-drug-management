from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.db.models import Q, Count
from .models import (
    PatientGroup, DrugCategory, DrugFamily, Manufacturer, GenericMedication,
    DosageRule, RangeBasedDose, TradeNameProduct, TradeNameComposition,
    DrugInteraction, MedicationAlternative, AgeWeightEstimate, Equation,
    EquationInput, SearchHistory
)
from .forms import (
    PatientGroupForm, DrugCategoryForm, DrugFamilyForm, ManufacturerForm,
    GenericMedicationForm, DosageRuleForm, DosageRuleFormSet,
    TradeNameProductForm, EquationForm, AgeWeightEstimateForm, DrugInteractionForm
)


# ══════════════════════════════════════════════════════════════
# Dashboard
# ══════════════════════════════════════════════════════════════
def dashboard(request):
    context = {
        'total_medications': GenericMedication.objects.count(),
        'total_products':    TradeNameProduct.objects.count(),
        'total_categories':  DrugCategory.objects.count(),
        'total_families':    DrugFamily.objects.count(),
        'total_equations':   Equation.objects.count(),
        'total_interactions':DrugInteraction.objects.count(),
        'latest_medications': GenericMedication.objects.select_related('drug_category', 'drug_family').order_by('-created_at')[:5],
        'latest_products':    TradeNameProduct.objects.select_related('drug_category').order_by('-created_at')[:5],
        'categories':         DrugCategory.objects.annotate(med_count=Count('medications')).order_by('display_order'),
    }
    return render(request, 'drug_management/dashboard.html', context)


# ══════════════════════════════════════════════════════════════
# PatientGroup
# ══════════════════════════════════════════════════════════════
class PatientGroupListView(ListView):
    model = PatientGroup
    template_name = 'drug_management/patient_group_list.html'
    context_object_name = 'patient_groups'
    paginate_by = 10

    def get_queryset(self):
        qs = PatientGroup.objects.all()
        q = self.request.GET.get('search')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(name_ar__icontains=q))
        return qs.order_by('display_order')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_query'] = self.request.GET.get('search', '')
        return ctx


def patient_group_create(request):
    form = PatientGroupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _('Patient group created successfully.'))
        return redirect('patient_group_list')
    return render(request, 'drug_management/patient_group_form.html', {'form': form})


def patient_group_edit(request, pk):
    obj = get_object_or_404(PatientGroup, pk=pk)
    form = PatientGroupForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _('Patient group updated.'))
        return redirect('patient_group_list')
    return render(request, 'drug_management/patient_group_form.html', {'form': form, 'object': obj})


class PatientGroupDeleteView(DeleteView):
    model = PatientGroup
    template_name = 'drug_management/confirm_delete.html'
    success_url = reverse_lazy('patient_group_list')
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Deleted.'))
        return super().delete(request, *args, **kwargs)


# ══════════════════════════════════════════════════════════════
# DrugCategory
# ══════════════════════════════════════════════════════════════
class DrugCategoryListView(ListView):
    model = DrugCategory
    template_name = 'drug_management/drug_category_list.html'
    context_object_name = 'categories'
    paginate_by = 20

    def get_queryset(self):
        qs = DrugCategory.objects.annotate(family_count=Count('families'))
        q = self.request.GET.get('search')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(name_ar__icontains=q))
        return qs.order_by('display_order')


def drug_category_create(request):
    form = DrugCategoryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _('Category created.'))
        return redirect('drug_category_list')
    return render(request, 'drug_management/drug_category_form.html', {'form': form})


def drug_category_edit(request, pk):
    obj = get_object_or_404(DrugCategory, pk=pk)
    form = DrugCategoryForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _('Category updated.'))
        return redirect('drug_category_list')
    return render(request, 'drug_management/drug_category_form.html', {'form': form, 'object': obj})


class DrugCategoryDeleteView(DeleteView):
    model = DrugCategory
    template_name = 'drug_management/confirm_delete.html'
    success_url = reverse_lazy('drug_category_list')
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Deleted.'))
        return super().delete(request, *args, **kwargs)


# ══════════════════════════════════════════════════════════════
# DrugFamily
# ══════════════════════════════════════════════════════════════
class DrugFamilyListView(ListView):
    model = DrugFamily
    template_name = 'drug_management/drug_family_list.html'
    context_object_name = 'families'
    paginate_by = 20

    def get_queryset(self):
        qs = DrugFamily.objects.select_related('drug_category')
        q = self.request.GET.get('search')
        cat = self.request.GET.get('category')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(name_ar__icontains=q))
        if cat:
            qs = qs.filter(drug_category_id=cat)
        return qs.order_by('drug_category__display_order', 'display_order')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = DrugCategory.objects.all()
        ctx['search_query'] = self.request.GET.get('search', '')
        ctx['selected_category'] = self.request.GET.get('category', '')
        return ctx


def drug_family_create(request):
    form = DrugFamilyForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _('Drug family created.'))
        return redirect('drug_family_list')
    return render(request, 'drug_management/drug_family_form.html', {'form': form})


def drug_family_edit(request, pk):
    obj = get_object_or_404(DrugFamily, pk=pk)
    form = DrugFamilyForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _('Drug family updated.'))
        return redirect('drug_family_list')
    return render(request, 'drug_management/drug_family_form.html', {'form': form, 'object': obj})


class DrugFamilyDeleteView(DeleteView):
    model = DrugFamily
    template_name = 'drug_management/confirm_delete.html'
    success_url = reverse_lazy('drug_family_list')
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Deleted.'))
        return super().delete(request, *args, **kwargs)


# ══════════════════════════════════════════════════════════════
# Manufacturer
# ══════════════════════════════════════════════════════════════
class ManufacturerListView(ListView):
    model = Manufacturer
    template_name = 'drug_management/manufacturer_list.html'
    context_object_name = 'manufacturers'
    paginate_by = 20

    def get_queryset(self):
        qs = Manufacturer.objects.all()
        q = self.request.GET.get('search')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(name_ar__icontains=q))
        return qs.order_by('name')


def manufacturer_create(request):
    form = ManufacturerForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _('Manufacturer created.'))
        return redirect('manufacturer_list')
    return render(request, 'drug_management/manufacturer_form.html', {'form': form})


def manufacturer_edit(request, pk):
    obj = get_object_or_404(Manufacturer, pk=pk)
    form = ManufacturerForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _('Manufacturer updated.'))
        return redirect('manufacturer_list')
    return render(request, 'drug_management/manufacturer_form.html', {'form': form, 'object': obj})


class ManufacturerDeleteView(DeleteView):
    model = Manufacturer
    template_name = 'drug_management/confirm_delete.html'
    success_url = reverse_lazy('manufacturer_list')
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Deleted.'))
        return super().delete(request, *args, **kwargs)


# ══════════════════════════════════════════════════════════════
# GenericMedication  ← core views, now handle DosageRuleFormSet
# ══════════════════════════════════════════════════════════════
class MedicationListView(ListView):
    model = GenericMedication
    template_name = 'drug_management/medication_list.html'
    context_object_name = 'medications'
    paginate_by = 20

    def get_queryset(self):
        qs = GenericMedication.objects.select_related('drug_family', 'drug_category', 'patient_group')
        q        = self.request.GET.get('search')
        category = self.request.GET.get('category')
        family   = self.request.GET.get('family')
        if q:
            qs = qs.filter(Q(generic_name__icontains=q) | Q(generic_name_ar__icontains=q))
        if category:
            qs = qs.filter(drug_category_id=category)
        if family:
            qs = qs.filter(drug_family_id=family)
        return qs.order_by('drug_family', 'display_order_in_family')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories']       = DrugCategory.objects.all()
        ctx['families']         = DrugFamily.objects.all()
        ctx['search_query']     = self.request.GET.get('search', '')
        ctx['selected_category']= self.request.GET.get('category', '')
        ctx['selected_family']  = self.request.GET.get('family', '')
        return ctx


def medication_create(request):
    if request.method == 'POST':
        form    = GenericMedicationForm(request.POST)
        formset = DosageRuleFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            medication          = form.save()
            formset.instance    = medication
            formset.save()
            messages.success(request, _('Medication created successfully.'))
            return redirect('medication_detail', pk=medication.pk)
    else:
        form    = GenericMedicationForm()
        formset = DosageRuleFormSet()
    return render(request, 'drug_management/medication_form.html', {
        'form': form, 'dosage_formset': formset,
    })


def medication_edit(request, pk):
    medication = get_object_or_404(GenericMedication, pk=pk)
    if request.method == 'POST':
        form    = GenericMedicationForm(request.POST, instance=medication)
        formset = DosageRuleFormSet(request.POST, instance=medication)
        if form.is_valid() and formset.is_valid():
            medication          = form.save()
            formset.instance    = medication
            formset.save()
            messages.success(request, _('Medication updated.'))
            return redirect('medication_detail', pk=medication.pk)
    else:
        form    = GenericMedicationForm(instance=medication)
        formset = DosageRuleFormSet(instance=medication)
    return render(request, 'drug_management/medication_form.html', {
        'form': form, 'dosage_formset': formset, 'object': medication,
    })


class MedicationDetailView(DetailView):
    model = GenericMedication
    template_name = 'drug_management/medication_detail.html'
    context_object_name = 'medication'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['dosage_rules'] = self.object.dosage_rules.select_related('patient_group').all()
        ctx['interactions'] = DrugInteraction.objects.filter(
            Q(drug_a=self.object) | Q(drug_b=self.object)
        )
        return ctx


class MedicationDeleteView(DeleteView):
    model = GenericMedication
    template_name = 'drug_management/confirm_delete.html'
    success_url = reverse_lazy('medication_list')
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Medication deleted.'))
        return super().delete(request, *args, **kwargs)


# ══════════════════════════════════════════════════════════════
# DosageRule (standalone)
# ══════════════════════════════════════════════════════════════
class DosageRuleListView(ListView):
    model = DosageRule
    template_name = 'drug_management/dosage_rule_list.html'
    context_object_name = 'rules'
    paginate_by = 20

    def get_queryset(self):
        qs = DosageRule.objects.select_related('generic_medication', 'patient_group')
        med = self.request.GET.get('medication')
        if med:
            qs = qs.filter(generic_medication_id=med)
        return qs.order_by('generic_medication', 'display_order')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['medications'] = GenericMedication.objects.all()
        ctx['selected_medication'] = self.request.GET.get('medication', '')
        return ctx


def dosage_rule_create(request):
    form = DosageRuleForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _('Dosage rule created.'))
        return redirect('dosage_rule_list')
    return render(request, 'drug_management/dosage_rule_form.html', {'form': form})


def dosage_rule_edit(request, pk):
    obj = get_object_or_404(DosageRule, pk=pk)
    form = DosageRuleForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _('Dosage rule updated.'))
        return redirect('dosage_rule_list')
    return render(request, 'drug_management/dosage_rule_form.html', {'form': form, 'object': obj})


class DosageRuleDeleteView(DeleteView):
    model = DosageRule
    template_name = 'drug_management/confirm_delete.html'
    success_url = reverse_lazy('dosage_rule_list')
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Deleted.'))
        return super().delete(request, *args, **kwargs)


# ══════════════════════════════════════════════════════════════
# TradeNameProduct
# ══════════════════════════════════════════════════════════════
class TradeNameListView(ListView):
    model = TradeNameProduct
    template_name = 'drug_management/trade_name_list.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        qs = TradeNameProduct.objects.select_related('drug_family', 'drug_category', 'manufacturer')
        q        = self.request.GET.get('search')
        category = self.request.GET.get('category')
        if q:
            qs = qs.filter(Q(trade_name__icontains=q) | Q(trade_name_ar__icontains=q))
        if category:
            qs = qs.filter(drug_category_id=category)
        return qs.order_by('drug_family', 'display_order_in_family')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories']       = DrugCategory.objects.all()
        ctx['search_query']     = self.request.GET.get('search', '')
        ctx['selected_category']= self.request.GET.get('category', '')
        return ctx


def trade_name_create(request):
    form = TradeNameProductForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _('Trade name product created.'))
        return redirect('trade_name_list')
    return render(request, 'drug_management/trade_name_form.html', {'form': form})


def trade_name_edit(request, pk):
    obj = get_object_or_404(TradeNameProduct, pk=pk)
    form = TradeNameProductForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _('Trade name updated.'))
        return redirect('trade_name_list')
    return render(request, 'drug_management/trade_name_form.html', {'form': form, 'object': obj})


class TradeNameDetailView(DetailView):
    model = TradeNameProduct
    template_name = 'drug_management/trade_name_detail.html'
    context_object_name = 'product'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['compositions'] = self.object.compositions.select_related('generic_medication').all()
        return ctx


class TradeNameDeleteView(DeleteView):
    model = TradeNameProduct
    template_name = 'drug_management/confirm_delete.html'
    success_url = reverse_lazy('trade_name_list')
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Deleted.'))
        return super().delete(request, *args, **kwargs)


# ══════════════════════════════════════════════════════════════
# Equation
# ══════════════════════════════════════════════════════════════
class EquationListView(ListView):
    model = Equation
    template_name = 'drug_management/equation_list.html'
    context_object_name = 'equations'
    paginate_by = 10

    def get_queryset(self):
        qs = Equation.objects.filter(is_active=True)
        q = self.request.GET.get('search')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(name_ar__icontains=q))
        return qs.order_by('display_order', 'name')


def equation_create(request):
    form = EquationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _('Equation created.'))
        return redirect('equation_list')
    return render(request, 'drug_management/equation_form.html', {'form': form})


def equation_edit(request, pk):
    obj = get_object_or_404(Equation, pk=pk)
    form = EquationForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _('Equation updated.'))
        return redirect('equation_list')
    return render(request, 'drug_management/equation_form.html', {'form': form, 'object': obj})


class EquationDeleteView(DeleteView):
    model = Equation
    template_name = 'drug_management/confirm_delete.html'
    success_url = reverse_lazy('equation_list')
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Deleted.'))
        return super().delete(request, *args, **kwargs)


# ══════════════════════════════════════════════════════════════
# AgeWeightEstimate
# ══════════════════════════════════════════════════════════════
class AgeWeightEstimateListView(ListView):
    model = AgeWeightEstimate
    template_name = 'drug_management/age_weight_list.html'
    context_object_name = 'estimates'
    paginate_by = 40

    def get_queryset(self):
        return AgeWeightEstimate.objects.all().order_by('age_months')


def age_weight_create(request):
    form = AgeWeightEstimateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _('Entry created.'))
        return redirect('age_weight_list')
    return render(request, 'drug_management/age_weight_form.html', {'form': form})


def age_weight_edit(request, pk):
    obj = get_object_or_404(AgeWeightEstimate, pk=pk)
    form = AgeWeightEstimateForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _('Entry updated.'))
        return redirect('age_weight_list')
    return render(request, 'drug_management/age_weight_form.html', {'form': form, 'object': obj})


class AgeWeightEstimateDeleteView(DeleteView):
    model = AgeWeightEstimate
    template_name = 'drug_management/confirm_delete.html'
    success_url = reverse_lazy('age_weight_list')
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Deleted.'))
        return super().delete(request, *args, **kwargs)


# ══════════════════════════════════════════════════════════════
# DrugInteraction
# ══════════════════════════════════════════════════════════════
class DrugInteractionListView(ListView):
    model = DrugInteraction
    template_name = 'drug_management/interaction_list.html'
    context_object_name = 'interactions'
    paginate_by = 20

    def get_queryset(self):
        qs = DrugInteraction.objects.select_related('drug_a', 'drug_b')
        sev = self.request.GET.get('severity')
        if sev:
            qs = qs.filter(severity=sev)
        return qs.order_by('-severity')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['selected_severity'] = self.request.GET.get('severity', '')
        return ctx


def drug_interaction_create(request):
    form = DrugInteractionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _('Interaction recorded.'))
        return redirect('drug_interaction_list')
    return render(request, 'drug_management/interaction_form.html', {'form': form})


def drug_interaction_edit(request, pk):
    obj = get_object_or_404(DrugInteraction, pk=pk)
    form = DrugInteractionForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _('Interaction updated.'))
        return redirect('drug_interaction_list')
    return render(request, 'drug_management/interaction_form.html', {'form': form, 'object': obj})


class DrugInteractionDeleteView(DeleteView):
    model = DrugInteraction
    template_name = 'drug_management/confirm_delete.html'
    success_url = reverse_lazy('drug_interaction_list')
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Deleted.'))
        return super().delete(request, *args, **kwargs)
