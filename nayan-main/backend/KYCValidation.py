from pydantic import BaseModel, Field, validator
from datetime import date
from enum import Enum


# KYC Document Base Model for imput (Currently for all documents type) 
class KYCDocument(BaseModel):
    id_number: str = Field(..., description="The ID card number.")
    name: str = Field(..., description="Full name of the individual.")
    dob: str = Field(..., description="Date of birth in any common format (e.g., YYYY-MM-DD, MM/DD/YYYY).")
    gender: str = Field(..., description="Gender of the individual.")
    district: str = Field(..., description="The individual's home district.")
    municipality: str = Field(..., description="The individual's municipality.")
    father_name: str = Field(..., description="Full name of the father.")
    mother_name: str = Field(..., description="Full name of the mother.")

        
    class Config:
        schema_extra = {
            "example": {
                "id_number": "65668093",
                "name": "Aayam Bir Bikram Dom",
                "dob": "1992-07-04",
                "gender": "Male",
                "district": "Rupandehi",
                "municipality": "Tribeni",
                "father_name": "Aakar Pratap Jogi",
                "mother_name": "Rukmita Khatave"
            }
        }

class KYCResponse(BaseModel):
    original_data: KYCDocument
    corrected_text: str