
def string_to_list(food_ids):
    food_ids = food_ids.strip('[]')
    food_ids_list = food_ids.split(',')
    return [int(food_id) for food_id in food_ids_list if food_id.strip()]
