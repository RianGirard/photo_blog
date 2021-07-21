from django.contrib.auth.models import User
from django.db import models

PUBLISHED_CHOICES = (
    ('yes', 'YES'),
    ('no', 'NO')
)

class Post(models.Model):
    title = models.CharField(max_length=240)
    desc = models.TextField(blank=True, null=True)
    published = models.CharField(max_length=3, choices=PUBLISHED_CHOICES, default='no')
    # published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title[0:100]

class Photo(models.Model):
    # file = models.FileField(upload_to='blog/', null=True)
    file = models.ImageField(upload_to='blog/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        blank=True, 
        null=True
    )
    
    def __str__(self):
        return f'{self.id} - {self.created_at}'


class Comment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(
        Post, 
        related_name= "post_comments", 
        on_delete= models.CASCADE
    )
    author = models.ForeignKey(
        User, 
        related_name= "user_comments", 
        on_delete= models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__ (self):
        return f"<Comment: {self.id} {self.author.username }{self.comment}[0:30]>"



# Create your models here.
