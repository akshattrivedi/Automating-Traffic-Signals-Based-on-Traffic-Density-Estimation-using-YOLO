from django import forms 
from .models import Traffic

class TrafficForm(forms.ModelForm): 

	class Meta: 
		model = Traffic 
		fields = ['Image_URL'] 
