from django.db.models import Q
from users.models import Follow
from django.contrib.auth.models import User


def suggested_users(request):
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            follower=request.user
        ).values_list("following", flat=True)
        suggested = (
            User.objects.exclude(Q(id__in=following) | Q(id=request.user.id))
            .filter(is_superuser=False)
            .order_by("?")[:5]
        )
        return {"suggested_users": suggested}
    return {}
