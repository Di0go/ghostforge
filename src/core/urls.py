# ghostforge/src/core/urls.py
# 
# Main URL configuration for the ghostforge project
# 
# <diogopinto> 2025+

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # -----------------------------------------------------------------
    # EN: API Routes (Attack, Defense)
    path('api/', include('forge.urls')),
]