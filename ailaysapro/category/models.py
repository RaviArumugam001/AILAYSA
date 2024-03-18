from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    status=models.IntegerField(default=1)
    created_date=models.DateTimeField(null=True,blank=True)


class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='subcategories')
    status = models.IntegerField(default=1)
    created_date = models.DateTimeField(null=True, blank=True)


class Artist(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, related_name="songs", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class PostModel(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=264,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CommentModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
