from django.urls import path
from . import views


__author__ = "Josue Isai Hernandez Sanchez"
__email__ = "josueisaihs@gmail.com"


urlpatterns = [
    path("", views.index, name="sapereaude_index"),
    path("<slug:edition>/", views.index, name="sapereaude_index"),
    path("<slug:edition>/article/<slug:article>", views.article, name="article"),
    path("<slug:edition>/section/<slug:section>", views.section, name="section"),
    path("api/editions/", views.Edition.as_view(), name="editions"),
    path("api/<slug:edition>/sections/", views.Section.as_view(), name="sections"),
    path("api/<slug:edition>/articles/", views.ArticleRandom.as_view(), name="articles"),
    path("api/authors/", views.Author.as_view(), name="authors"),
]