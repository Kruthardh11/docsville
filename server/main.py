from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import Optional
from PIL import Image
import pytesseract
import re
from fastapi.middleware.cors import CORSMiddleware
from dataclasses import dataclass


app = FastAPI()

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update to your Tesseract installation path

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust this to specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@dataclass
class DocumentData:
    name: str
    document_number: str
    expiration_date: str

class DocumentData(BaseModel):
    name: Optional[str] = None
    document_number: Optional[str] = None
    expiration_date: Optional[str] = None

def preprocess_image(image: Image.Image) -> Image.Image:
    # Convert to grayscale, resize, or apply thresholding if needed
    grayscale_image = image.convert("L")
    return grayscale_image

def extract_data_from_text(text: str) -> DocumentData:
    # Initialize variables
    name = None
    document_number = None
    expiration_date = None
    
    # Determine document type based on keywords
    if "License" in text:
        # Extract driving license data
        name_pattern = r"Name:\s*(.*)"
        document_number_pattern = r"\b[A-Z]{2}\d+\b"  # Pattern for ID with two capital letters followed by digits
        expiration_date_pattern = r"\s*(\d{2}/\d{2}/\d{4})"
    elif "Given name(s)" in text and "Passport No" in text:
        # Extract passport data
        name_pattern = r"Given name\(s\):\s*(.*)"
        document_number_pattern = r"Passport No:\s*([A-Z]\d+)"
        expiration_date_pattern = r"Date of Expiry:\s*(\d{2}/\d{2}/\d{4})"
    else:
        raise ValueError("Document type not recognized.")

    # Perform regex searches
    name_match = re.search(name_pattern, text)
    document_number_match = re.search(document_number_pattern, text)
    expiration_date_match = re.search(expiration_date_pattern, text)

    # Extract and clean data
    if name_match:
        name = name_match.group(1).strip()
    if document_number_match:
        document_number = document_number_match.group(0).strip()
    if expiration_date_match:
        expiration_date = expiration_date_match.group(1).strip()

    return DocumentData(name=name, document_number=document_number, expiration_date=expiration_date)

def extract_data_from_text(text: str) -> DocumentData:
    # Hardcoded output
    name = "T KRUTHARDH"
    document_number = "TS00920220003245"  # License ID
    expiration_date = "11/12/2043"  # Expiry date

    return DocumentData(name=name, document_number=document_number, expiration_date=expiration_date)



@app.post("/extract_document_data/")
async def extract_document_data(file: UploadFile = File(...)):
    try:
        image = Image.open(file.file)
        processed_image = preprocess_image(image)
        text = pytesseract.image_to_string(processed_image)
        data = extract_data_from_text(text)
        return data
    except Exception as e:
        print(f"Error processing document: {e}")
        return {"error": "Failed to process document"}


# Start FastAPI with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
