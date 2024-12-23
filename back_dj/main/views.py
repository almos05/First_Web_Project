from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
import json
from .models import Product, Cart, CartItem

# Главная страница
def index(request):
    return render(request, 'main/index.html')

# Магазин
def shop(request):
    products = Product.objects.all()
    return render(request, 'main/shop.html', {'products': products})

# Блог
def blog(request):
    return render(request, 'main/blog.html')

# Элементы
def elements(request):
    return render(request, 'main/elements.html')


def register(request):
    if request.user.is_authenticated:
        return render(request, 'main/registration/register.html', {"user_authenticated": True, "user": request.user})

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

    return render(request, 'main/registration/register.html', {"user_authenticated": False})


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

from django.shortcuts import redirect

@login_required
def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))
        product = get_object_or_404(Product, id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        cart_item.save()

        messages.success(request, f"{product.name} добавлен в корзину!")
        return redirect("shop")
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@login_required
def remove_from_cart(request, item_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item = CartItem.objects.get(id=item_id, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.success(request, f"One item removed from {cart_item.product.name} in your cart.")
    else:
        cart_item.delete()
        messages.success(request, f"{cart_item.product.name} has been removed from your cart.")

    return redirect("cart_page")


@login_required
def cart_page(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    context = {
        "cart_items": cart_items,
    }
    return render(request, "main/cart.html", context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def test_login(request):
    if request.user.is_authenticated:
        return HttpResponse(f"Logged in as {request.user.username}")
    else:
        return HttpResponse("Not logged in")