from django.urls import path
from .views import (
    QuotationListView,
    QuotationDetailView,
    QuotationCreateView,
    QuotationUpdateView,
    QuotationDeleteView,
    QuotationTemplateDetailAPIView,
    QuotationReportView,
    QuotationPrintView,
    ItemListView,
    ItemCreateView,
    ItemUpdateView,
    ItemDeleteView,
    ItemGroupListView,
    ItemGroupCreateView,
    ItemGroupUpdateView,
    ItemGroupDeleteView,
    UnitListView,
    UnitCreateView,
    UnitUpdateView,
    UnitDeleteView,
    quotation_pdf_view,
)

urlpatterns = [
    path('', QuotationListView.as_view(), name='quotation_list'),
    path('create/', QuotationCreateView.as_view(), name='quotation_create'),
    path('<int:pk>/', QuotationDetailView.as_view(), name='quotation_view'),
    path('<int:pk>/update/', QuotationUpdateView.as_view(), name='quotation_update'),
    path('<int:pk>/delete/', QuotationDeleteView.as_view(), name='quotation_delete'),
    path('<int:pk>/report/', QuotationReportView.as_view(), name='quotation_report'),
    path('<int:pk>/print/', QuotationPrintView.as_view(), name='quotation_print'),
    path('api/templates/<int:pk>/', QuotationTemplateDetailAPIView.as_view(), name='quotation_template_api'),

    path('items/', ItemListView.as_view(), name='item_list'),
    path('items/create/', ItemCreateView.as_view(), name='item_create'),
    path('items/<int:pk>/update/', ItemUpdateView.as_view(), name='item_update'),
    path('items/<int:pk>/delete/', ItemDeleteView.as_view(), name='item_delete'),

    path('item-groups/', ItemGroupListView.as_view(), name='itemgroup_list'),
    path('item-groups/create/', ItemGroupCreateView.as_view(), name='itemgroup_create'),
    path('item-groups/<int:pk>/update/', ItemGroupUpdateView.as_view(), name='itemgroup_update'),
    path('item-groups/<int:pk>/delete/', ItemGroupDeleteView.as_view(), name='itemgroup_delete'),

    path('units/', UnitListView.as_view(), name='unit_list'),
    path('units/create/', UnitCreateView.as_view(), name='unit_create'),
    path('units/<int:pk>/update/', UnitUpdateView.as_view(), name='unit_update'),
    path('units/<int:pk>/delete/', UnitDeleteView.as_view(), name='unit_delete'),
    
    path('quotation/<int:pk>/pdf/', quotation_pdf_view, name='quotation-pdf'),
]
