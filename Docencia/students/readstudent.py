__author__ = "Josue Isai Hernandez Sanchez"
__email__ = "josueisaihs@gmail.com"

import os

from Docencia.DatosPersonales.models import User, StudentPersonalInformation
from Docencia.Admision.models import Application
from Docencia.Cursos.models import CourseInformation, Edition

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'students', 'Datos estudiantes DEH.csv'), 'r', encoding="ISO-8859-1") as file:
    for line in file.readlines():
        nombre, apellidos, genero, ci, direccion, muncipio, provincia, movil, telefono, email, nacionalidad, ocupacion, grado, titulo = line.split(";")
        
        student = StudentPersonalInformation()
        student.name = nombre
        student.lastname = apellidos
        student.genero = ""
        student.numberidentification = ci
        student.street = direccion
        student.city = muncipio
        student.state = provincia
        student.phone = telefono
        student.cellphone = movil
        student.email = email
        student.nacionality = nacionalidad
        student.title = titulo
        student.save()

        app = Application()
        app.course = CourseInformation.objects.get(name="Desarrollo Web")
        app.student = student
        app.status = "aceptado"
        app.edition = Edition.objects.get(active=True)

        app.save()

    file.close()