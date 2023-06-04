from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Article
from .models import Message
from django.http import JsonResponse
from firebase_admin import auth




def send_sms(request):
    phone_number = request.POST.get('phone_number')
    if not phone_number:
        return JsonResponse({'error': 'Phone number is required.'}, status=400)

    try:
        # Send the verification code to the user's phone
        verification = auth.create_phone_verification(phone_number)
        return JsonResponse({'success': 'Verification code sent successfully.'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)



def verify_code(request):
    phone_number = request.POST.get('phone_number')
    verification_code = request.POST.get('verification_code')
    if not phone_number or not verification_code:
        return JsonResponse({'error': 'Phone number and verification code are required.'}, status=400)

    try:
        # Verify the user's phone number with the verification code
        verification = auth.verify_phone_number(phone_number, verification_code)
        # Create a Firebase user with the verified phone number
        user = auth.create_user(phone_number=phone_number)
        return JsonResponse({'success': 'Phone number verified and user created successfully.'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def regist(request):

    # Массив для передачи данных шаблону
    data = {}
    # Проверка что есть запрос POST
    if request.method == 'POST':
        # Создаём форму
        form = UserCreationForm(request.POST)
        # Валидация данных из формы
        if form.is_valid():
            # Получение данных из формы
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            confirm_password = form.cleaned_data['password2']

            # Создание объекта User и сохранение его в базе данных
            user = User.objects.create(username=username, password=password, confirm_password=confirm_password)

            data['username'] = username
            # Передача формы к рендеру
            data['form'] = form
            # Передача надписи, если прошло всё успешно
            data['res'] = "Всё прошло успешно"
            next_url = request.POST.get('next', '/')
            return redirect(next_url)
            # Рендеринг страницы

    else:  # Иначе
        # Создаём форму
        form = UserCreationForm()
        # Передаём форму для рендеринга
        data['form'] = form
        # Рендеринг страницы
        return render(request, 'main/registr.html', data)


def index(request):
    return render(request, 'main/index.html')


def page(request):
    last_user = User.objects.last()  # Получаем последнего пользователя из базы данных
    users = [last_user]  # Создаем список, содержащий только последнего пользователя
    context = {'users': users}  # Создаем контекст шаблона, содержащий пользователей
    return render(request, 'main/main_page.html', context)


def check(request):
    last_user = User.objects.last()  # Получаем последнего пользователя из базы данных
    users = [last_user]  # Создаем список, содержащий только последнего пользователя
    context = {'users': users}  # Создаем контекст шаблона, содержащий пользователей
    return render(request, 'main/check.html', context)


def advertisement(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        intro = request.POST.get('intro')
        text = request.POST.get('text')
        article = Article(title=title, intro=intro, text=text)
        article.save()

    else:
        ads = Article.objects.all()
        return render(request, 'main/advertisement.html', {'ads': ads})


def posts(request):
    articles = Article.objects.all().order_by('text')
    return render(request, 'main/posts.html', {'articles': articles})


def chat1(request):
    if request.method == 'POST':
        sender_user = request.user
        receiver = request.POST.get('receiver').strip()
        message_text = request.POST.get('message')
        message = Message(sender=sender_user, receiver=receiver, message=message_text)
        message.save()
        return redirect('/')
    else:
        return render(request, 'main/chat1.html', {})


def chat2(request):
    return render(request, 'main/chat2.html')


def payment_view(request):
    return render(request, 'main/payment.html')



def payment_successful(request):
    return render(request, 'main/payment2.html')


