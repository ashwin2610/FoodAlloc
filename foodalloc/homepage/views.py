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

@login_required
def set_preferences(request):
    if request.method == 'POST':
        form = LookupFoodWithFoodName(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            items = FooDB.objects.filter(food__iexact=name)
            user_name = request.user.username

            if "set" in request.POST:
                for item in items:
                    if item.preferences == '0':
                        item.preferences = user_name

                    else:
                        item.preferences = item.preferences + ', ' + user_name
                    item.save()

            elif "remove" in request.POST:
                for item in items:
                    if ',' in item.preferences:
                        if user_name in item.preferences:
                            item.preferences = item.preferences.replace(user_name + ', ', '')
                    else:
                        if user_name in item.preferences:
                            item.preferences = item.preferences.replace(user_name, '0')
                    item.save()

        return HttpResponseRedirect('/prefer')
    else:
        form = LookupFoodWithFoodName()
        return render(request, 'prefer.html', {'form': form})



@login_required
def set_alternatives(request):
    if request.method == 'POST':
        form = LookupFoodWithFoodName(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            items = FooDB.objects.filter(food__icontains=name)
            user_name = request.user.username


            if "set" in request.POST:
                for item in items:
                    if item.alternatives == '0':
                        item.alternatives = user_name

                    else:
                        item.alternatives = item.alternatives + ', ' + user_name
                    item.save()

            elif "remove" in request.POST:
                for item in items:
                    if ',' in item.alternatives:
                        if user_name in item.alternatives:
                            item.alternatives = item.alternatives.replace(user_name + ', ', '')
                    else:
                        if user_name in item.alternatives:
                            item.alternatives = item.alternatives.replace(user_name, '0')
                    item.save()
        return HttpResponseRedirect('/alter')
    else:
        form = LookupFoodWithFoodName()
        return render(request, 'alter.html', {'form': form})


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

        breakfast, lunch, dinner = allocate(request, calories_required)

        return render(request, 'alloc/allocated_food.html', {'breakfast': breakfast, 'lunch': lunch, 'dinner': dinner})
    else:
        form = AllocateFoodWithPhysicalTraits()
        return render(request, 'alloc/allocate_food_physical.html', {'form': form})


def get_food_range(request):
    if request.method == 'POST':
        form = FoodInfo(request.POST)

        if form.is_valid():
            upper_bound = form.cleaned_data['upper_bound']
            lower_bound = form.cleaned_data['lower_bound']
            breakfast, lunch, dinner = allocate(request, randint(lower_bound, upper_bound))

            return render(request, 'alloc/allocated_food.html', {'breakfast': breakfast, 'lunch': lunch, 'dinner': dinner})

    else:
        form = FoodInfo()
        return render(request, 'alloc/allocate_food_physical.html', {'form': form})


def get_food_info(request):
    if request.method == 'POST':
        form = FoodInfo(request.POST)

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

        if form.is_valid():
            name = form.cleaned_data['name']
            items = FooDB.objects.filter(food__iexact=name)
            return render(request, 'alloc/result.html', {'items': items})

    else:
        form = LookupFoodWithFoodName()
        return render(request, 'alloc/allocate_food_physical.html', {'form': form})




def allocate(request, calories):
    type1 = (FooDB.objects.filter(food_type = 'Fruit') | FooDB.objects.filter(food_type = 'Nut')).exclude(preferences__iexact = request.user.username).exclude(alternatives__iexact = request.user.username).order_by('?')
    type2 = (FooDB.objects.filter(food_type = 'Vegetable') | FooDB.objects.filter(food_type = 'Meat') | FooDB.objects.filter(food_type = 'Legumes')).exclude(preferences__iexact = request.user.username).exclude(alternatives__iexact = request.user.username).order_by('?')

    type1_pref = (FooDB.objects.filter(food_type = 'Fruit') | FooDB.objects.filter(food_type = 'Nut')).filter(preferences__iexact = request.user.username)
    type2_pref = (FooDB.objects.filter(food_type = 'Vegetable') | FooDB.objects.filter(food_type = 'Meat') | FooDB.objects.filter(food_type = 'Legumes')).filter(preferences__iexact = request.user.username)


    breakfast = []
    lunch = []
    dinner = []

    low_calorie = ['Pepper', 'Lemon', 'Lime', 'Wasabi', 'Olives', 'Black Olives', 'Green Olives', 'Garlic', 'Tamarind']

    breakfast_items = [0, 0, 0]
    lunch_items = [0, 0, 0, 0, 0]
    dinner_items = [0, 0, 0, 0, 0]


    for i in range(3):
        if len(type1_pref) == 0:
            breakfast.append(type1[randint(0, len(type1)-1)])
        else:
            index = randint(0, len(type1_pref)-1)
            breakfast.append(type1_pref[index])
            type1_pref = type1_pref[:index] + type1_pref[index+1 : len(type1_pref)]

        breakfast_items[i] = [breakfast[i].food]
        breakfast_items[i].append(("("+breakfast[i].food_type+")"))


    for i in range(5):
        if len(type2_pref) == 0:
            lunch.append(type2[randint(0, len(type2)-1)])
        else:
            index = randint(0, len(type2_pref)-1)
            lunch.append(type2_pref[index])
            type2_pref = type2_pref[:index] + type2_pref[index+1 : len(type2_pref)]

        lunch_items[i] = [lunch[i].food]
        lunch_items[i].append(("("+lunch[i].food_type+")"))


        if len(type2_pref) == 0:
            dinner.append(type2[randint(0, len(type2)-1)])
        else:
            index = randint(0, len(type2_pref)-1)
            dinner.append(type2_pref[index])
            type2_pref = type2_pref[:index] + type2_pref[index+1 : len(type2_pref)]

        dinner_items[i] = [dinner[i].food]
        dinner_items[i].append(("("+dinner[i].food_type+")"))



    for i in range(3):
        if breakfast[i].food in low_calorie:
            quantity = 30
        else:
            quantity = (calories/9) * (100/breakfast[i].calories)

        if quantity > 350:
            quantity = 350
        breakfast_items[i].append((str(int(quantity))+"g"))

    for i in range(5):
        if lunch[i].food in low_calorie:
            quantity = 30
        else:
            quantity = (calories/15) * (100/lunch[i].calories)
        if quantity > 350:
            quantity = 350
        lunch_items[i].append((str(int(quantity))+"g"))


        if dinner[i].food in low_calorie:
            quantity = 30
        else:
            quantity = (calories/15) * (100/dinner[i].calories)

        if quantity > 350:
            quantity = 350
        dinner_items[i].append((str(int(quantity))+"g"))

    return breakfast_items, lunch_items, dinner_items
