from .models import Table, US_SIZES
from django.forms import ModelForm, DateInput, NumberInput, Select, TextInput


class TableForm(ModelForm):
    class Meta:
        model = Table
        fields = ["title", "size", "price", "sellprice", "anyprice", "datebuy", "datesell", "notes"]
        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Model Name'
            }),
            "size": Select(choices=US_SIZES, attrs={
                'class': 'form-select',
                'aria-label': '.form-select-lg example',
                'placeholder': 'Model Size'
            }),
            "price": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Model Price'
            }),
            "sellprice": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Model Sell Price'
            }),
            "anyprice": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Доп расходы'
            }),
            "datebuy": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата покупки',
                'type': 'date'
            }),
            "datesell": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата продажи',
                'type': 'date'
            }),
            "notes": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заметки'
            }),
        }
