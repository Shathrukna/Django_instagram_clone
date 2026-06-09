from django import template

register = template.Library()


@register.filter
def time_ago(value):
    """Convert a datetime to a relative time string."""
    from django.utils import timezone
    now = timezone.now()
    diff = now - value

    if diff.days > 365:
        years = diff.days // 365
        return f"{years}y"
    elif diff.days > 30:
        months = diff.days // 30
        return f"{months}mo"
    elif diff.days > 0:
        return f"{diff.days}d"
    elif diff.seconds > 3600:
        return f"{diff.seconds // 3600}h"
    elif diff.seconds > 60:
        return f"{diff.seconds // 60}m"
    else:
        return "just now"
