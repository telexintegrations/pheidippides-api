import random
from fastapi import APIRouter, BackgroundTasks, Request, status
import httpx
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class TelexSetting(BaseModel):
    label: str
    type: str
    required: bool
    default: str


class TelexPayload(BaseModel):
    channel_id: str
    return_url: str
    settings: list[TelexSetting]


class PheidippidesPayload(BaseModel):
    message: str = "Could not resolve"
    username: str = "Pheidippides API"
    event_name: str = "Daily Book Recommendation"
    status: str = "success"


#telex integration.json endpoint
@router.get("/integration.json")
def integration_json(request: Request):
    base_url = str(request.base_url).rstrip("/")
    return {
        "data": {
            "date": {
                "created_at": "2025-02-21",
                "updated_at": "2025-02-21"
                },
            "descriptions": {
                "app_name": "Pheidippides API",
                "app_description": "An integration that suggests books to read based on any selected genre.",
                "app_logo": "https://i.imgur.com/D2619X4.jpeg",
                "app_url": f"{base_url}/pheidippides-api", #change to an env variable
                "background_color": "#fff"
            },
            "is_active": True,
            "integration_type": "interval",
            "integration_category": "Communication & Collaboration",
            "key_features": [
                "daily-book-recommendations"
                ],
            "author": "Ayodeji Oni",
            "settings": [
                {
                    "label": "genre",
                    "type": "dropdown",
                    "required": True,
                    "default": "fantasy",
                    "options": [
                            # "random", #issues with generating random genre on google api
                            "fantasy",
                            "mystery",
                            "horror",
                            "romance",
                            "dystopian",
                            "adventure",
                            "biography",
                            "history",
                            "comedy",
                            "nigerian"
                        ]
                },
                {
                    "label": "interval",
                    "type": "text",
                    "required": True,
                    "default": "* * * * *"
                }
            ],
            "target_url": os.getenv("TELEX_WEBHOOK"),
            "tick_url": f"{base_url}/pheidippides-api/tick" #change to an env variable
        }
    }


async def get_recommendation(genre, max_results=20, limit=20):
    #public api used for making queries
    API = {
        "google-books-api": f"https://www.googleapis.com/books/v1/volumes?q=subject:{genre}&maxResults={max_results}",
        "open-library-api": f"https://openlibrary.org/subjects/{genre}.json?limit={limit}"
    }

    chosen_api = API[random.choice(["google-books-api", "open-library-api"])]

    async with httpx.AsyncClient() as http_client:
        try:
            response = await http_client.get(chosen_api, timeout=10)
            texts = response.json()

            if chosen_api == API["google-books-api"]:
                #data extraction
                books = texts.get("items", [])
                random_book = random.choice(list(books))
                detail = random_book.get("volumeInfo")
                title = detail.get("title")
                authors = ", ".join(detail.get("authors"))
                published_date = detail.get("publishedDate")
                description = detail.get("description")
                
            elif chosen_api == API["open-library-api"]:
                #data extraction
                books = texts.get("works", [])
                random_book = random.choice(list(books))
                title = random_book.get("title")
                authors = random_book.get("authors")[0].get("name")
                published_date = random_book.get("first_publish_year")
                description = ", ".join(random_book.get("subject")[0:3])

            return f"📖Title: {title}\n\n✍Author(s): {authors}\n🗓Year: {published_date}\n\n📝Description: {description}"
        except: 
            return JSONResponse({"error": "Public API request failed"})
    
    

#Implemetation to get genre from request payload
async def receive_telex_payload(telex_payload: TelexPayload):

    #getting the selected genre
    genre = [s.default for s in telex_payload.settings if s.label == "genre"]
    genre = str(genre[0])
    
    pheidippides_message = await get_recommendation(genre)
    
    payload = PheidippidesPayload(message=pheidippides_message)

    async with httpx.AsyncClient() as http_client:
        try:
            response = await http_client.post(
                telex_payload.return_url, #change to channel_url
                json=payload.model_dump(),
                headers={
                    "Accept" : "application/json",
                    "Content-Type": "application/json"}
            )
            return response.json()
        except:
            return JSONResponse({"error": "Error communicating with telex"})
        

#telex tick_url endpoint
@router.post("/tick")
async def tick_url(telex_payload: TelexPayload, background_tasks: BackgroundTasks):
    background_tasks.add_task(receive_telex_payload, telex_payload)
    return JSONResponse({"status": "accepted"})