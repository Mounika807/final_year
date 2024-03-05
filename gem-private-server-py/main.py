import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from typing import List
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from youtubesearchpython import *
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0)
# class Restaurant(BaseModel):
#     restaurant_name: str = Field(..., description="The name of the restaurant near the destination.")
#     restaurant_type: str = Field(..., description="The type of cuisine served in the restaurant. it can be veg/non-veg/vegan etc")
#     address: str = Field(..., description="full address of the restaurant.")
#     rating: float = Field(..., description="The rating of the restaurant (1-5).")

class PlaceDetails(BaseModel):
    place_name: str = Field(..., description="The name of the place.")
    place_description: str = Field(..., description="Description of the place.")
    # bus_cost: int = Field(..., description="The cost of bus travel from destination to the place.")
    famous_food: List[str] = Field(..., description="List of famous food items.")
    place_rating: int = Field(..., description="The rating of the place (1-5).")
    # best_restaurants: List[Restaurant] = Field(..., description="List of the best restaurants near the place.")

class City(BaseModel):
    city: str = Field(..., description="The name of the city.")
    details: PlaceDetails = Field(..., description="Details of the best places to visit in the city.")

class CityRecommendation(BaseModel):
    destinations: List[City] = Field(..., description="List of city recommendations.")

parser = JsonOutputParser(pydantic_object=CityRecommendation)

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query","restaurant_type"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
) 

chain = prompt | llm | parser



@app.post("/private/api/gen/{city}/trip_type/{trip_type}/people/{people}/travel_budget/{travel_budget}/restaurant_type/{food_type}/food_budget/{food_budget}/first_time_visit/{first_time_visit}")
async def read_root(city: str,food_type:str,travel_budget:str,trip_type:str,food_budget:str,first_time_visit:str,people:int):
    print('request received')
    visit_prompt = "we have already visited this city"

    if first_time_visit.lower() == "yes":
        visit_prompt = "its our first time visit"

    # res = chain.invoke({"query": f"suggest best place to visit in city: 
    #                     {city}, 
    #                     only {food_type} restaurents, places must be {trip_type} only ,
    #                       {visit_prompt}, travel_budget: {travel_budget}, food_budget: {food_budget}, 
    #                       we are total {people} members "})
    
    
    res = chain.invoke({"query": f"suggest best place to visit in city: {city}, suggest atleast 10 places, places must be {trip_type} only, travel_budget: {travel_budget} "})

    print(res)
    return JSONResponse(content=res, media_type="application/json")

@app.post("/private/api/fetch/video/{place}/limit/{limit}/sort/{sort}")
async def read_root(place:str,limit:int,sort:str):
    sorts = {
        "relevance":VideoSortOrder.relevance,
        "uploadDate":VideoSortOrder.uploadDate,
        "viewCount" :VideoSortOrder.viewCount,
        "rating":VideoSortOrder.rating,
    }

    videosSearch = CustomSearch(place,  sorts[sort], limit = limit,region ='IN',)
    return JSONResponse(content=videosSearch.result(), media_type="application/json")

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application using the ASGI server (uvicorn)
    uvicorn.run(app, host="127.0.0.1", port=9000, reload=True)