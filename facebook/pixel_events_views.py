# make a view that takes a request and creates an initiatecheckout event for it
import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from facebook.services.facebook_pixel import FacebookPixel
from shop.models import Product


class InitiateCheckout(APIView):
    def post(self, request):
        fb_pixel = FacebookPixel(self.request)
        try:
            fb_pixel.checkout(self.request.cart)
        except Exception as e:
            logging.error(
                f"[Facebook Pixel] Error while sending InitiateCheckout event: {e}"
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class ViewContent(APIView):
    def post(self, request, product_slug):
        fb_pixel = FacebookPixel(self.request)
        product = Product.objects.filter(slug=product_slug).first()

        if product:
            try:
                fb_pixel.view_content(product)
            except Exception as e:
                logging.error(
                    f"[Facebook Pixel] Error while sending ViewContent event: {e}"
                )

        return Response(status=status.HTTP_204_NO_CONTENT)
