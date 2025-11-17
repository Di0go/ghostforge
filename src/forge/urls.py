# ghostforge/src/forge/urls.py
# 
# URL routing for the Forge app
# 
# <diogopinto> 2025+

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttackScenarioViewSet, DefenseAnalysisViewSet



# -----------------------------------------------------------------
# EN: Automatically generates URLs for the ViewSets (ex: /attacks/, /attacks/1/)
# The router handles automatially all the REST routes (GET, POST, PUT/PATCH, DELETE) because of the viewset.
router = DefaultRouter()
router.register(r'attacks', AttackScenarioViewSet)
router.register(r'defense', DefenseAnalysisViewSet)


# -----------------------------------------------------------------
# EN: URL Patterns
urlpatterns = [
    path('', include(router.urls)),
]