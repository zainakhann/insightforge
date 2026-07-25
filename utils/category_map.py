"""
Maps Olist's ~70 raw product categories into Nova Commerce's 6 brand categories.
"""

NOVA_CATEGORY_MAP = {
    # Electronics
    "computers_accessories": "Electronics", "electronics": "Electronics",
    "telephony": "Electronics", "fixed_telephony": "Electronics",
    "computers": "Electronics", "tablets_printing_image": "Electronics",
    "audio": "Electronics", "cine_photo": "Electronics",
    "small_appliances": "Electronics", "home_appliances": "Electronics",
    "home_appliances_2": "Electronics", "air_conditioning": "Electronics",
    "consoles_games": "Electronics", "dvds_blu_ray": "Electronics",

    # Furniture
    "furniture_decor": "Furniture", "furniture_living_room": "Furniture",
    "furniture_bedroom": "Furniture", "furniture_mattress_and_upholstery": "Furniture",
    "office_furniture": "Furniture", "kitchen_dining_laundry_garden_furniture": "Furniture",

    # Fashion
    "fashion_bags_accessories": "Fashion", "fashion_shoes": "Fashion",
    "fashion_male_clothing": "Fashion", "fashion_female_clothing": "Fashion",
    "fashion_underwear_beach": "Fashion", "fashion_sport": "Fashion",
    "fashio_female_clothing": "Fashion", "fashion_childrens_clothes": "Fashion",
    "watches_gifts": "Fashion", "luggage_accessories": "Fashion",

    # Home Goods
    "housewares": "Home Goods", "home_confort": "Home Goods",
    "home_comfort_2": "Home Goods", "bed_bath_table": "Home Goods",
    "garden_tools": "Home Goods", "costruction_tools_garden": "Home Goods",
    "home_construction": "Home Goods", "la_cuisine": "Home Goods",
    "flowers": "Home Goods", "christmas_supplies": "Home Goods",
    "cool_stuff": "Home Goods", "art": "Home Goods",

    # Sports Equipment
    "sports_leisure": "Sports Equipment", "toys": "Sports Equipment",
    "fashion_sport_2": "Sports Equipment",

    # Beauty
    "perfumery": "Beauty", "health_beauty": "Beauty",
    "diapers_and_hygiene": "Beauty",
}

DEFAULT_CATEGORY = "Home Goods"  # fallback bucket for anything unmapped

def map_category(english_category: str) -> str:
    if not isinstance(english_category, str):
        return DEFAULT_CATEGORY
    return NOVA_CATEGORY_MAP.get(english_category, DEFAULT_CATEGORY)