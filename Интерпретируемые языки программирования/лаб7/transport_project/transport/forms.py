from django import forms
from .models import Trips

class TripForm(forms.ModelForm):
    class Meta:
        model = Trips
        fields = '__all__'