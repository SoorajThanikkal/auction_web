from django.shortcuts import render

# Create your views here.


def Role(request):
    return render(request, 'role.html')
