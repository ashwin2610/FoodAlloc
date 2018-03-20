from django.urls import path
from . import views

urlpatterns = [
	path('', views.HomePageView.as_view(), name='home'),
	path('alloc/', views.FoodAllocView.as_view(), name='alloc'),
	path('lookup/', views.FoodLookupView.as_view(), name='lookup'),
	path('prefer/', views.set_preferences, name='prefer'),
	path('alter/', views.SetAlternativesView.as_view(), name='alter'),
	path('alloc/allocate_food_physical', views.get_food_details, name='food_details'),
	path('alloc/allocate_food_nutritional', views.get_food_range, name='food_info'),
	path('lookup/lookup_info', views.get_food_info, name='lookup_info'),
	path('lookup/lookup_name', views.get_food_name, name='lookup_name'),
]
