from django.urls import path

from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'), # Home
    path('recipes/category/<int:category_id>/', views.category, name='category'), # Recipe
    path('recipes/<int:id>/', views.recipe, name='recipe'), # Recipe
    path('recipes/search/', lambda request: ... , name='search'),
]
