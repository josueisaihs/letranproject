import json

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views import View

from . import serializers
from Docencia.Admision.models import Application
from Docencia.tasks import enviar_notification

class Enrollments(View):
    def get(self, request, *args, **kwargs):
        enrollments = serializers.EnrollmentSerializer(serializers.EnrollmentPay.objects.all(), many=True)
        return JsonResponse(enrollments.data, safe=False)

@require_POST
@csrf_exempt
def checkEnrollmentPay(request):
    transfernumber = request.POST["transfernumber"]
    monto = request.POST["monto"]
    enrollments = serializers.EnrollmentPay.objects.filter(transfernumber=transfernumber, accept=False, monto=monto)
    if enrollments.__len__() > 0:
        enrollment = enrollments.first()

        app = Application.objects.get(pk=enrollment.app.pk)
        app.paid = True
        app.save()

        enrollment.accept = True
        enrollment.save()

        enviar_notification(
                subject="Verificado Pago",
                body="%s %s, el CFBC agradece su pago de las cuotas administrativas de matrícula en el curso gratuito de %s con la transacción %s y monto de %s CUP." % (app.student.name, app.student.lastname, app.course.name, enrollment.transfernumber, enrollment.monto),
                studentMail="%s"
        )

        # Mostrando resultado si es valido
        enrollments = serializers.EnrollmentSerializer(enrollment, many=True)

        return JsonResponse([{'status': True},], safe=False)
    else:
        return JsonResponse([{'status': False},], safe=False, status=404)