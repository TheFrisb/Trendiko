"""
URL configuration for trendiko project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


sitemaps = {
    # 'products': ProductSitemap,
    # 'categories': CategorySitemap,
    # 'static': StaticViewSitemap,
}

urlpatterns = [
    # THIRD PARTY APPS URLS
    path("ckeditor/", include("ckeditor_uploader.urls")),
    # END THIRD PARTY APPS URLS
    path("admin/", admin.site.urls),
    path("shop-manager/", include("shop_manager.urls")),
    path("api/cart/", include("cart.urls")),
    path("api/stock/", include("stock.urls")),
    path("api/facebook/", include("facebook.urls")),
    # path("facebook/", include("facebook.urls")),
    path("", include("shop.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
