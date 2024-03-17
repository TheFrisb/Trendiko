from django.apps import AppConfig


# noinspection PyUnresolvedReferences
class CartConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cart"

    def ready(self):
        import cart.signals
