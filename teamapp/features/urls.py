
from django.urls import path, include, re_path
from . import views


app_name = 'features'
urlpatterns = [
    path('create/', views.ArticleCreateView.as_view(), name='article-create'),
    path('', views.ArticleListView.as_view(), name='article-list'),
    path('<int:id>/', views.ArticleView.as_view(), name='article-detail'),
    path('<int:id>/update/', views.ArticleUpdateView.as_view(), name='article-update'),
    path('<int:id>/delete/', views.ArticleDeleteView.as_view(), name='article-delete'),

]




# urlpatterns = [
#
#     path('create/',views.ArticleCreateView.as_view(), name='article-create'),
#     path('',views.ArticleListView.as_view(), name='article-list'),
#     path('<int:id>/',views.ArticleDetailView.as_view(), name='article-detail'),
#     path('<int:id>/update/',views.ArticleUpdateView.as_view(), name='article-update')
#     path('<int:id>/delete/',views.ArticleDeleteView.as_view(), name='article-delete')
#     # path('home/', views.hello, name='home'),
#     # path('service/', views.service, name='service'),
#     # path('books/', views.BookListView.as_view(), name='books'),
#     # re_path(r'^book/(?P<pk>\d+)$',views.BookDetailView.as_view(), name='book-detail'),
#
# ]



