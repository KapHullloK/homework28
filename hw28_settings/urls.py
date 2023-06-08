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

    path('catg/', category_views.CategoryGetView.as_view()),
    path('catp/', category_views.CategoryPostView.as_view()),
    path('catd/<int:pk>/', category_views.CategoryDeleteView.as_view()),
    path('catpa/<int:pk>/', category_views.CategoryUpdateView.as_view()),

    #######################################################

    path('adg/', ad_views.AdGetView.as_view()),
    path('adgd/<int:pk>/', ad_views.AdDetailView.as_view()),
    path('adp/', ad_views.AdPostView.as_view()),
    path('add/<int:pk>/', ad_views.AdDeleteView.as_view()),
    path('adpa/<int:pk>/', ad_views.AdUpdateView.as_view()),
    path('ad/<int:pk>/upload_imag/', ad_views.UploadImagesView.as_view()),

    #######################################################

    path('usg/', user_views.UserGetView.as_view()),
    path('usgd/<int:pk>/', user_views.UserDetailView.as_view()),
    path('usd/<int:pk>/', user_views.UserDeleteView.as_view()),
    path('usp/', user_views.UserPostView.as_view()),
    path('uspa/<int:pk>/', user_views.UserUpdateView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
