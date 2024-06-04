# Core imports
from fastapi import APIRouter, Request, Depends, UploadFile
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAuthenticated
)

# App imports
from services import CategoryServices
from schemas import CategorySchema, ProductDetailSchema
from services import ProductServices

# Pytohn imports
from typing import List
from openai import OpenAI

api_url = "https://api.openai.com/v1/chat/completions"

api_key = ""

prompt = """
First of all, I will give you a categories in json format.

[CATEGORIES]

I will provide you with a product_list in JSON format to use as a database.
Learn this products.

[PRODUCTS]

I will provide you with an event_list containing event_type and several product IDs in json format.

[EVENT_LIST]

Examine the user's interactions and the products based on interaction types in the event_list.
Provide the user with 5 product recommendations in json format for purchase from the database you have learned. 
do not write anything just give me the recommended products in json format

"The priority order of event types is as follows: 'purchased' > 'added_to_cart' > 'added_to_favorites' > 'details_viewed'."
"Suggestions for similar products based on their respective priority order."
"Make recommendations based on the most suitable size and color attributes."
"If the products in the event_list do not all have the same category_id, suggest at least one similar product in the same color and size for each category_id."
"""

client = OpenAI(api_key=api_key)

router = APIRouter()


@router.get(
    "/{user_id}",
    # response_model=FileSchema,
    # dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def recommend(request: Request, user_id: int):
    categories: List[CategorySchema] = await CategoryServices().get_category_tree()
    products: List[ProductDetailSchema] = await ProductServices().get_all_product_details()

    parsed_products = []
    for product in products:
        
        attrs = {}
        
        for attr in product.attributes:
            attrs[attr.name] = attr.value
            
        parsed_products.append({
            "id": product.id,
            "title": product.title,
            "description": product.description,
            "category_id": product.category_id,
            "price": product.price,
            **attr
        })
        
    return products
    # completion = client.chat.completions.create(model="gpt-4o",messages=[
    # {"role":"system","content":prompt},
    # {"role":"user","content":categories},
    # {"role":"user","content":products},
    # {"role":"user","content":events},
    #   ],)

    # return(completion.choices[0].message.content)
