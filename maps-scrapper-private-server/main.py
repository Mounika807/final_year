from src.gmaps import Gmaps
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gmaps.places(queries, min_reviews=5, max_reviews=100, has_phone=True, has_website=False)
# Gmaps.places(queries, category_in=[Gmaps.Category.DentalClinic, Gmaps.Category.DentalLaboratory])
# https://github.com/omkarcloud/google-maps-scraper
# Gmaps.places(queries, sort=[Gmaps.SORT_BY_REVIEWS_DESCENDING])
# Gmaps.places(queries, sort=[Gmaps.SORT_BY_RATING_DESCENDING])
# Gmaps.places(queries, sort=[Gmaps.SORT_BY_REVIEWS_DESCENDING, Gmaps.SORT_BY_NOT_HAS_WEBSITE])
# Gmaps.places(queries, sort=[Gmaps.SORT_BY_NAME_ASCENDING])
# Gmaps.places(queries, sort=[[Gmaps.Fields.CATEGORIES, Gmaps.SORT_ASCENDING]])
# Gmaps.places(queries, sort=[[Gmaps.Fields.CATEGORIES, Gmaps.SORT_DESCENDING]])

import json

@app.get("/private/api/nearby/restaurants/{no_of_restaurents}/{query}")
async def fetch_nearby_restaurents(no_of_restaurents:int,query:str):
    result = Gmaps.places(["best restaurants near "+query], max=no_of_restaurents, sort=[Gmaps.MOST_RELEVANT])
    r = json.loads(result)
    print(r)
    return JSONResponse(content=r, media_type="application/json")

@app.get("/private/api/nearby/places/{no_of_places}/{query}")
async def fetch_nearby_places(no_of_places:int,query:str):
    result = Gmaps.places(["best places to visit near "+query], max=no_of_places, sort=[Gmaps.MOST_RELEVANT])
    r = json.loads(result)
    print(r)
    return JSONResponse(content=r, media_type="application/json")

@app.get("/private/api/scrap/maps/{data}/max_results/{result_count}/fetch_review/{fetch_review}/max_review_count/{max_review_count}")
async def read_root(data: str,result_count:int=1,max_review_count:int=0,fetch_review:bool=False):
    # Assuming Gmaps.places returns a dictionary
    result = Gmaps.places([data], max=result_count,scrape_reviews=fetch_review,reviews_max=max_review_count)

    # r = json.dumps()
    r = json.loads(result)
    print(r)
    # Return the result as JSON response
    return JSONResponse(content=r, media_type="application/json")

# queries = [rohan]
# # Gmaps.places(queries, max=100, has_phone=True, sort=[Gmaps.SORT_BY_REVIEWS_DESCENDING] , category_in=[Gmaps.Category.HardwareStore, Gmaps.Category.PaintStore,Gmaps.Category.PaintingsStore])
# t = Gmaps.places(queries, max=1)

# print(t)

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application using the ASGI server (uvicorn)
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
