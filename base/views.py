from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Article, Book, FormTesterModel, Section, Topic, Tag
from django.db.models.query import Q


class BookUtil:
    def __init__(self):
        pass

    @staticmethod
    def remove_duplicates():
        _all_books = Book.objects.all()
        for book in _all_books:
            _all_articles = book.article_set.all()
            _article_titles = []
            for article in _all_articles:
                if article.title not in _article_titles:
                    _article_titles.append(article.title)
                else:
                    article.delete()

    def book_save(self, book: Book, form: dict):
        duplicates = []
        for key, value in form.items():
            keys = key.split('.')

            if len(keys) == 3:
                _obj, _id, _attr = keys

                if _obj.lower() == 'article':
                    _article = Article.objects.get(id=int(_id))

                    if _article:
                        _article.__setattr__(_attr, value)

                        if self.validated(book, _article, _attr):
                            _article.save()
                        else:
                            _article.delete()

                elif _obj.lower() == 'section':
                    _section = Section.objects.get(id=int(_id))

                    if _section:
                        _section.__setattr__(_attr, value)

                        if self.validated(book, _section, _attr):
                            _section.save()
                        else:
                            _section.delete()

    @staticmethod
    def validated(book, fm: Article, attr) -> bool:
        # print(f"Validating {book}.{fm}...\n")
        _all_articles = Article.objects.all()
        for _article in _all_articles:
            if fm != _article and _article.book == book:
                if fm.__getattribute__(attr) == _article.__getattribute__(attr):
                    return False
        return True

    @staticmethod
    def validated(book, fm: Section, attr) -> bool:
        # print(f"Validating {book}.{fm}...\n")
        _all_sections = Section.objects.all()
        for _section in _all_sections:
            if fm != _section and _section.article in book.article_set.all():
                if fm.__getattribute__(attr) == _section.__getattribute__(attr):
                    return False
        return True

    @staticmethod
    def form_process(form):
        form = dict(form)
        return form

    def form_create_book(self, form: dict):
        __id = None
        for key, value in form.items():
            keys = key.split('.')
            if len(keys) == 3:
                _obj, _id, _attr = keys
                _ = self._set_attr(_obj, _id, _attr, value)
                if __id is None:
                    __id = _
        return __id

    @staticmethod
    def _set_attr(_form) -> int:
        _new_book = Book.objects.create()
        for keys, value in _form.items():
            print(keys, value)
            if len(keys.split('.')) == 3:
                _obj, _id, _attr = keys.split('.')
                if _id == 'null':
                    if _obj.lower() == 'book':
                        print(f"setting {_attr} to {value}...")
                        _new_book.__setattr__(_attr, value)
                        _new_book.save()
                else:
                    if _obj.lower() == 'book':
                        print(f"setting {_attr} to {value}...")
                        _book = Book.objects.get(id=_id)
                        _book.__setattr__(_attr, value)
                        _book.save()
                    elif _obj.lower() == 'section':
                        print(f"setting {_attr} to {value}...")
                        _object = Section.objects.get(id=_id)
                        _new_book.section_set.add(_object)
                        _new_book.save()
                    elif _obj.lower() == 'article':
                        print(f"setting {_attr} to {value}...")
                        _object = Article.objects.get(id=_id)
                        _new_book.article_set.add(_object)
                        _new_book.save()
                    elif _obj.lower() == 'tags':
                        print(f"setting {_attr} to {value}...")
                        _object = Tag.objects.get(id=_id)
                        _object.book_set.add(_new_book)
                        _new_book.save()
                    elif _obj.lower() == 'topic':
                        print(f"setting {_attr} to {value}...")
                        _object = Topic.objects.get(id=_id)
                        _object.book_set.add(_new_book)
                        print("This is line 265!")
                        _new_book.save()
        return int(_new_book.id)


# [+] HOME [+]
def home(request):
    q = request.GET.get('q')
    q = q if q is not None else ''

    _books = Book.objects.filter(topics__name__icontains=q).distinct()
    _topics = Topic.objects.all()
    context = {'books': _books, 'topics': _topics}
    return render(request, 'base/home.html', context)
# [-] HOME [-]


# [+] AUTH [+]
def authenticate_user(request):
    return redirect('login')


# login
def login_page(request):
    if request.method == "POST":
        form_data = request.POST
        _username = form_data.get('username')
        _password = form_data.get('password')
        try:
            User.objects.get(username=_username)
        except:
            messages.error(request, 'Username does not exists!')
            return redirect('login')

        _user = authenticate(
            request, username=_username, password=_password)
        if _user:
            login(request, _user)
        else:
            messages.error(request, 'Incorrect username or password!')
            return redirect('login')

        return redirect('home')

    return render(request, 'base/auth/login.html')


# sign in
def sign_in_page(request):
    return render(request, 'base/auth/sign-in.html')


# logout
def logout_page(request):
    if request.method == 'get':
        logout(request)
        return redirect('home')
    return render(request, 'base/auth/logout.html')
# [-] AUTH [-]


# [+] BOOK [+]
# view
def book_view(request, pk):
    return render(request, 'base/book/view.html')


# create
def book_create(request):
    return render(request, 'base/book/create.html')


# edit
def book_edit(request, pk):
    return render(request, 'base/book/edit.html')
# [-] BOOK [-]


# [+] ARTICLE [+]
# view
def article_view(request, pk):
    return render(request, 'base/article/view.html')


# create
def article_create(request):
    return render(request, 'base/article/create.html')


# edit
def article_edit(request, pk):
    return render(request, 'base/article/edit.html')
# [-] ARTICLE [-]


# [+] SECTION [+]
# view
def section_view(request, pk):
    return render(request, 'base/section/view.html')


# create
def section_create(request):
    return render(request, 'base/section/create.html')


# edit
def section_edit(request, pk):
    return render(request, 'base/section/edit.html')
# [-] BOOK [-]


# [!] RESET DATA [!]
def data_reset(request):
    __all_sections = Section.objects.all()
    for _section in __all_sections:
        _section.delete()
    __all_sections = Article.objects.all()
    for _section in __all_sections:
        _section.delete()
    __all_sections = Book.objects.all()
    for _section in __all_sections:
        _section.delete()
    return redirect('home')


# def logout_page(request):
#     if request.method == 'POST':
#         logout(request)
#         return redirect('home')
#     context = {}
#     return render(request, 'base/logout.html', context)


# def book_create(request):
#     if request.method == 'POST':
#         _form = request.POST.dict()
#         _id = BookUtil()._set_attr(_form)
#         return redirect('book-edit', pk=_id)
#     _topics = Topic.objects.all()
#     _tags = Tag.objects.all()
#     context = {'tags': _tags, 'topics': _topics}
#     return render(request, 'base/book-create.html', context)


# def book_view(request, pk):
#     _book = Book.objects.get(id=pk)
#     _articles = _book.article_set.all()
#     print(f"count: {_articles.count()}")
#     _article_count = _articles.count()
#     _sections = Section.objects.all()
#     context = {'article_count': _article_count, 'book': _book, 'sections': _sections,
#                'articles': _articles, 'edit': False}
#     return render(request, 'base/articles.html', context)


# def book_edit(request, pk):
#     _book = Book.objects.get(id=pk)
#     _articles = _book.article_set.all()
#     _sections = Section.objects.all()
#     if request.method == 'POST':
#         submit_method = request.POST.get('submit_method')
#         if submit_method == 'Add':
#             _new_article = Article.objects.create(
#                 title=request.POST.get('article-title'),
#                 book=_book
#             )
#             _form_out_test = FormTesterModel.objects.create()
#             _form_out_test.body = f"{request.POST}\n{request.POST.get('form2')}\n{request}"
#             _form_out_test.save()
#             _new_article.save()
#             return redirect('section-create', pk=_new_article.id)

#         BookUtil().book_save(_book, request.POST.dict())
#         BookUtil().remove_duplicates()

#     _article_count = _articles.count()
#     context = {'article_count': _article_count, 'book': _book, 'articles': _articles,
#                'sections': _sections, 'edit': True}
#     return render(request, 'base/book-edit.html', context)


# def section_create(request, pk):
#     _article = Article.objects.get(id=pk)

#     if request.method == 'POST':
#         Section.objects.create(
#             article=_article,
#             title=request.POST.get('section-title'),
#             body=request.POST.get('section-body')
#         ).save()
#         return redirect('book-edit', pk=_article.book.id)

#     context = {'article': _article}
#     return render(request, 'base/section-create.html', context)


# # def section_edit(request, pk):


# def write_book(request):
#     context = {}
#     return render(request, 'base/content-write.html')
