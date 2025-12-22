import random
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from app_store.models import DATABASE
from app_store.logic.services import filtering_category
from app_store.logic.control_cart import view_in_cart, add_to_cart, remove_from_cart


# def product_view_json(request):
#     if request.method == "GET":
#         return  JsonResponse(DATABASE,
#                              json_dumps_params={
#                                  'ensure_ascii':False,
#                                  'indent': 4
#                              })# TODO Вернуть JsonResponse с объектом DATABASE и параметрами отступов и кодировок,
#         # как в приложении app_weather

# def shop_view(request):
#     if request.method == 'GET':
#     #     with open('app_store/shop.html', 'r', encoding='utf-8')as f:
#     #         data = f.read()
#     #     return HttpResponse(data)
#         return render(request, 'app_store/shop.html', context={'products': DATABASE.values()})

def shop_view(request):
    if request.method == "GET":
        # Обработка фильтрации из параметров запроса
        category_key = request.GET.get("category")
        if ordering_key := request.GET.get("ordering"):
            if request.GET.get("reverse").lower() == 'true':
                data = filtering_category(DATABASE, category_key, ordering_key, True)
            else:
                data = filtering_category(DATABASE, category_key, ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)
        return render(request, 'app_store/shop.html',
                      context={"products": data, 'category': category_key })


def product_view_json(request):
    if request.method == "GET":
        id_ = request.GET.get('id')
        if id_:
            if id_ in DATABASE:
                return JsonResponse(DATABASE.get(id_), json_dumps_params={'ensure_ascii':False,
                                                                     'indent':4})
            else:
                return HttpResponseNotFound('Данного продукта нет в базе данных!')
            # TODO Если id_ было передано (существует)
            # TODO Если этот id_ есть в базе (DATABASE), то вернуть JsonResponse товара (словаря с характеристиками товара)
            # TODO Иначе вернуть HttpResponseNotFound("Данного продукта нет в базе данных")

        category_key = request.GET.get('category')
        ordering_key = request.GET.get('ordering')
        if ordering_key:
            reverse = request.GET.get('reverse')
            if reverse and reverse.lower() == 'true':
                data = filtering_category(DATABASE, category_key, ordering_key, reverse = True)
            else:
                data = filtering_category(DATABASE, category_key, ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)

        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False,
                                                         'indent': 4})
def product_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for data in DATABASE.values():
                if data['html'] == page:  # Если значение переданного параметра совпадает именем html файла
                    data_other_products = [prod for prod in DATABASE.values() if
                                           prod['category'] == data['category'] and prod['name'] != data['name']]  # TODO Переделать по заданию
                    if len(data_other_products) > 5:
                        data_other_products = random.sample(data_other_products, k=5)
                    return render(request, 'app_store/product.html', context={'product': data,
                                                                              'other_products': data_other_products})

        elif isinstance(page, int):
            data = DATABASE.get(str(page))  # Получаем какой странице соответствует данный id
            if data:  # Если по данному page было найдено значение
                data_other_products = [prod for prod in DATABASE.values() if
                                       prod['category'] == data['category'] and prod['name'] != data[
                                           'name']]  # TODO Переделать по заданию
                if len(data_other_products) > 5:
                    data_other_products = random.sample(data_other_products, k=5)
                return render(request, 'app_store/product.html', context={'product': data,
                                                                          'other_products':
                                                                              data_other_products})

        return HttpResponse(status=404)

# def product_page_view(request, page):
#     if request.method == "GET":
#         if isinstance(page, str):  # Проверяем, что в параметр page передали значение строкового типа
#             for data in DATABASE.values():  # Перебираем все товары (словари) в DATABASE
#                 if data['html'] == page:  # Если значение переданного параметра совпадает именем html файла, получаемого по ключу
#                     with open(f'app_store/product/{page}.html', encoding="utf-8") as f:
#                         s = f.read()
#                         return HttpResponse(s)
#
#                     # TODO 1. Откройте файл open(f'app_store/product/{page}.html', encoding="utf-8") (Не забываем про контекстный менеджер with)
#                     # TODO 2. Прочитайте его содержимое
#                     # TODO 3. Верните HttpResponse c содержимым html файла
#
#             # Если за всё время поиска не было совпадений, то значит по данному имени нет соответствующей
#             # страницы товара и можно вернуть ответ с ошибкой HttpResponse(status=404)
#             return HttpResponse(status=404)
#
#         elif isinstance(page, int):
#             data = DATABASE.get(str(page))
#             if data:
#                 with open(f'app_store/product/{data["html"]}.html',
#                           encoding='utf-8') as f:
#                     return HttpResponse(f.read())
#             return HttpResponse(status=404)





def cart_view_json(request):
    if request.method == "GET":
        username = ''
        data = view_in_cart(username) # TODO Вызвать ответственную за это действие функцию view_in_cart(username)
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})


def cart_add_view_json(request, id_product):
    if request.method == "GET":
        username = ''
        result = add_to_cart(id_product, username) # TODO Вызвать ответственную за это действие функцию add_to_cart(id_product, username)
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def cart_del_view_json(request, id_product):
    if request.method == "GET":
        username = ''
        result =  remove_from_cart(id_product, username)# TODO Вызвать ответственную за это действие функцию remove_from_cart(id_product, username)
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})

def cart_view(request):
    if request.method == "GET":
        username = ''
        data = view_in_cart(username)[username]  # Получаем корзину пользователя username

        products = []  # Список продуктов
        for product_id, quantity in data['products'].items():
            product = DATABASE[product_id]  # Получаем информацию о продукте
            # TODO в словарь product под ключом "quantity" запишите текущее значение количества товара в корзине
            product["quantity"] = quantity  # Реализуйте
            # TODO в словарь product под ключом "price_total" посчитайте и запишите общую стоимость товара как произведение
            #  его количества в корзине на цену с учетом скидки ('price_after'). Значение цены "price_total" приведите к формату
            #  2 символов после запятой
            product["price_total"] = product['price_after'] * quantity  # Реализуйте
            # TODO добавьте словарь product в конец списка products
            # Реализуйте
            products.append(product)
        return render(request, "app_store/cart.html", context={"products": products})


