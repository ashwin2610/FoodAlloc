from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
    
class AllocateFoodWithPhysicalTraits(forms.Form):
    height = forms.IntegerField(help_text="Enter height in centimetres")
    weight = forms.IntegerField(help_text="Enter weight in kilograms")
    age = forms.IntegerField(help_text="Enter age")
    
    gender_choices=[('M','Male'), ('F','Female')]

    gender = forms.ChoiceField(help_text="Select gender", choices=gender_choices, widget=forms.RadioSelect)

    def clean_food_alloc_data(self):
        height_cleaned = self.cleaned_data['height']
        weight_cleaned = self.cleaned_data['weight']
        age_cleaned = self.cleaned_data['age']
        gender_cleaned = self.cleaned_data['gender']

        
        # Remember to always return the cleaned data.
        return height_cleaned, weight_cleaned, age_cleaned, gender_cleaned



class FoodInfo(forms.Form):
    lower_bound = forms.IntegerField(help_text="Enter lower bound")
    upper_bound = forms.IntegerField(help_text="Enter upper bound")

class LookupFoodWithFoodName(forms.Form):
    name = forms.CharField(help_text="Enter name of the food", max_length=100)