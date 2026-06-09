from django.db import models
from django.contrib.auth.models import User


class Reel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reels")
    video = models.FileField(upload_to="reels")
    caption = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}'s Reel ({self.id})"


class ReelLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reel_likes")
    reel = models.ForeignKey(Reel, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "reel")

    def __str__(self):
        return f"{self.user.username} likes Reel {self.reel.id}"


class ReelComment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reel_comments"
    )
    reel = models.ForeignKey(Reel, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} on Reel {self.reel.id}"
