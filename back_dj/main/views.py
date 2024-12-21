from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
import json
from .models import Product, Cart, CartItem

# Главная страница
def index(request):
    return render(request, 'main/index.html')

# Магазин
def shop(request):
    return render(request, 'main/shop.html')

# Блог
def blog(request):
    return render(request, 'main/blog.html')

# Элементы
def elements(request):
    return render(request, 'main/elements.html')

# Регистрация
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'main/registration/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'main/registration/register.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return JsonResponse({"success": True, "message": "Registration successful!"})

    return render(request, 'main/registration/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')  # Перенаправление на главную страницу
        else:
            return render(request, 'main/registration/login.html', {'error': 'Invalid username or password'})
    return render(request, 'main/registration/login.html')


def product_list(request):
    products = Product.objects.all()
    data = [{"id": p.id, "name": p.name, "price": str(p.price), "image_url": p.image_url} for p in products]
    return JsonResponse(data, safe=False)

@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = [{"product_id": item.product.id, "name": item.product.name,
              "price": str(item.product.price), "quantity": item.quantity}
             for item in cart.items.all()]
    return JsonResponse(items, safe=False)

@csrf_exempt
@login_required
def add_to_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get("product_id")
        quantity = data.get("quantity", 1)
        product = get_object_or_404(Product, id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        cart_item.save()
        return JsonResponse({"success": True})

@login_required
def cart_page(request):
    return render(request, 'main/cart.html')
