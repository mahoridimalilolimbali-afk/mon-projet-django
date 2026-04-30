from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Adresse Email")

    class Meta:
        model = User
        fields = ['username', 'email'] # Les champs visibles pour l'utilisateur

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'