# coding: utf-8
import uuid
from django.db import models


class CustomEmailField(models.EmailField):
    pass


class CategoryRelation(models.Model):
    category1 = models.ForeignKey('Category', related_name='parents', on_delete=models.CASCADE)
    category2 = models.ForeignKey('Category', related_name='children', on_delete=models.CASCADE)
    type = models.CharField(max_length=30, null=True)

    class Meta:
        db_table = 'category_relation'


class Author(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField()
    email = CustomEmailField(null=True)

    class Meta:
        db_table = 'author'


class Category(models.Model):
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now=True)
    related_coming = models.ManyToManyField('self', symmetrical=False,
                                            through='CategoryRelation', related_name='related_going')

    class Meta:
        db_table = 'category'


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price = models.IntegerField(default=100)
    title = models.CharField(max_length=255, verbose_name="book title")
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL, related_name='books')
    category = models.ManyToManyField(Category, related_name='books')
    content = models.BinaryField()

    class Meta:
        db_table = 'book'
