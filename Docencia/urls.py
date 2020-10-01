from django.urls import path
from . import views

__author__ = "Josue Isai Hernandez Sanchez"
__email__ = "josueisaihs@gmail.com"

urlpatterns = [
    path('', views.index.index, name='index'),
    path('api/suscribir', views.index.suscribeteAjax, name='api_index_suscribete'),
    path("eventos/", views.index.eventos, name="eventos"),
    path("evento/<int:pk>/", views.index.evento, name="evento"),
    path("cursos/", views.index.cursos, name="cursos"),
    path("curso/<slug:slug>/", views.index.curso, name="curso"),
    path("noticias/", views.index.noticias, name="noticias"),
    path("noticia/<slug:slug>/", views.index.noticia, name="noticia"),
    path("comunicado/<slug:slug>/", views.index.release, name="comunicado"),
    path("api/previewlink/", views.index.previewLink, name="api_index_previewlink"),
    path("recursos/", views.index.recursos, name="recursos"),
    path("politicaprivacidad/", views.politicaprivacidad, name="politicaprivacidad"),

    # Plataforma Estudiantes
    path("plataforma/dashboard/", views.plataforma.dashboard, name="plataforma_dashboard"),
    path("plataforma/dashboard/clase/<slug:slug>/", views.plataforma.clase, name="plataforma_clase"),
    path("plataforma/dashboard/clase/recurso/<slug:slug>", views.plataforma.downloadResource, name="plataforma_recurso"),

    #Plataforma Profesores
    path("plataforma/admin/dashboard/", views.plataforma.admindashboard, name="plataforma_admin_index"),
    path("plataforma/admin/dashboard/<slug:slug>/clase/crear/", views.plataforma.adminclass, name="plataforma_admin_clase"),
    path("plataforma/admin/dashboard/<slug:slug>/clase/<slug:slugclass>/editar/", views.plataforma.adminclass_edit, name="plataforma_admin_clase_editar"),
    path("plataforma/admin/dashboard/clase/file/upload/", views.plataforma.uploadfile, name="plataforma_admin_upload"),
    path("plataforma/admin/dashboard/clase/file/delete/", views.plataforma.deletefile, name="plataforma_admin_delete"),

    path('admision/dashboard/', views.datospersonales.dashboard, name='admision_dashboard'),
    path('admision/registro/', views.datospersonales.registro, name='admision_registro'),
    path('admision/success/', views.datospersonales.registrocompletado, name='admision_registro_ok'),
    path('admision/seleccioncurso/', views.admision.selectcourse, name='admision_seleccion_curso'),
    path('admision/seleccioncurso/<int:coursePk>/application/', views.admision.application, name='admision_applicacion'),
    path('api/admision/application/add/', views.admision.applicationAjax, name='api_admision_aplicacion'),
    path('api/admision/application/cancel/', views.admision.applicationCancelAjax, name='api_admision_aplicacion_cancel'),

    path('admision/admin/dashboard/', views.admon.admindashboard, name='admision_admin'),
    path('admision/admin/dashboard/<int:coursepk>/', views.admon.admindashboard_course, name='admision_admin_course'),
    path('api/admision/admin/dashboard/denegar/', views.admon.admindashboard_denegar, name='api_admision_denegar'),
    path('api/admision/admin/dashboard/accion/', views.admon.admindashboard_accion, name='api_admision_accion'),
    path('admision/admin/dashboard/detail/<int:coursepk>/', views.admon.admindashboard_detail, name='admision_admin_detail'),
    path('admision/admin/dashboard/detail/student/<int:apppk>/', views.admon.admindashboard_student_detail, name='admision_admin_student_detail'),
]