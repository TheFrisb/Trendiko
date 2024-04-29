from django.http import HttpResponse


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /checkout/",
        "Disallow: /cart/",
        "Disallow: /user/",
        "Disallow: /profile/",
        "Disallow: /order/",
        "Disallow: /api/",
        "Disallow: /settings/",
        "Disallow: /login/",
        "Disallow: /register/",
        "Disallow: /thank-you/",
        "Sitemap: https://www.trendiko.mk/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
