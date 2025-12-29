import json
import os
from app_store.models import DATABASE

PATH_WISHLIST = 'wishlist.json'


def view_in_wishlist(username: str = '') -> dict:  # Уже реализовано, не нужно здесь ничего писать
    """
    Просматривает содержимое Избранного wishlist.json, если пользователя с именем username нет в Избранном, то создает его там

    :param username: Имя пользователя
    :return: Содержимое 'wishlist.json'
    """
    empty_user_wishlist = {'products': []}  # Пустая Избранное для пользователя

    if os.path.exists(PATH_WISHLIST):  # Если файл с Избранным существует
        with open(PATH_WISHLIST, encoding='utf-8') as f:  # Открываем файл
            wishlist = json.load(f)  # Считываем Избранное
            if username not in wishlist:  # Если пользователя нет в Избранном, то создаем запись с пустой Избранным для него
                wishlist[username] = empty_user_wishlist
    else:  # Если файла с Избранным нет
        wishlist = {username: empty_user_wishlist}

    # Запись словаря wishlist в wishlist.json
    with open(PATH_WISHLIST, mode='w', encoding='utf-8') as f:  # Создаём файл и записываем Избранное
        json.dump(wishlist, f)

    return wishlist  # Возвращаем содержимое Избранного


def add_to_wishlist(id_product: str, username: str = '') -> bool:
    """
    Добавляет продукт в Избранное. Если в Избранное нет данного продукта, то добавляет его с количеством равное 1.
    Если в Избранное есть такой продукт, то не добавляет его.

    :param id_product: Идентификационный номер продукта в виде строки.
    :param username: Имя пользователя

    :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления(товара по id_product
    не существует).
    """
    wishlist = view_in_wishlist(username)  # TODO Помните, что у вас есть уже реализация просмотра корзины view_in_cart(username),
    # поэтому, чтобы загрузить данные из корзины, не нужно заново писать код.
    if not id_product in DATABASE:
        return False
    # TODO Проверьте существует ли добавляемый товар с id_product в базе данных DATABASE, если нет, то возвращаем False,
    #  так как добавление в корзину прошло неуспешно.

    user_wishlist = wishlist[username]['products']  # TODO в переменную user_cart запишите данные об товарах пользователя.
    #  Т.е. в user_cart будет словарь из ключа "products" для соответствующего пользователя по username.

    # ! Обратите внимание, что в переменной cart под ключем значения username находится словарь с ключом "products".
    # ! Именно в cart[username]["products"] лежит словарь где по id продуктов можно получить число продуктов в корзине.
    # ! Т.е. чтобы обратиться к продукту с id_product = "1" в переменной cart нужно вызвать
    # ! cart[username]["products"][id_product]
    # ! Далее уже сами решайте, как и в какой последовательности дальше действовать.

    # TODO Проверьте, а существует ли товар с id_product в корзине пользователя user_cart, если товар существует,
    #  то увеличиваем его количество в user_cart на 1, иначе товар добавляется в первый раз и его количество равно 1.
    if id_product not in user_wishlist:
        user_wishlist[id_product] = 1

    # TODO Не забываем записать обновленные данные cart в 'cart.json'. Так как именно из этого файла мы считываем данные
    #  и если мы не запишем изменения, то считать измененные данные затем не получится. Так user_cart является частью
    #  словаря cart, то любые изменения в user_cart аналогично отражаются в cart, поэтому достаточно записать
    #  в 'cart.json' словарь из cart
    with open(PATH_WISHLIST, mode='w', encoding='utf-8') as f:
        json.dump(wishlist, f)
    return True

def remove_from_wishlist(id_product: str, username: str = '') -> bool:
    """
    Добавляет позицию продукта из Избранное. Если в Избранное есть такой продукт, то удаляется ключ в словаре
    с этим продуктом.

    :param id_product: Идентификационный номер продукта в виде строки.
    :param username: Имя пользователя

    :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
    не существует).
    """
    wishlist = view_in_wishlist(username)  # TODO Помните, что у вас есть уже реализация просмотра корзины view_in_cart(username),
    # поэтому, чтобы загрузить данные из корзины, не нужно заново писать код.

    # С переменной user_cart функции remove_from_cart ситуация аналогичная, что с cart функции add_to_cart
    user_wishlist = wishlist[username]["products"]  # TODO в переменную user_cart запишите данные об товарах пользователя.
    #  Т.е. в user_cart будет словарь из ключа "products" для соответствующего пользователя по username.

    # TODO Проверьте, существует ли товар с id_product в корзине пользователя user_cart, если нет, то возвращаем False.
    if id_product not in user_wishlist:
        return False
    # TODO Если существует товар, то удаляем ключ 'id_product' у user_cart,
    #  вспомните как удалять ключи у словаря.
    del user_wishlist[id_product]
    # TODO Не забываем записать обновленные данные cart в 'cart.json', аналогично как делали в add_to_cart
    with open(PATH_WISHLIST, mode='w', encoding='utf-8') as f:
        json.dump(wishlist, f)
    return True
