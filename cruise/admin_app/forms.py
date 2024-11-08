from django import forms
from django.apps import apps

def get_dynamic_form(model):
    # Retrieve the model form dynamically
    model_form = type(f"{model._meta.model_name}Form", 
                      (forms.ModelForm,), 
                      {'Meta': type('Meta', (), {'model': model, 'fields': '__all__'})})
    return model_form
