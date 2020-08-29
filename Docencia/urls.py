from django.urls import path
from . import views

__author__ = "Josue Isai Hernandez Sanchez"
__email__ = "josueisaihs@gmail.com"

urlpatterns = [
    path('', views.index, name='index'),
    path('api/suscribir', views.suscribeteAjax, name='api_index_suscribete'),
    path("eventos/", views.eventos, name="eventos"),
    path("evento/<int:pk>/", views.evento, name="evento"),
    path("cursos/", views.cursos, name="cursos"),
    path("curso/<int:pk>/", views.curso, name="curso"),
    path("noticias/", views.noticias, name="noticias"),
    path("noticia/<int:pk>/", views.noticia, name="noticia"),
    path("api/previewlink/", views.previewLink, name="api_index_previewlink"),
    path("recursos/", views.recursos, name="recursos"),

    path("clase/", views.clase, name="clase"),

    path('admision/dashboard/', views.dashboard, name='admision_dashboard'),
    path('admision/registro/', views.registro, name='admision_registro'),
    path('admision/success/', views.registrocompletado, name='admision_registro_ok'),
    path('admision/seleccioncurso/', views.selectcourse, name='admision_seleccion_curso'),
    path('admision/seleccioncurso/<int:coursePk>/application/', views.application, name='admision_applicacion'),
    path('api/admision/application/add/', views.applicationAjax, name='api_admision_aplicacion'),
    path('api/admision/application/cancel/', views.applicationCancelAjax, name='api_admision_aplicacion_cancel'),

    path('admision/admin/dashboard/', views.admindashboard, name='admision_admin'),
    path('admision/admin/dashboard/<int:coursepk>/', views.admindashboard_course, name='admision_admin_course'),
    path('api/admision/admin/dashboard/denegar/', views.admindashboard_denegar, name='api_admision_denegar'),
    path('api/admision/admin/dashboard/accion/', views.admindashboard_accion, name='api_admision_accion'),
    path('admision/admin/dashboard/detail/<int:coursepk>/', views.admindashboard_detail, name='admision_admin_detail'),
    path('admision/admin/dashboard/detail/student/<int:apppk>/', views.admindashboard_student_detail, name='admision_admin_student_detail'),
]