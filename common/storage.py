from django.conf import settings
from django.core.files.storage import FileSystemStorage


class InvoicesStorage(FileSystemStorage):
    def __init__(self, location=settings.INVOICES_DIR, *args, **kwargs):
        super().__init__(location, *args, **kwargs)
