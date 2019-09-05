from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create),
    url(r'^validate$', views.validate),
    url(r'^books$', views.books),
    url(r'^add_book$', views.add_book),
    url(r'^edit_book/(?P<id>\d+)$', views.edit_book),
    url(r'^update_book$', views.update_book), #<-------- USES HIIDDEN INPUT INSTEAD OF URL ID
    url(r'^delete_book/(?P<id>\d+)$', views.delete_book),
    url(r'^favorite/(?P<id>\d+)$', views.favorite),
    url(r'^unfavorite/(?P<id>\d+)$', views.unfavorite),
    url(r'^favorite_page/(?P<id>\d+)$', views.favorite_page),
    url(r'^unfavorite_page/(?P<id>\d+)$', views.unfavorite_page),
]
