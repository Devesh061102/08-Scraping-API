from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

# Function to load items from JSON file
def load_items():
    with open('items.json', 'r') as f:
        return json.load(f)

# Load items from JSON file
items = load_items()

@app.get('/')
def hello():
    return {'message': 'Hello, FastAPI!'}

@app.get('/get-items', response_model=List[Item])
def get_items():
    return items

@app.get('/get-item', response_model=Item)
def get_item(name: str):
    for item in items:
        if name == item['name']:
            return item
    raise HTTPException(status_code=404, detail="Record does not exist")

@app.post('/add-items', status_code=201)
def add_items(item: Item):
    items.append(item.dict())
    # Save updated items to JSON file
    with open('items.json', 'w') as f:
        json.dump(items, f, indent=4)
    return {"message": "Item added successfully"}

@app.put('/update-item')
def update_item(item: Item):
    for i in range(len(items)):
        if items[i]['name'] == item.name:
            items[i]['price'] = item.price
            # Save updated items to JSON file
            with open('items.json', 'w') as f:
                json.dump(items, f, indent=4)
            return {"message": "Item updated successfully"}
    raise HTTPException(status_code=404, detail="Record does not exist")

@app.delete('/delete-item')
def delete_item(name: str):
    global items
    items = [item for item in items if item['name'] != name]
    # Save updated items to JSON file
    with open('items.json', 'w') as f:
        json.dump(items, f, indent=4)
    return {"message": "Item deleted successfully"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
    
# http://127.0.0.1:8000/docs
# uvicorn test:app --reload

# After we restart the server the data get lost and also get reset as 
# it was in the items.json file so we need a DATABASE to permanently store our data