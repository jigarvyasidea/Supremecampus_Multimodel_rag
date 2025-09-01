from fastapi import FastAPI
import json

app = FastAPI()

# Load data from JSON file
def load_data():
    with open('patient.json', 'r') as f:
        data = json.load(f)
    return data

@app.get("/")
def abc():
    return {"message": "Hello World"}

@app.get("/about")
def about():
    return {"message": "This is about us Page of Golden Eagle"}

@app.get("/patients")
def get_patients():
    data = load_data()
    return {"patients": data}
