from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    created_at = models.DateTimeField(_("created at"),auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"),auto_now=True)

    class Meta:
        abstract=True