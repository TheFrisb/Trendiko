from facebook.services.api_connection import FacebookApi
from facebook.services.catalogue_management import CatalogueManager


def update_facebook_catalogue_feed():
    """
    Update the Facebook catalogue feed.
    """
    catalogue_management = CatalogueManager()
    catalogue_management.make_csv_catalogue_feed()


def refresh_facebook_access_token():
    """
    Refresh the Facebook access token.
    """
    fb_api = FacebookApi()
    fb_api.refresh_access_token()
