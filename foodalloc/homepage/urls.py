from django.urls import path
from . import views

urlpatterns = [
	path('', views.HomePageView.as_view(), name='home'),
	path('alloc/', views.FoodAllocView.as_view(), name='alloc'),
	path('lookup/', views.FoodLookupView.as_view(), name='lookup'),
	path('prefer/', views.SetPreferencesView.as_view(), name='prefer'),
	path('alter/', views.SetAlternativesView.as_view(), name='alter'),
]
