from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
import questions.views as home_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_views.home, name='home'),
    path('results/', home_views.public_results, name='public_results'),
    path('accounts/', include('accounts.urls')),
    path('exam/', include('exams.urls')),
    path('dashboard/', include('questions.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
