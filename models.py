from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location='.')

class Upload(models.Model):
    title = models.CharField(max_length=250,blank=True)
    filename = models.CharField(max_length=250)
    datetime = models.DateTimeField(auto_created=True,null=True,blank=True)
    file_path = models.FilePathField(path=settings.MEDIA_ROOT,blank=True,null=True)
    slug = models.SlugField(max_length=250)
    user = models.ForeignKey(User)
    downloads = models.IntegerField(default=0)

    def get_absolute_url(self):
        if settings.DEBUG:
            return u'/media/' + self.filename
        else:
            return u'/biogas/upload/%s/' % self.id
    def __unicode__(self):
        return self.filename + u' - ' + self.user.username
    class Meta:
        ordering = ['-datetime']
