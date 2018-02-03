from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# all models have a default id field that acts as a primary key

class Category(models.Model):
    # store character data
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        # replace whitespace in urls with hyphens
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Page(models.Model):
    # store category, title, url for the page
    # Page has a one-to-many relationships with model Category
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    # links UserProfile to a User model instance
    user = models.OneToOneField(User)

    # additional attributes we wish to include (on top of Django's pre-initialised ones)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
