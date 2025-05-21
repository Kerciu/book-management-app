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
                raise ValidationError(
                    "Cannot modify shelf type of existing default shelves")

        return cleaned_data


@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    form = ShelfAdminForm
    list_display = ('name', 'user', 'shelf_type_display', 'is_default', 'created_at')
    list_filter = ('is_default', 'shelf_type', 'created_at')
    search_fields = ('name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'is_default', 'shelf_type')
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def shelf_type_display(self, obj):
        return obj.get_shelf_type_display()
    shelf_type_display.short_description = 'Shelf Type'

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.is_default:
            return ['is_default', 'shelf_type'] + self.readonly_fields
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        try:
            return super().save_model(request, obj, form, change)
        except ValidationError as e:
            self.message_user(request, str(e), level=messages.ERROR)
