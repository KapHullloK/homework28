"""
URL configuration for hw28_settings project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from ads.views import tools_views, category_views, ad_views, user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tools_views.StatusView.as_view()),
    path('ddD/', tools_views.DownloadDataView.as_view()),

    #######################################################

    path('cat/', category_views.CategoryGetView.as_view()),
    path('cat/create/', category_views.CategoryPostView.as_view()),
    path('cat/<int:pk>/update/', category_views.CategoryDeleteView.as_view()),
    path('cat/<int:pk>/delete/', category_views.CategoryUpdateView.as_view()),

    #######################################################

    path('ad/', ad_views.AdGetView.as_view()),
    path('ad/<int:pk>/', ad_views.AdDetailView.as_view()),
    path('ad/create/', ad_views.AdPostView.as_view()),
    path('ad/<int:pk>/delete/', ad_views.AdDeleteView.as_view()),
    path('ad/<int:pk>/update/', ad_views.AdUpdateView.as_view()),
    path('ad/<int:pk>/upload_imag/', ad_views.UploadImagesView.as_view()),

    #######################################################

    path('user/', user_views.UserGetView.as_view()),
    path('user/<int:pk>/', user_views.UserDetailView.as_view()),
    path('user/<int:pk>/delete/', user_views.UserDeleteView.as_view()),
    path('user/create/', user_views.UserPostView.as_view()),
    path('user/<int:pk>/update/', user_views.UserUpdateView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
