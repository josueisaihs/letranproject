from django.shortcuts import render

# Create your views here.
def pagary(request):
    return render(request, 'pagarytest/index.html', locals())