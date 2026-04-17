from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # PatientGroup
    path('patient-groups/',                   views.PatientGroupListView.as_view(),   name='patient_group_list'),
    path('patient-groups/create/',            views.patient_group_create,             name='patient_group_create'),
    path('patient-groups/<int:pk>/edit/',     views.patient_group_edit,               name='patient_group_edit'),
    path('patient-groups/<int:pk>/delete/',   views.PatientGroupDeleteView.as_view(), name='patient_group_delete'),

    # DrugCategory
    path('categories/',                       views.DrugCategoryListView.as_view(),   name='drug_category_list'),
    path('categories/create/',                views.drug_category_create,             name='drug_category_create'),
    path('categories/<int:pk>/edit/',         views.drug_category_edit,               name='drug_category_edit'),
    path('categories/<int:pk>/delete/',       views.DrugCategoryDeleteView.as_view(), name='drug_category_delete'),

    # DrugFamily
    path('families/',                         views.DrugFamilyListView.as_view(),     name='drug_family_list'),
    path('families/create/',                  views.drug_family_create,               name='drug_family_create'),
    path('families/<int:pk>/edit/',           views.drug_family_edit,                 name='drug_family_edit'),
    path('families/<int:pk>/delete/',         views.DrugFamilyDeleteView.as_view(),   name='drug_family_delete'),

    # Manufacturer
    path('manufacturers/',                    views.ManufacturerListView.as_view(),   name='manufacturer_list'),
    path('manufacturers/create/',             views.manufacturer_create,              name='manufacturer_create'),
    path('manufacturers/<int:pk>/edit/',      views.manufacturer_edit,                name='manufacturer_edit'),
    path('manufacturers/<int:pk>/delete/',    views.ManufacturerDeleteView.as_view(), name='manufacturer_delete'),

    # GenericMedication
    path('medications/',                      views.MedicationListView.as_view(),     name='medication_list'),
    path('medications/create/',               views.medication_create,                name='medication_create'),
    path('medications/<int:pk>/',             views.MedicationDetailView.as_view(),   name='medication_detail'),
    path('medications/<int:pk>/edit/',        views.medication_edit,                  name='medication_edit'),
    path('medications/<int:pk>/delete/',      views.MedicationDeleteView.as_view(),   name='medication_delete'),

    # DosageRule
    path('dosage-rules/',                     views.DosageRuleListView.as_view(),     name='dosage_rule_list'),
    path('dosage-rules/create/',              views.dosage_rule_create,               name='dosage_rule_create'),
    path('dosage-rules/<int:pk>/edit/',       views.dosage_rule_edit,                 name='dosage_rule_edit'),
    path('dosage-rules/<int:pk>/delete/',     views.DosageRuleDeleteView.as_view(),   name='dosage_rule_delete'),

    # TradeNameProduct
    path('trade-names/',                      views.TradeNameListView.as_view(),      name='trade_name_list'),
    path('trade-names/create/',               views.trade_name_create,                name='trade_name_create'),
    path('trade-names/<int:pk>/',             views.TradeNameDetailView.as_view(),    name='trade_name_detail'),
    path('trade-names/<int:pk>/edit/',        views.trade_name_edit,                  name='trade_name_edit'),
    path('trade-names/<int:pk>/delete/',      views.TradeNameDeleteView.as_view(),    name='trade_name_delete'),

    # Equation
    path('equations/',                        views.EquationListView.as_view(),       name='equation_list'),
    path('equations/create/',                 views.equation_create,                  name='equation_create'),
    path('equations/<int:pk>/edit/',          views.equation_edit,                    name='equation_edit'),
    path('equations/<int:pk>/delete/',        views.EquationDeleteView.as_view(),     name='equation_delete'),

    # AgeWeightEstimate
    path('age-weight/',                       views.AgeWeightEstimateListView.as_view(), name='age_weight_list'),
    path('age-weight/create/',                views.age_weight_create,                name='age_weight_create'),
    path('age-weight/<int:pk>/edit/',         views.age_weight_edit,                  name='age_weight_edit'),
    path('age-weight/<int:pk>/delete/',       views.AgeWeightEstimateDeleteView.as_view(), name='age_weight_delete'),

    # DrugInteraction
    path('interactions/',                     views.DrugInteractionListView.as_view(), name='drug_interaction_list'),
    path('interactions/create/',              views.drug_interaction_create,           name='drug_interaction_create'),
    path('interactions/<int:pk>/edit/',       views.drug_interaction_edit,             name='drug_interaction_edit'),
    path('interactions/<int:pk>/delete/',     views.DrugInteractionDeleteView.as_view(), name='drug_interaction_delete'),
]
