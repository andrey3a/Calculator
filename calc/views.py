from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from calc.rpn import Calculator

# Create your views here.

def index(request):
    if 'digitsDisplay' in request.POST:
        if request.POST['digitsDisplay']:
            calc = Calculator(request.POST['digitsDisplay'])
            calc.calculateResult()
            if calc.getError():
                return render(request, 'index.html', { 'error_message' : calc.getError() })
            return render(request, 'index.html', { 'result_value' : calc.getResult() })
    return render(request, "index.html")
