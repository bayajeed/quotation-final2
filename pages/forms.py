from django import forms
from .models import Quotation, Item, ItemGroup, Unit

class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ['title', 'client_name']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        widgets = {
            'group': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        group = cleaned_data.get("group")
        name = cleaned_data.get("name")

        if group and name:
            # Check for uniqueness for new objects
            if not self.instance.pk and Item.objects.filter(group=group, name=name).exists():
                raise forms.ValidationError("This item already exists in this group.")

            # Check for uniqueness when updating an existing object
            if self.instance.pk and Item.objects.filter(group=group, name=name).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("This item already exists in this group.")

        return cleaned_data

class ItemGroupForm(forms.ModelForm):
    class Meta:
        model = ItemGroup
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }