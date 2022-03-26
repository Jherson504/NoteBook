from django.contrib import admin
from .models import Article, Book, Log, Message, Section, Tag, Topic

admin.site.register(Article)
admin.site.register(Book)
admin.site.register(Section)
admin.site.register(Message)
admin.site.register(Tag)
admin.site.register(Topic)
admin.site.register(Log)
