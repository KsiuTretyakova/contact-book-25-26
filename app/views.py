from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

# Імпортуємо модель Contact для роботи з базою даних
from .models import Contact

# Імпортуємо клас ContactsForm для роботи з формою
from .forms import ContactsForm


# Представлення для відображення списку контактів
def home(request):

    # Головна сторінка додатку - відображає список усіх контактів
    # Підтримує пошук за ім'ям, прізвищем, номером телефону та email

    # Отримуємо всі контакти з бази даних
    # contacts = Contact.objects.all()

    # Отримуємо параметр пошуку 'q' з GET-запиту.
    # Якщо параметр відсутній - повертаємо порожній рядок як значення за замовчуванням,
    # щоб уникнути помилки KeyError та не ламати логіку нижче
    query = request.GET.get('q', '')
    if query:
        # Якщо користувач ввів пошуковий запит - фільтруємо контакти
        # Q-об'єкти дозволяють комбінувати умови через логічне АБО (|),
        # тобто контакт потрапить у результат, якщо збіг знайдено хоча б в одному полі
        # icontains - регістронезалежний пошук підрядка (case-insensitive contains)
        contacts = Contact.objects.filter(
            Q(first_name__icontains=query) |        # Пошук по імені
            Q(last_name__icontains=query) |         # Пошук по прізвищу
            Q(phone_number__icontains=query) |      # Пошук по номеру телефону
            Q(email__icontains=query)               # Пошук по email-адресі
        )
    else:
        # Якщо рядок пошуку порожній - повертаємо всі контакти з бази даних
        # all() повертає QuerySet з усіма записами моделі Contact
        contacts = Contact.objects.all()

    # Передаємо контакти в шаблон
    # - contacts: відфільтрований або повний список контактів для відображення
    # - query: поточний пошуковий запит, щоб шаблон міг показати його у полі пошуку
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