from django.http import FileResponse

from facebook.services.catalogue_management import CatalogueManager


# Create your views here.
def feed_facebook_catalogue(request):
    ctlg_service = CatalogueManager()

    return FileResponse(
        ctlg_service.make_xlsx_catalogue_feed(),
        as_attachment=True,
        filename="facebook_catalogue_feed.xlsx",
    )
