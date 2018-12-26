from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView,DeleteView
from .models import Book, Article
from .forms import ArticleModelForm

from django.http import HttpResponseRedirect

from django.views import View


class ArticleObjectMixin(object):
    model = Article
    lookup = 'id'

    def get_object(self):
        id = self.kwargs.get(self.lookup)
        obj = None
        if id is not None:
            obj = get_object_or_404(Article,id=id)
        return obj


class ArticleDeleteView(ArticleObjectMixin, View):
    template_name = 'features/article_delete.html'

    def get(self, request, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = ArticleModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            obj.delete()
            context['object'] = None
            return redirect('/features/')
        return render(request, self.template_name, context)


class ArticleUpdateView(ArticleObjectMixin, View):
    template_name = 'features/article_update.html'

    # def get_object(self):
    #     self.id = self.kwargs.get('id')
    #     obj = None
    #     if id is not None:
    #         obj = get_object_or_404(Article, id=self.id)
    #     return obj

    def get(self, request, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = ArticleModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = ArticleModelForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
            context['form'] = form
            context['object'] = obj
        #return HttpResponseRedirect('/{}'.format(self.id))
        return render(request, self.template_name, context)

class ArticleCreateView(View):
    template_name = 'features/article_create.html'

    def get(self, request, *args, **kwargs):
        context = {}
        form = ArticleModelForm()
        context = {'form': form}
        return render(request, self.template_name, context )

    def post(self, request, *args, **kwargs):
        form = ArticleModelForm(request.POST)
        if form.is_valid():
            form.save()
        context = {'form': form}
        return render(request, self.template_name, context)


class ArticleView(ArticleObjectMixin, View):
    template_name = 'features/article_detail.html'

    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_object()}
        # if id is not None:
        #     obj = get_object_or_404(Article, id=id)
        #     context['object'] = obj
        return render(request, self.template_name, context )



class ArticleListView(View):

    template_name = 'features/article_list.html'
    queryset = Article.objects.all()

    def get_queryset(self):
        return self.queryset


    def get(self, request, *args, **kwargs):
        context = {'object_list': self.queryset}
        return render(request, self.template_name,context)






"""


class ArticleCreateView(CreateView):
    template_name = 'features/article_create.html'
    form_class = ArticleModelForm
    queryset = Article.objects.all()
    #success_url = '/'

    def form_valid(self, form):
        print (form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return '/'



class ArticleUpdateView(UpdateView):
    template_name = 'features/article_delete.html'
    form_class = ArticleModelForm

    def get_object(self):
        print ("kwargs are :", self.kwargs)
        id_ = self.kwargs.get("id")
        return get_object_or_404(Article, id=id_)


    def form_valid(self, form):
        print (form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return '/'



class ArticleDeleteView(DeleteView):
    template_name = 'features/article_delete.html'

    def get_object(self):
        print ("kwargs are :", self.kwargs)
        id_ = self.kwargs.get("id")
        return get_object_or_404(Article, id=id_)

    def get_success_url(self):
        return reverse('features:article-list')






class ArticleListView(ListView):
    context_object_name = 'myarticles'
    queryset = Article.objects.all()



class ArticleDetailView(DetailView):
    queryset = Article.objects.all()

    def get_object(self):
        print ("kwargs are :", self.kwargs)
        id_ = self.kwargs.get("id")
        return get_object_or_404(Article, id=id_)





















def hello(request):
    return render(request, 'features/index.html')

def service(request):
    return render(request, 'features/services.html')

class  BookListView(ListView):
    model = Book
    context_object_name = 'my_book_list'
    queryset = Book.objects.all()
    print ("queryset..", queryset)
    template_name = 'features/book_list.html'

# class BookDetailView(DetailView):
#     model = Book


class BookDetailView(DetailView):
    model = Book






"""





