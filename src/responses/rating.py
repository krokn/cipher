
def response_rating(rating_orm):
    rating_dict_list = [
        {
            'current_level': rating.current_level,
            'reputation': rating.reputation,
            'identifier': rating.user.identifier
        }
        for rating in rating_orm
    ]
    return rating_dict_list
