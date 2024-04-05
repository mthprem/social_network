from django.db import models
from django.contrib.auth.models import User


class FriendRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    )

    from_user = models.ForeignKey(
        User, related_name='sent_requests', on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User, related_name='received_requests', on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f'from_user: {self.from_user}, to_user: {self.to_user}, '
            f'status: {self.status}'
        )

    class Meta:
        unique_together = ('from_user', 'to_user', 'status')
