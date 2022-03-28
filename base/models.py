from django.db import models
from django.contrib.auth.models import User

# topics


class Topic(models.Model):

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# tags


class Tag(models.Model):

    name = models.CharField(max_length=80)
    description = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created', ]

# books


class Book(models.Model):

    tags = models.ManyToManyField(Tag,  related_name="book_tags")
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    topics = models.ManyToManyField(
        Topic, related_name="book_topics")
    description = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created', '-updated']

# articles


class Article(models.Model):

    book = models.ForeignKey(Book, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topics = models.ManyToManyField(
        Topic, related_name="article_topics")
    tags = models.ManyToManyField(Tag, related_name="article_tags")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created', 'updated']

    def __str__(self):
        return f"{self.book.title}/{self.title}/"

# sections


class Section(models.Model):
    title = models.CharField(max_length=200)
    article = models.ForeignKey(Article, null=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="section_tags")
    topics = models.ManyToManyField(
        Topic, related_name="section_topics")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.article.title}/{self.title}"

    class Meta:
        ordering = ['created', 'updated']

# messages


class Message(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    message = models.ForeignKey(
        'self', related_name='reply', on_delete=models.SET_NULL, null=True)

    body = models.TextField()

    def __str__(self):
        return self.body[:50]


# debugging models
class FormTesterModel(models.Model):
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created)


class Log(models.Model):
    body = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created.__str__()
