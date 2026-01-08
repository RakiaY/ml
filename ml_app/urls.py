from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('women_preference/', views.women_preference_view, name='women_preference'),
    path('future_avg_basket/', views.future_avg_basket_view, name='future_avg_basket'),
    path('potential_region/', views.potential_region_view, name='potential_region'),
    path('recommended_price/', views.recommended_price_view, name='recommended_price'),
    path('spending_level/', views.spending_level_view, name='spending_level'),
    path('regression_failed_orders/', views.regression_failed_orders_view, name='regression_failed_orders'),
    path('classification_high_risk_cancelling/', views.classification_high_risk_cancelling_view, name='classification_high_risk_cancelling'),
    path('regression_state_revenue/', views.regression_state_revenue_view, name='regression_state_revenue'),
    path('classification_customer_behavior/', views.classification_customer_behavior_view, name='classification_customer_behavior'),
    path('future_purchases/', views.future_purchases_view, name='future_purchases'),
    path('customer_clustering/', views.customer_clustering_view, name='customer_clustering'),
    path('regional_clustering/', views.regional_clustering_view, name='regional_clustering'),
    path('power_bi_dashboard/', views.power_bi_dashboard_view, name='power_bi_dashboard'),
    # Redirection temporaire pour l'ancienne URL
    path('regression_ghada/', lambda request: redirect('future_purchases', permanent=True)),
]