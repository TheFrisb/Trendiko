from django.contrib import admin

from facebook.models import FacebookCampaign


# Register your models here.
class FacebookCampaignsInline(admin.StackedInline):
    model = FacebookCampaign
    extra = 1
    autocomplete_fields = ["product"]
