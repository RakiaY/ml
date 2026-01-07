from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_view, name='predict'),
    path('women_preference/', views.women_preference_view, name='women_preference'),
    path('future_avg_basket/', views.future_avg_basket_view, name='future_avg_basket'),
    path('potential_region/', views.potential_region_view, name='potential_region'),
    path('recommended_price/', views.recommended_price_view, name='recommended_price'),
    path('spending_level/', views.spending_level_view, name='spending_level'),
]