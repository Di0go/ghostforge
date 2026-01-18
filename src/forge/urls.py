# ghostforge/src/forge/urls.py
# 
# URL routing for the Forge app (API + Frontend)
# 
# <diogopinto> 2025+

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttackScenarioViewSet, DefenseAnalysisViewSet, home, attack_view, defense_view

# EN: API Router
router = DefaultRouter()
router.register(r'attacks', AttackScenarioViewSet)
router.register(r'defense', DefenseAnalysisViewSet)

urlpatterns = [
    # EN: Frontend Routes
    path('', home, name='home'),
    path('attack/', attack_view, name='attack'),
    path('defense/', defense_view, name='defense'),

    # EN: API Routes
    path('api/', include(router.urls)),
]