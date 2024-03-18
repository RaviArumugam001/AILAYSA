from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .views import createuser_profile,profileImageView,userprofileupdate,ProfileDelete
from django.urls import path
urlpatterns = [
    path("user_create",createuser_profile,name='user_create'),
    path("profile_view/<int:id>",profileImageView,name='profle_view'),
    path("profileupdate",userprofileupdate,name='profile_update'),
    path("profiledelete",ProfileDelete,name='profile_delete')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)