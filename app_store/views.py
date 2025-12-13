from django.http import JsonResponse, HttpResponse, HttpResponseNotFound

from app_store.models import DATABASE


# def product_view_json(request):
#     if request.method == "GET":
#         return  JsonResponse(DATABASE,
#                              json_dumps_params={
#                                  'ensure_ascii':False,
#                                  'indent': 4
#                              })# TODO Вернуть JsonResponse с объектом DATABASE и параметрами отступов и кодировок,
#         # как в приложении app_weather

def shop_view(request):
    if request.method == 'GET':
        with open('app_store/shop.html', 'r', encoding='utf-8')as f:
            data = f.read()
        return HttpResponse(data)

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

        return JsonResponse(DATABASE, json_dumps_params={'ensure_ascii': False,
                                                         'indent': 4})


def product_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):  # Проверяем, что в параметр page передали значение строкового типа
            for data in DATABASE.values():  # Перебираем все товары (словари) в DATABASE
                if data['html'] == page:  # Если значение переданного параметра совпадает именем html файла, получаемого по ключу
                    with open(f'app_store/product/{page}.html', encoding="utf-8") as f:
                        s = f.read()
                        return HttpResponse(s)

                    # TODO 1. Откройте файл open(f'app_store/product/{page}.html', encoding="utf-8") (Не забываем про контекстный менеджер with)
                    # TODO 2. Прочитайте его содержимое
                    # TODO 3. Верните HttpResponse c содержимым html файла

            # Если за всё время поиска не было совпадений, то значит по данному имени нет соответствующей
            # страницы товара и можно вернуть ответ с ошибкой HttpResponse(status=404)
            return HttpResponse(status=404)

        elif isinstance(page, int):
            data = DATABASE.get(str(page))
            if data:
                with open(f'app_store/product/{data["html"]}.html',
                          encoding='utf-8') as f:
                    return HttpResponse(f.read())
            return HttpResponse(status=404)
