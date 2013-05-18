from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import simplejson as json

from .models import Show, Rating


def list_shows(request):
    """List shows view."""
    shows = Show.objects.all()
    return render(request, 'list_shows.html', {'shows': shows})


def view_show(request, slug):
    """View show view."""
    show = get_object_or_404(Show, slug=slug)

    if show.rated_show.filter(user=request.user.id):
        user_rating = show.rated_show.filter(
            user=request.user.id)[0].rating
    else:
        user_rating = 0

    return render(request, 'view_show.html',
                  {'show': show,
                   'votes': show.get_rating_votes(),
                   'user_rating': user_rating})


def rate_show(request, slug):
    """View for user to rate a show."""
    show = get_object_or_404(Show, slug=slug)
    rating_input = int(request.POST.get('rating')) or None

    data = {
        'user_rating': rating_input,
        'overall_rating': 0
    }
    if not rating_input:
        pass
    else:
        try:
            rating = Rating.objects.get(user__pk=request.user.id,
                                        show__pk=show.id)
        except Rating.DoesNotExist:
            rating = Rating(user=request.user, show=show)
        rating.rating = rating_input
        rating.save()
        show_overall_rating = show.get_avg_rating()
        data['overall_rating'] = round(show_overall_rating, 1)
        data['number_of_votes'] = show.get_rating_votes()

    return HttpResponse(json.dumps(data), mimetype='application/json')
