from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from .forms import AllocateFoodWithPhysicalTraits, FoodInfo, LookupFoodWithFoodName
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import FooDB

from random import randint, sample

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

		if form.is_valid():
			height, weight, age, gender = form.clean_food_alloc_data()

		if gender == 'M':
			bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
		else:
			bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

		calories_required = bmr *1.55

		breakfast, lunch, dinner = allocate(calories_required)

		return render(request, 'alloc/allocated_food.html', {'breakfast': breakfast, 'lunch': lunch, 'dinner': dinner})
	else:
		form = AllocateFoodWithPhysicalTraits()
		return render(request, 'alloc/allocate_food_physical.html', {'form': form})


def get_food_range(request):
    if request.method == 'POST':
        form = FoodInfo(request.POST)
		# Have to do something here
        if form.is_valid():
            upper_bound = form.cleaned_data['upper_bound']
            lower_bound = form.cleaned_data['lower_bound']
            breakfast, lunch, dinner = allocate(randint(lower_bound, upper_bound))

            return render(request, 'alloc/allocated_food.html', {'breakfast': breakfast, 'lunch': lunch, 'dinner': dinner})

    else:
        form = FoodInfo()
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





def allocate(calories):
    type1 = (FooDB.objects.filter(food_type = 'Fruit') | FooDB.objects.filter(food_type = 'Nut')).order_by('?')
    type2 = (FooDB.objects.filter(food_type = 'Vegetable') | FooDB.objects.filter(food_type = 'Meat') | FooDB.objects.filter(food_type = 'Legumes')).order_by('?')

    breakfast = []
    lunch = []
    dinner = []

    breakfast_items = [0, 0, 0]
    lunch_items = [0, 0, 0, 0, 0]
    dinner_items = [0, 0, 0, 0, 0]


    for i in range(3):
        breakfast.append(type1[randint(0, len(type1)-1)])
        breakfast_items[i] = [breakfast[i].food]
        breakfast_items[i].append(("("+breakfast[i].food_type+")"))

    for i in range(5):
        lunch.append(type2[randint(0, len(type2)-1)])
        lunch_items[i] = [lunch[i].food]
        lunch_items[i].append(("("+lunch[i].food_type+")"))

        dinner.append(type2[randint(0, len(type2)-1)])
        dinner_items[i] = [dinner[i].food]
        dinner_items[i].append(("("+dinner[i].food_type+")"))


    for i in range(3):
        quantity = (calories/9) * (100/breakfast[i].calories)
        breakfast_items[i].append((str(int(quantity))+"g"))

    for i in range(5):
        quantity = (calories/15) * (100/lunch[i].calories)
        lunch_items[i].append((str(int(quantity))+"g"))

        quantity = (calories/15) * (100/dinner[i].calories)
        dinner_items[i].append((str(int(quantity))+"g"))

    return breakfast_items, lunch_items, dinner_items
