from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from .forms import AllocateFoodWithPhysicalTraits, FoodInfo, LookupFoodWithFoodName

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'home.html'

class FoodAllocView(TemplateView):
    template_name = 'alloc.html'

class FoodLookupView(TemplateView):
    template_name = 'lookup.html'

class SetPreferencesView(TemplateView):
    template_name = 'prefer.html'

class SetAlternativesView(TemplateView):
    template_name = 'alter.html'

def get_food_details(request):
	if request.method == 'POST':
		form = AllocateFoodWithPhysicalTraits(request.POST)
		# Have to do something here
	else:
		form = AllocateFoodWithPhysicalTraits()
		return render(request, 'alloc/allocate_food_physical.html', {'form': form})

def get_food_info(request):
	if request.method == 'POST':
		form = FoodInfo(request.POST)
		# Have to do something here
	else:
		form = FoodInfo()
		return render(request, 'alloc/allocate_food_physical.html', {'form': form})

def get_food_name(request):
	if request.method == 'POST':
		form = LookupFoodWithFoodName(request.POST)
		# Have to do something here
	else:
		form = LookupFoodWithFoodName()
		return render(request, 'alloc/allocate_food_physical.html', {'form': form})