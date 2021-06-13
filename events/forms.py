from ckeditor.widgets import CKEditorWidget
from django import forms
from django.forms import ModelForm, Textarea
from .models import Venue, Event

class EventForm(ModelForm):
    description = forms.CharField(widget=CKEditorWidget)
    class Meta:
        model = Event
        fields = ['name', 'event_date', 'description']
        



class MyFormWidget(forms.TextInput):
    class Media:
        css = {
                'all':('widget.css',)
        }


class VenueForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Venue
        fields = '__all__'
        widgets = {
            'name':MyFormWidget(attrs={'class':'mywidget'}),
            'address':Textarea(attrs={'cols':40, 'rows':3}),
            }

    class Media:
        css = {
            'all':('form.css',)
        }
        js = ('mycustom.js',)

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        email_address = cleaned_data.get("email_address")

        if not(phone or email_address):
            raise forms.ValidationError(
                "You must enter a phone number or email, or both."
            )