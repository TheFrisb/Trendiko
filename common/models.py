from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill


IMAGE_DIMENSIONS = (550, 550)
THUMBNAIL_DIMENSIONS = (250, 250)
IMAGE_QUALITY = 95


# Create your models here.
class TimeStampedModel(models.Model):
    """Time Stamped Model"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta Class"""

        abstract = True


class BaseProduct(TimeStampedModel):
    """Time Stamped Product Model"""

    title = models.CharField(max_length=255)
    thumbnail = ProcessedImageField(
        upload_to="products/%Y/%m/%d/",
        processors=[ResizeToFill(*IMAGE_DIMENSIONS)],
        format="WEBP",
        options={"quality": IMAGE_QUALITY},
        null=True,
        blank=True,
    )
    thumbnail_as_jpeg = ImageSpecField(source="thumbnail", format="JPEG")
    thumbnail_loop = ImageSpecField(
        source="thumbnail",
        processors=[ResizeToFill(*THUMBNAIL_DIMENSIONS)],
        format="WEBP",
        options={"quality": IMAGE_QUALITY},
    )
    thumbnail_loop_as_jpeg = ImageSpecField(
        source="thumbnail",
        processors=[ResizeToFill(*THUMBNAIL_DIMENSIONS)],
        format="JPEG",
        options={"quality": IMAGE_QUALITY},
    )

    class Meta:
        """Meta Class"""

        abstract = True

    def __str__(self):
        return self.title
