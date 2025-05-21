from django import forms
from .models import Shelf
from django.core.exceptions import ValidationError


class ShelfForm(forms.ModelForm):
    class Meta:
        model = Shelf
        fields = ['name']

    def clean(self):
        cleaned_data = super().clean()
        user = self.instance.user if self.instance else None

        if self.isinstance and self.instance.is_default:
            raise ValidationError("Cannot modify default shelves")

        if Shelf.objects.filter(user=user, name=cleaned_data['name']).exists():
            raise ValidationError("You already have a shelf with this name")
        
        return cleaned_data
