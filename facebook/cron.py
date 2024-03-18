from facebook.services.catalogue_management import CatalogueManager


def update_facebook_catalogue_feed():
    """
    Update the Facebook catalogue feed.
    """
    catalogue_management = CatalogueManager()
    catalogue_management.make_xlsx_catalogue_feed()
