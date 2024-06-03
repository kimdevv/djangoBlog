from django.db import models
from accounts.models import CustomUser

class Blog(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE) # ForeignKey()는 1:N에서 N 쪽에 작성해준다.
    title = models.CharField(max_length=100)
    body = models.TextField(default="")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
