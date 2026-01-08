from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_view, name='predict'),
    path('women_preference/', views.women_preference_view, name='women_preference'),
    path('future_avg_basket/', views.future_avg_basket_view, name='future_avg_basket'),
    path('potential_region/', views.potential_region_view, name='potential_region'),
    path('recommended_price/', views.recommended_price_view, name='recommended_price'),
    path('spending_level/', views.spending_level_view, name='spending_level'),
    path('regression_failed_orders/', views.regression_failed_orders_view, name='regression_failed_orders'),
    path('classification_high_risk_cancelling/', views.classification_high_risk_cancelling_view, name='classification_high_risk_cancelling'),
    path('regression_state_revenue/', views.regression_state_revenue_view, name='regression_state_revenue'),
    path('classification_customer_behavior/', views.classification_customer_behavior_view, name='classification_customer_behavior'),
    path('regression_ghada/', views.regression_ghada_view, name='regression_ghada'),

]