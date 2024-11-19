#
# @receiver(post_save, sender=Product)
# def create_seo_tags_if_not_exist(sender, instance, created, **kwargs):
#     if created:
#         if not ProductSeoTags.objects.filter(product=instance).exists():
#             instance.create_seo_tags()
