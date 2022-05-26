# Create your models here.
from category.models import Category
from django.db import models


class Post(models.Model):
    cate = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_post")
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=50)
    content = models.TextField()
    like = models.IntegerField(default='0')
    created = models.DateTimeField(auto_now_add=True)

    def one_four_posts(self):
        return Post.objects.all().filter(Category=self)[:3]

    def __str__(self):
        return self.content
