from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'contact_list.html')

def add_contact(request):
    return render(request, 'add_contact.html')

def about_book(request):
    return render(request, 'about_book.html')