from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import io

app = FastAPI()

# Cho phép web (GitHub Pages) truy cập API này
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # sau này có thể sửa lại chỉ cho phép domain của anh
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EcgResult(BaseModel):
    ischemia: bool
    dangerous_arrhythmia: bool
    summary: str

def dummy_ecg_ai(image: Image.Image) -> EcgResult:
    """
    HÀM GIẢ LẬP (DEMO):
    Sau này sẽ được thay bằng mô hình AI thật (deep learning).
    Tạm thời chỉ trả về summary đơn giản.
    """
    width, height = image.size

    ischemia = False
    dangerous_arrhythmia = False

    # Ở bản thật: tại đây sẽ gọi model deep learning để:
    # - nhận diện ST chênh
    # - T đảo
    # - Q bệnh lý
    # - rối loạn nhịp...
    # Bản demo chỉ mô tả kích thước ảnh.
    summary = f"Ảnh ECG được AI tiếp nhận với kích thước {width}x{height}px. (Mô hình AI thật sẽ đưa nhận định chi tiết tại đây)."

    return EcgResult(
        ischemia=ischemia,
        dangerous_arrhythmia=dangerous_arrhythmia,
        summary=summary
    )

@app.post("/api/ecg-analyze")
async def ecg_analyze(file: UploadFile = File(...)):
    """
    Endpoint chính: nhận 1 file ảnh ECG, trả về:
    - ischemia: có gợi ý thiếu máu cơ tim không
    - dangerous_arrhythmia: có gợi ý rối loạn nhịp nguy hiểm không
    - summary: text tóm tắt để hiển thị trên web
    """
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