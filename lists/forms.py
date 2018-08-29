from django import forms
from .models import Widget

class WidgetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WidgetForm, self).__init__(*args, **kwargs)
        self.fields['my_extra_field'] = forms.CharField()

    class Meta:
        model = Widget
