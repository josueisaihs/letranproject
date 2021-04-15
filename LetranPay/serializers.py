from rest_framework import serializers
from Docencia.Plataforma.models import EnrollmentPay

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentPay
        fields = ['app', 'cardnumber', 'transfernumber', 'accept', 'monto', 'datepub']