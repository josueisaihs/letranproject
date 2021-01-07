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

    # Plataforma
    path("plataforma/foro/<slug:slug>", views.plataforma.messages, name="plataforma_messages"),
    path("plataforma/admin/foro/<slug:slug>", views.plataforma.adminmessages, name="plataforma_adminmessages"),
    path("plataforma/foro/send/", views.plataforma.send_message, name="plataforma_send_message"),
    path("plataforma/foro/delete/", views.plataforma.delete_message, name="plataforma_delete_message"),
    path("plataforma/foro/update/", views.plataforma.update_messages, name="plataforma_update_messages"),
    path("plataforma/foro/user/",views.plataforma.user_message, name="plataforma_user_message"),
    # Plataforma Estudiantes
    path("plataforma/dashboard/", views.plataforma.dashboard, name="plataforma_dashboard"),
    path("plataforma/dashboard/curso/<slug:slug>", views.plataforma.curso, name="plataforma_curso"),
    path("plataforma/dashboard/subject/<slug:slug>", views.plataforma.subject, name="plataforma_subject"),
    path("plataforma/dashboard/clase/<slug:slug>", views.plataforma.clase, name="plataforma_clase"),
    path("plataforma/dashboard/recursos/<slug:slug>", views.plataforma.recursos, name="plataforma_recursos"),
    path("plataforma/dashboard/clase/recurso/<slug:slug>", views.plataforma.downloadResource, name="plataforma_recurso"),
    #Plataforma Profesores
    path("plataforma/admin/dashboard/", views.plataforma.admindashboard, name="plataforma_admin_index"),
    path("plataforma/admin/dashboard/<slug:slug>/clase/crear/", views.plataforma.adminclass, name="plataforma_admin_clase"),
    path("plataforma/admin/dashboard/clase/delete/", views.plataforma.deleteclass, name="plataforma_admin_clase_delete"),
    path("plataforma/admin/dashboard/<slug:slug>/clase/<slug:slugclass>/editar/", views.plataforma.adminclass_edit, name="plataforma_admin_clase_editar"),
    path("plataforma/admin/dashboard/clase/file/upload/", views.plataforma.uploadfile, name="plataforma_admin_upload"),
    path("plataforma/admin/dashboard/clase/file/delete/", views.plataforma.deletefile, name="plataforma_admin_delete"),
    path("plataforma/admin/dashboard/comunicado/", views.plataforma.sendmasivemail, name="plataforma_admin_comunicado"),
    path("plataforma/admin/dashboard/clase/recurso/<slug:slug>", views.plataforma.downloadTeacherResource, name="plataforma_admin_recurso"),

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
    path('api/admision/admin/dashboard/comment/', views.admon.updateComment, name='api_admision_comment'),
    path('admision/admin/dashboard/detail/<int:coursepk>/', views.admon.admindashboard_detail, name='admision_admin_detail'),
    path('admision/admin/dashboard/detail/student/<int:apppk>/', views.admon.admindashboard_student_detail, name='admision_admin_student_detail'),
]