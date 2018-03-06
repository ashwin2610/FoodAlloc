from django.shortcuts import render
from django.views.generic import TemplateView

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

