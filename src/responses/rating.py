def response_rating(rating_orm, identifier: str):
    # Запоминаем данные пользователя, для которого был запрос
    user_data = next((rating for rating in rating_orm if rating.user.identifier == identifier), None)

    if user_data:
        user_place = next(
            index + 1 for index, rating in enumerate(rating_orm) if rating.user.identifier == identifier)
        user_reputation = user_data.reputation
        user_identifier = user_data.user.identifier
        user_entry = {
            'place': user_place,
            'reputation': user_reputation,
            'identifier': f"{user_identifier[0:4]}XXXX{user_identifier[-3:]}"
        }
    else:
        user_entry = None

    # Создаем список словарей для первых 50 пользователей
    rating_dict_list = [
        {
            'place': index + 1,
            'reputation': rating.reputation,
            'identifier': f"{rating.user.identifier[0:4]}XXXX{rating.user.identifier[-3:]}"
        }
        for index, rating in enumerate(rating_orm[:50])
    ]

    # Формируем окончательный ответ
    response = {
        'user': user_entry,  # Данные пользователя (может быть None)
        'top_rating': rating_dict_list  # Список первых 50 пользователей
    }

    return response
