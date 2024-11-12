from django.shortcuts import render

# Create your views here.
def main(request, sala):
    
    return render(request, 'main.html')