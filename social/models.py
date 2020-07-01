from django.db import models
from django.contrib.auth.models import User

# Post model 
class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.CharField(max_length = 500)
    genre = models.CharField(max_length=20)
    header = models.CharField(max_length=50)
    def __str__(self):
        return self.header

# comment model
class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    text = models.CharField(max_length = 500)
    def __str__(self):
        return self.text
