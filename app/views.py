from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

# Імпортуємо модель Contact для роботи з базою даних
from .models import Contact

# Імпортуємо клас ContactsForm для роботи з формою
from .forms import ContactsForm


# Представлення для відображення списку контактів
def home(request):
    # Отримуємо всі контакти з бази даних
    contacts = Contact.objects.all()

    query = request.GET.get('q')
    if query:
        contacts = Contact.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(email__icontains=query)
        )

    # Передаємо контакти в шаблон
    return render(request, 'contact_list.html',
                  {'contacts': contacts, 'query': query})


# Функція для додавання нового контакту
def add_contact(request):
    # Перевіряємо, чи запит є POST-запитом (тобто форма була відправлена)
    if request.method == 'POST':
        # Створюємо форму та передаємо в неї дані з запиту
        form = ContactsForm(request.POST, request.FILES)
        # Перевіряємо, чи форма заповнена коректно
        if form.is_valid():
            # Зберігаємо новий контакт у базу даних
            form.save()
            # Перенаправляємо користувача на список контактів
            return redirect('home')
    # Якщо запит не POST (користувач просто відкрив сторінку)
    else:
        # Створюємо порожню форму
        form = ContactsForm()
        # Відображаємо сторінку з формою
        return render(request, 'add_contact.html', {'form': form})

def about_book(request):
    return render(request, 'about_book.html')

def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    # Перевіряємо, чи запит є POST-запитом (тобто форма була відправлена)
    if request.method == 'POST':
        # Створюємо форму та передаємо в неї дані з запиту
        form = ContactsForm(request.POST, request.FILES, instance=contact)
        # Перевіряємо, чи форма заповнена коректно
        if form.is_valid():
            # Зберігаємо новий контакт у базу даних
            form.save()
            # Перенаправляємо користувача на список контактів
            return redirect('home')
    # Якщо запит не POST (користувач просто відкрив сторінку)
    else:
        # Створюємо порожню форму
        form = ContactsForm(instance=contact)
        # Відображаємо сторінку з формою
        return render(request, 'add_contact.html', {'form': form})

def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    return redirect('home')

def search_contacts(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Contact.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(email__icontains=query)
        )
    return render(
        request,
        'contact_list.html',
        {'contacts': results, 'query': query}
    )