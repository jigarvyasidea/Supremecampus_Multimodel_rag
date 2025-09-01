from fastapi import FastAPI, HTTPException
from typing import Annotated, Literal
from pydantic import BaseModel, Field
import json
import os

app = FastAPI()

# ✅ Patient model
class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Id of the patient")]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="City where the patient lives")]
    age: Annotated[int, Field(..., description="Age of the patient")]
    gender: Annotated[Literal["Male", "Female", "Other"], Field(..., description="Gender")]
    height: Annotated[float, Field(..., description="Height in meters")]
    weight: Annotated[float, Field(..., description="Weight in kilograms")]

    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"


# ✅ Load data from JSON file
def load_data():
    if not os.path.exists("patient.json"):
        return {}  # empty if file doesn't exist
    with open("patient.json", "r") as f:
        return json.load(f)


# ✅ Save data to JSON file
def save_data(data):
    with open("patient.json", "w") as f:
        json.dump(data, f, indent=2)


# ✅ POST endpoint to create a new patient
@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    # Convert patient object to dict and add BMI + verdict manually
    patient_dict = patient.model_dump()
    patient_dict["bmi"] = patient.bmi
    patient_dict["verdict"] = patient.verdict

    # Save to data
    data[patient.id] = patient_dict
    save_data(data)

    return {"message": "Patient created successfully", "patient": patient_dict}


# ✅ GET endpoint to retrieve patient by ID
@app.get("/patient/{patient_id}")
def get_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    return data[patient_id]
