from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.views import APIView

from shop_manager.forms.retrieve_adspend import RetrieveAdspendForm


class TotalAdSpend(APIView):
    # require only authenticated users to access this view
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        form = RetrieveAdspendForm(request.query_params)
        if form.is_valid():
            ad_spend = form.retrieve_adspend()
            return JsonResponse(ad_spend, status=200)
        else:
            return JsonResponse(form.errors, status=400)
