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
    fieldsets = (
        (
            "Global CSS",
            {
                "fields": ("css",),
                "description": "Add or update the global CSS styles.",
            },
        ),
        (
            "Cart Sections",
            {
                "fields": (
                    "cart_section_one",
                    "cart_section_two",
                    "cart_section_three",
                    "cart_section_four",
                    "cart_section_five",
                ),
                "description": "Add html for various cart sections.",
            },
        ),
        (
            "Checkout Sections",
            {
                "fields": (
                    "checkout_section_one",
                    "checkout_section_two",
                    "checkout_section_three",
                ),
                "description": "Add html for various checkout sections.",
            },
        ),
    )
    list_display = (
        "__str__",
        "updated_at",
        "created_at",
    )  # Customize display columns if needed


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
