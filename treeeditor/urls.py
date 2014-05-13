from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
import trees.urls
import trees.views


urlpatterns = patterns('',
    url(r'^$', 'trees.views.index'),
    url(r'^example/', 'trees.views.example'),
    url(r'^trees/', include(trees.urls)),
    url(r'^sign_up/', 'trees.views.new_user'),
    url(r'^my_trees/', 'trees.views.user_trees'),
    url(r'^save_tree/(?P<tree_id>\d+)/', 'trees.views.save_tree'),
    url(r'^delete_tree/(?P<tree_id>\d+)/', 'trees.views.delete_tree'),
    url(r'^tree/(?P<tree_url>.*)/', 'trees.views.edit_tree'),
    url(r'^new/', 'trees.views.new_tree'),
    url(r'^login/', 'trees.views.login_user', name='login'),
    url(r'^logout/', 'trees.views.logout_user', name='logout'),

    )+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
