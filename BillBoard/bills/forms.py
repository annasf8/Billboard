from django import forms
from .models import Bill, Click
from ckeditor.fields import RichTextFormField


class BillForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        categories_choices = kwargs.pop('categories_choices', None)
        super().__init__(*args, **kwargs)
        if categories_choices:
            self.fields['categories'].queryset = categories_choices

    # image = forms.ImageField(required=False)
    # video_url = forms.URLField(required=False)

    class Meta:
        model = Bill
        fields = ['categories', 'title', 'text_bill']
        widgets = {
            'text_bill': RichTextFormField(),
        }

class ClickForm(forms.ModelForm):
    class Meta:
        model = Click
        fields = ['text_click']