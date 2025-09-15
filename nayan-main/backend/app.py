from fastapi import FastAPI
from KYCValidation import KYCDocument, KYCResponse 
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from contextlib import asynccontextmanager 

model_cache = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[INFO] Application startup: Loading ML models...")

    ENGLISH_MODEL_DIR = "./model/ocr_correction_model"
    NEPALI_MODEL_DIR = "./model/ocr-post-corr-nepali/"

    gpu_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    cpu_device = torch.device("cpu")

    print(f"[INFO] Using GPU for Nepali Model: {gpu_device}")
    print(f"[INFO] Using CPU for English Model: {cpu_device}")

    try:
        print(f"[INFO] Loading English model from: {ENGLISH_MODEL_DIR}")
        eng_model = AutoModelForSeq2SeqLM.from_pretrained(ENGLISH_MODEL_DIR)
        eng_tokenizer = AutoTokenizer.from_pretrained(ENGLISH_MODEL_DIR)

        eng_model.to(cpu_device)
        eng_model.eval()
        
        model_cache["english"] = {
            "model": eng_model, "tokenizer": eng_tokenizer, "device": cpu_device
        }
        print("[INFO] English model loaded successfully onto CPU.")
    except OSError:
        print(f"[❌ ERROR] English model not found at '{ENGLISH_MODEL_DIR}'.")

    try:
        print(f"[INFO] Loading Nepali model from: {NEPALI_MODEL_DIR}")
        nep_model = AutoModelForSeq2SeqLM.from_pretrained(NEPALI_MODEL_DIR)
        nep_tokenizer = AutoTokenizer.from_pretrained(NEPALI_MODEL_DIR, use_fast=False) 
        
        nep_model.to(gpu_device)
        nep_model.eval()
        
        model_cache["nepali"] = {
            "model": nep_model, "tokenizer": nep_tokenizer, "device": gpu_device
        }
        print("[INFO] Nepali model loaded successfully onto GPU.")
    except OSError:
        print(f"[❌ ERROR] Nepali model not found at '{NEPALI_MODEL_DIR}'.")
    
    yield

    print("[INFO] Application shutdown: Clearing model cache.")
    model_cache.clear()
    

app = FastAPI(
    title="KYC OCR Post-Correction API",
    description="An API to receive KYC data, which will eventually be cleaned by a Transformer model.",
    version="1.1.0",
    lifespan=lifespan  
)

origins = [
    "http://localhost:5173", 
    "http://localhost:3000", 
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.post("/kyc/english/", response_model=KYCResponse, tags=["Post-OCR Correction"])
async def process_english_kyc_data(kyc_data: KYCDocument):
    if "english" not in model_cache or model_cache["english"] is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="English model is not available.")

    eng_cache = model_cache["english"]
    model, tokenizer, device = eng_cache["model"], eng_cache["tokenizer"], eng_cache["device"]
    input_text = f"ID: {kyc_data.id_number}, Name: {kyc_data.name}, DOB: {kyc_data.dob}, Gender: {kyc_data.gender.value}, District: {kyc_data.district}, Municipality: {kyc_data.municipality}, Father's name: {kyc_data.father_name}, Mother's name: {kyc_data.mother_name}"
    inputs = tokenizer(input_text, return_tensors="pt").to(device)

    with torch.no_grad():
        output_ids = model.generate(**inputs, max_length=128, num_beams=5, early_stopping=True)
    
    corrected_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return KYCResponse(original_data=kyc_data, corrected_text=corrected_text)


@app.post("/kyc/nepali/", response_model=KYCResponse, tags=["Post-OCR Correction"])
async def process_nepali_kyc_data(kyc_data: KYCDocument):
    if "nepali" not in model_cache or model_cache["nepali"] is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="Nepali model is not available.")
    nep_cache = model_cache["nepali"]
    model, tokenizer, device = nep_cache["model"], nep_cache["tokenizer"], nep_cache["device"]

    input_text = f"परिचयपत्र नम्बर: {kyc_data.id_number}, नाम: {kyc_data.name}, जन्म मिति: {kyc_data.dob}, लिङ्ग: {kyc_data.gender}, जिल्ला: {kyc_data.district}, नगरपालिका: {kyc_data.municipality}, बुबाको नाम: {kyc_data.father_name}, आमाको नाम: {kyc_data.mother_name}"
    inputs = tokenizer(input_text, return_tensors="pt").to(device)

    with torch.no_grad():
        output_ids = model.generate(**inputs, max_length=256, num_beams=5, early_stopping=True) 
    
    corrected_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return KYCResponse(original_data=kyc_data, corrected_text=corrected_text)