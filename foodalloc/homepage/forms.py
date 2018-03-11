from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
    
class AllocateFoodWithPhysicalTraits(forms.Form):
    height = forms.IntegerField(help_text="Enter height in centimetres")
    weight = forms.IntegerField(help_text="Enter weight in kilograms")
    age = forms.IntegerField(help_text="Enter age")

    # def clean_food_alloc_data(self):
    #     height_cleaned = self.cleaned_data['height']
    #     weight_cleaned = self.cleaned_data['weight']
    #     age_cleaned = self.cleaned_data['age']
        
    #     # Remember to always return the cleaned data.
    #     return data


class FoodInfo(forms.Form):
    lower_bound = forms.IntegerField(help_text="Enter lower bound")
    upper_bound = forms.IntegerField(help_text="Enter upper bound")

class LookupFoodWithFoodName(forms.Form):
    name = forms.CharField(help_text="Enter name of the food", max_length=100)