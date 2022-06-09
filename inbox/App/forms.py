from django import forms
from App.models import Customer


class Customerform(forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = Customer
        fields = "__all__"


# Function to reply emails


class EmailForm(forms.Form):
    email = forms.EmailField()
    cc = forms.EmailField(required=False)
    subject = forms.CharField(max_length=100)
    attach = forms.FileField(
        required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    message = forms.CharField(widget=forms.Textarea)
