from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def act(request):
    return render(request, 'act.html')

def about(request):
    return render(request, 'about.html')

def privacy(request):
    return render(request, 'privacy.html')






