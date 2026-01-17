from django.shortcuts import render, redirect

# Імпортуємо модель Contact для роботи з базою даних
from .models import Contact

# Імпортуємо клас ContactsForm для роботи з формою
from .forms import ContactsForm


# Представлення для відображення списку контактів
def home(request):
    # Отримуємо всі контакти з бази даних
    contacts = Contact.objects.all()
    # Передаємо контакти в шаблон
    return render(request, 'contact_list.html', {'contacts': contacts})


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