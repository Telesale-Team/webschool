from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import questions.views as home_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_views.home, name='home'),
    path('results/', home_views.public_results, name='public_results'),
    path('accounts/', include('accounts.urls')),
    path('exam/', include('exams.urls')),
    path('dashboard/', include('questions.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
