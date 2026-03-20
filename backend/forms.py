from django.forms import ModelForm
from backend.models import *

class CategoryForm(ModelForm):
    class Meta:
        model =pro_category
        fields="__all__"

class ProductForm(ModelForm):
    class Meta:
        model = protable
        fields = "__all__"