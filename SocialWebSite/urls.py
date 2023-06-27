from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from SocialWebSite import settings
from scripts import *

urlpatterns = [
                  path('', include('Network.urls')),
                  path('admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

script()
