
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseNotFound
from app_store.models import DATABASE
from django.contrib.auth import get_user, authenticate, login
from app_wishlist.logic.control_wishlist import view_in_wishlist, add_to_wishlist, remove_from_wishlist
from django.contrib.auth.decorators import login_required
from app_store.logic.control_cart import view_in_cart


# Create your views here.
# def wishlist_view(request):
#     if request.method == "GET":
#         return render(request, "app_wishlist/wishlist.html")

@login_required
def wishlist_view(request):
    if request.method == "GET":
        username = get_user(request).username
        wishlist = view_in_wishlist(username)
        data = wishlist[username]["products"]  # TODO получить продукты из избранного для пользователя, используя view_in_wishlist

        products = []
        # TODO сформировать список словарей продуктов с их характеристиками. Пройдитесь по id продуктам в data
        #  получите словари с характеристиками продуктов по их id и запишите в список products
        for product_id in data:
            if product_id in DATABASE:
                product = DATABASE[product_id].copy()
                product["id"] = product_id
                products.append(product)

        return render(request, 'app_wishlist/wishlist.html', context={"products": products})

def login_view(request):
    if request.method == "GET":
        return render(request, "login/login.html")

    if request.method == "POST":
        data = request.POST  # Получаем данный из post запроса
        user = authenticate(username=data["username"], password=data["password"])  # Понимаем, что за пользователь перед нами
        if user:  # Если пользователь есть в базе
            login(request, user)  # Авторизируем пользователя
            view_in_cart(user.username)  # Получаем корзину пользователя, если её нет, то создаем её
            view_in_wishlist(user.username)  # TODO добавить пользователя в базу избранное view_in_wishlist(user.username)
            return redirect("/")  # Перенаправляем пользователя на стартовую страницу
        # Иначе заново показываем форму авторизации
        return render(request, "login/login.html", context={"error": "Неверные данные"})