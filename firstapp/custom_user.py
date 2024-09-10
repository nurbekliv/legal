from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from django.utils.text import slugify
User = get_user_model()


class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    user_photo = models.ImageField(upload_to='profile_pics')
    bio = models.TextField(max_length=500)

    def __str__(self):
        return self.username


class Sections(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Sections'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    section = models.ForeignKey(Sections, on_delete=models.CASCADE, related_name='lessons_in_section')
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    description = models.TextField()
    body = RichTextField()
    order = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class WatchedList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sections = models.IntegerField()
    lessons = models.IntegerField()

    def __str__(self):
        return self.user
