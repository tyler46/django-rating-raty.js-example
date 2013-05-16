import django.utils.timezone as timezone

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg, Count
from django.db.models.signals import pre_save
from django.dispatch import receiver

from uuslug import uuslug as slugify


RATING_CHOICES = (
    (1, 'bad'),
    (2, 'poor'),
    (3, 'regular'),
    (4, 'good'),
    (5, 'gorgeus'),)


class ShowManager(models.Manager):
    """Adds custom methods to Show model."""
    def top_rated(self):
        return self.annotate(score=Avg('rated_show__rating')).order_by('-score')

    def most_rated(self):
        return self.annotate(score=Avg('rated_show')).order_by('-score')


class Show(models.Model):
    """Show model."""
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

    def get_avg_rating(self):
        """Returns the average rating for a show."""
        if self.rated_show.all():
            return self.rated_show.aggregate(Avg('rating'))['rating__avg']
        else:
            return 0.00

    def get_latest_rating(self):
        """Returns latest rating for a show.
        (instance of Rating)
        """
        return self.rated_show.all().order_by('-date_rated')[0]

    def get_rating_votes(self):
        """Returns all rating votes for a show."""
        return self.rated_show.all().count()

    class Meta:
        ordering = ['start']

    objects = ShowManager()


class Rating(models.Model):
    """Rating model for Show model."""
    show = models.ForeignKey('Show', related_name='rated_show')
    user = models.ForeignKey(User, related_name='user_rated')
    rating = models.IntegerField(choices=RATING_CHOICES, default=1)
    date_rated = models.DateTimeField(editable=False)

    def __unicode__(self):
        return u'%s rated %s (%s)' % (self.user, self.show,
                                      self.get_rating_display())

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_rated = timezone.now()
        super(Rating, self).save(*args, **kwargs)


@receiver(pre_save, sender=Show, dispatch_uid='create_slug_signal')
def create_slug(sender, instance, raw, **kwargs):
    """Auto create a unique slug."""
    if not instance.slug:
        instance.slug = slugify(instance.title, instance=instance)
