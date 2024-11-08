from django.contrib import admin

from common.models import (
    MailSubscription,
    GlobalCSS,
    StoredCounter,
    CommonSiteSettings,
    FacebookAccessToken,
)


@admin.register(MailSubscription)
class MailSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at")
    search_fields = ("email",)
    list_filter = ("created_at",)


@admin.register(GlobalCSS)
class GlobalCSSAdmin(admin.ModelAdmin):
    change_form_template = "admin/global_css/change_form.html"
    # pass


@admin.register(StoredCounter)
class StoredCounter(admin.ModelAdmin):
    pass


@admin.register(CommonSiteSettings)
class GlobalSetting(admin.ModelAdmin):
    list_display = ("key", "enabled")
    search_fields = ("key",)

    readonly_fields = ("key",)


@admin.register(FacebookAccessToken)
class FacebookAccessTokenAdmin(admin.ModelAdmin):
    pass
