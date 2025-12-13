from django.shortcuts import render

# Create your views here.

from weather_api import current_weather

from django.http import JsonResponse
# TODO из weather_api импортируйте функцию current_weather


# def weather_view(request):
#     if request.method == "GET":
#         data = current_weather(lat=59.93, lon=30.31)  # TODO Вызовите функцию current_weather с параметрами lat=59.93, lon=30.31
#         # JsonResponse возвращаем объект JSON в качестве ответа.
#         # Параметр json_dumps_params используется, чтобы передать ensure_ascii=False
#         # как помните это необходимо для корректного отображения кириллицы
#         return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
#                                                      'indent': 4})


def weather_view(request):
    if request.method == "GET":
        lat = request.GET.get('lat')  # данные придут в виде строки
        lon = request.GET.get('lon')  # данные придут в виде строки
        if lat and lon:  # Если были переданы ключи lat и lon в параметрах запроса
            data = current_weather(lat=lat, lon=lon)  # Передаём их в функцию и получаем словарь с погодой
        else:  # Иначе получаем данные о погоде из Санкт-Петербурга
            data = current_weather(59.93, 30.31)
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,

                                                     'indent': 4})