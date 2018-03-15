from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from .forms import AllocateFoodWithPhysicalTraits, FoodInfo, LookupFoodWithFoodName
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import FooDB

# Create your views here.


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

class FoodAllocView(LoginRequiredMixin, TemplateView):
    template_name = 'alloc.html'

class FoodLookupView(LoginRequiredMixin, TemplateView):
    template_name = 'lookup.html'

class SetPreferencesView(LoginRequiredMixin, TemplateView):
    template_name = 'prefer.html'

class SetAlternativesView(LoginRequiredMixin, TemplateView):
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
		if form.is_valid():
			upper_bound = form.cleaned_data['upper_bound']
			lower_bound = form.cleaned_data['lower_bound']
			items = FooDB.objects.filter(calories__lte=upper_bound).filter(calories__gte=lower_bound).order_by('calories')
			return render(request, 'alloc/result.html', {'items': items})
	else:
		form = FoodInfo()
		return render(request, 'alloc/allocate_food_physical.html', {'form': form})

def get_food_name(request):
	if request.method == 'POST':
		form = LookupFoodWithFoodName(request.POST)
		# Have to do something here
		if form.is_valid():
			name = form.cleaned_data['name']
			items = FooDB.objects.filter(food__iexact=name)
			return render(request, 'alloc/result.html', {'items': items})	

	else:
		form = LookupFoodWithFoodName()
		return render(request, 'alloc/allocate_food_physical.html', {'form': form})