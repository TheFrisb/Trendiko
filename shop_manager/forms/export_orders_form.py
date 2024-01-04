from django import forms


class ExportOrdersForm(forms.Form):
    from_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "dateInput",
                "placeholder": "Select a date",
                "required": "required",
            }
        )
    )
    to_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "dateInput",
                "placeholder": "Select a date",
                "required": "required",
            }
        )
    )
