from django import forms
from .models import Contact

class ContactsForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'id',
            'name',
            'last_name',
            'phone_number',
            'mail',
            'photo'
        ]