from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from uuslug import uuslug as slugify


class Show(models.Model):
    title = models.CharField(max_length=50, default='',
                             blank=True, null=False)
    slug = models.SlugField(blank=True, max_length=50)
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = models.TextField()
    risk = models.NullBooleanField(choices=((True, 'Very risky'),
                                            (False, 'Not risky')),
                                   default=True)

    def __unicode__(self):
        """Show unicode representation."""
        return self.title

    class Meta:
        ordering = ['start']


@receiver(pre_save, sender=Show, dispatch_uid='create_slug_signal')
def create_slug(sender, instance, raw, **kwargs):
    """Auto create a unique slug."""
    if not instance.slug:
        instance.slug = slugify(instance.title, instance=instance)
