
def response_raiting(rating_orm):
    rating_dict_list = [
        {
            'current_level': rating.current_level,
            'reputation': rating.reputation,
            'phone': rating.user
        }
        for rating in rating_orm
    ]
    return rating_dict_list
