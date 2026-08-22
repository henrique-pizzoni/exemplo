from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    text: str = None
    is_done: bool = False

items = []

@app.post("/items")
def create_item(item:Item):
    items.append(item)
    return items

@app.get("/items")
def list_items(limit: int=10):
    return items[:limit]

@app.get("/items/{item_id}")
def get_item_id(item_id: int) -> Item:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} Not Found")
    

