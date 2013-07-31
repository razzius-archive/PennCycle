from django import forms

from crispy_forms.layout import Layout, Field
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import InlineRadios

from app.models import Student


class SignupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field(
                'penncard',
                placeholder="8 digits",
            ),
            'name',
            'phone',
            'email',
            Field(
                'last_two',
                placeholder="Usually 00"
            ),
            'grad_year',
            'living_location',
            InlineRadios('gender')
        )
        self.fields['last_two'].label = "Last two digits of PennCard"
        self.fields['penncard'].label = "PennCard Number"

    class Meta:
        model = Student
        fields = [
            'penncard',
            'name',
            'phone',
            'email',
            'last_two',
            'grad_year',
            'living_location',
            'gender',
        ]

    gender = forms.TypedChoiceField(
        choices=(("M", "Male"), ("F", "Female")),
    )
