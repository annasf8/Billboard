from django.contrib import admin
from . import forms
from .models import Bill, Click
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

admin.site.register(Bill)
admin.site.register(Click)


# Register your models here.
#
# class BillAdminForm(forms.ModelForm):
#     text_bill = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
#
#     class Meta:
#         model = Bill
#         fields = '__all__'


# class BillAdmin(admin.ModelAdmin):
#     form = BillAdminForm
