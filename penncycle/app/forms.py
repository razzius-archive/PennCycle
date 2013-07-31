from django import forms

from crispy_forms.layout import Layout, Submit, Div, Field
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import InlineRadios

from .models import Student


class SignupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                Div(
                    Field(
                        'penncard',
                        placeholder="8 digits",
                    ),
                    'name',
                    'phone',
                    'email', css_class="span5 offset1"
                ), Div(
                    Field(
                        'last_two',
                        placeholder="Usually 00"
                    ),
                    'grad_year',
                    'living_location',
                    InlineRadios('gender'), css_class="span6"
                ), css_class="row-fluid"
            )
        )
        self.helper.form_action = '/signup/'
        self.helper.add_input(Submit('submit', "Submit"))
        self.helper.form_method = 'post'
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
