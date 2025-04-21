"""
URL configuration for FitFusion project.

"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns  # ✅ Import this for language translater

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # ✅ Add this line to enable language switching
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('gym.urls')), #entry of gym ap urls
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    

















'''# Language switching URL
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

# Your main URLs inside i18n_patterns
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('gym.urls')),  # entry of gym app urls
)

# Media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)'''