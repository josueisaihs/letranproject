from django.core.exceptions import ValidationError

def valid_extension(value):
    if (not value.name.endswith('.pdf')):
        raise ValidationError("Solo se permiten archivos PDF")

def valid_size(object):
    filesize = object.file.size
    MBLimit = 10.0
    if filesize > MBLimit * 1024 * 1024:
            raise ValidationError("Solo se permiten archivos hasta 10MB")