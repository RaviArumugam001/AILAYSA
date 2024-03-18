from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .views import CategoryListView,getAlldataPost,Posttitlenone,PostRecentComments,Postcreatedate,readthefiledata_count,Totalnocomments,stream_sentence
from django.urls import path
urlpatterns = [
    path("catnested",CategoryListView.as_view(),name='catsubcatlistdata'),
    path("postdata",getAlldataPost.as_view(),name='postdata'),
    path("postdatatitle",Posttitlenone.as_view(),name='postdatatitle'),
    path("postrecentcmt",PostRecentComments.as_view(),name='postrecentcmt'),
    path("postcreatedate",Postcreatedate.as_view(),name='postcreatedate'),
    path("posttotalcmt",Totalnocomments.as_view(),name='posttotalcmt'),
    path('stream-sentence', stream_sentence, name='stream_sentence'),
    path('filedata', readthefiledata_count, name='filedata'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)