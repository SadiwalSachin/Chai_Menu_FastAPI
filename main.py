from fastapi import FastAPI, Query
import uvicorn
from models import MenuItem, MenuResponse
from data import menu_items

app = FastAPI(
    title="Chai Point Menu API",
    description="Read only menu api for kiosk and web applications"
)


@app.get("/")
def root():
    return {
        "message":"Welcome to chai point bengaluru"
    }
    

@app.get("/menu",response_model=MenuResponse)
def get_menu(category:str | None = Query(None,description="filter by chai, snack or combo")):
    if category:
        filtered = [item for item in menu_items if item["category"] == category.lower()]

        if not filtered:
            raise HTTPException(staus_code = 404, detail = f"No item found in category: {category}")
        
        return MenuResponse(status=200,message="Items with category",items=filtered)
    
    
    
    return MenuResponse(status=200,message="Items with no category",items=menu_items)


@app.get("/menu/{item_id}",response_model=MenuItem)
def get_single_item(item_id:int):
    for item in menu_items:
        if item["id"] == item_id:
            return item
    
    raise HTTPException(staus_code = 404, detail = f"No item found")