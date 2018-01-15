from django.db import models

# all models have a default id field that acts as a primary key

class Category(models.Model):
    # store character data
    name = models.CharField(max_length=128, unique=True)

    def __self__(self):
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