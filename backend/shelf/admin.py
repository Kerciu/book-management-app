from django.contrib import admin
from django import forms
from django.contrib import messages
from .models import Shelf
from django.core.exceptions import ValidationError

class ShelfAdminForm(forms.ModelForm):
    class Meta:
        model = Shelf
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        instance = self.instance

        if cleaned_data.get('is_default', False):
            if not cleaned_data.get('shelf_type'):
                raise ValidationError("Default shelves must have a shelf type")

            shelf_type = cleaned_data['shelf_type']
            cleaned_data['name'] = dict(Shelf.SHELF_TYPES).get(shelf_type, '')

        if instance and instance.pk and instance.is_default:
            if 'shelf_type' in self.changed_data:
                raise ValidationError("Cannot modify shelf type of existing default shelves")

        return cleaned_data
