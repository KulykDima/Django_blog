from uuid import uuid4

from accounts.models import User

from django.db import models


class Posts(models.Model):
    uuid = models.UUIDField(default=uuid4, db_index=True, unique=True)
    title = models.CharField(max_length=30)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    like = models.ManyToManyField(User, blank=True, related_name='likes')
    dislike = models.ManyToManyField(User, blank=True, related_name='dislikes')
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'posts'
