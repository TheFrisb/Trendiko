from django.contrib import admin

from analytics.models import CampaignSummary, CampaignEntry, PriceChange


# Register your models here.
@admin.register(CampaignSummary)
class CampaignSummaryAdmin(admin.ModelAdmin):
    pass


@admin.register(CampaignEntry)
class CampaignEntryAdmin(admin.ModelAdmin):
    pass


@admin.register(PriceChange)
class PriceChangeAdmin(admin.ModelAdmin):
    autocomplete_fields = ["product", "attribute"]
