from django import forms

from common.utils import get_euro_value_in_mkd
from facebook.services.api_connection import FacebookApi


class RetrieveAdspendForm(forms.Form):
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

    def retrieve_adspend(self):
        from_date = self.cleaned_data["from_date"]
        to_date = self.cleaned_data["to_date"]

        fb_api = FacebookApi()

        ad_spend_eur = float(
            fb_api.get_total_adspend_for_time_range(from_date, to_date)[0]["spend"]
        )
        ad_spend_mkd = get_euro_value_in_mkd(value=ad_spend_eur)

        return {
            "ad_spend_eur": ad_spend_eur,
            "ad_spend_mkd": ad_spend_mkd,
        }

    @property
    def get_template_id(self):
        return "retrieveAdspendForm"
