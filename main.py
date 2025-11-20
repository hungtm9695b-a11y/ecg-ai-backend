from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import io

app = FastAPI()

# ===== CORS CHUẨN =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://hungtm9695b-a11y.github.io",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EcgResult(BaseModel):
    ischemia: bool
    dangerous_arrhythmia: bool
    summary: str

def dummy_ecg_ai(image: Image.Image) -> EcgResult:
    width, height = image.size

    ischemia = False
    dangerous_arrhythmia = False

    summary = (
        f"Ảnh ECG (demo) kích thước {width}x{height}px. "
        "Mô hình AI thật sẽ phân tích khi tích hợp."
    )

    return EcgResult(
        ischemia=ischemia,
        dangerous_arrhythmia=dangerous_arrhythmia,
        summary=summary,
    )

@app.post("/api/ecg-analyze")
async def ecg_analyze(file: UploadFile = File(...)):
    content = await file.read()
    image = Image.open(io.BytesIO(content)).convert("RGB")

    result = dummy_ecg_ai(image)

    return {
        "ischemia": result.ischemia,
        "dangerous_arrhythmia": result.dangerous_arrhythmia,
        "summary": result.summary,
    }

@app.get("/")
def root():
    return {"message": "ECG AI backend is running."}
