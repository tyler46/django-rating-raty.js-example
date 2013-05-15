from django.contrib import admin

from .models import Rating, Show


class RatingInline(admin.StackedInline):
    """Rating Inline."""
    model = Rating
    extra = 1


class ShowAdmin(admin.ModelAdmin):
    inlines = [RatingInline]
    model = Show
    exclude = ('slug', )
    list_display = ('title', 'description', )


admin.site.register(Show, ShowAdmin)
