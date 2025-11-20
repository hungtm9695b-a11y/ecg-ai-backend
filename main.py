import json
import base64
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

# Khởi tạo client OpenAI - dùng biến môi trường OPENAI_API_KEY
client = OpenAI()

app = FastAPI(title="ECG OpenAI Backend")

# Cho phép CORS để frontend (web) gọi API dễ dàng
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # có thể thu hẹp sau cho an toàn hơn
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EcgAIResult(BaseModel):
    ischemia: str                # "none" | "possible" | "likely"
    dangerous_arrhythmia: bool
    summary: str
    details: str

PROMPT = """Bạn là bác sĩ tim mạch.

Ảnh kèm theo là ECG 12 chuyển đạo (25mm/s, 10mm/mV).

NHIỆM VỤ:
1. Phân tích:
   - Nhịp, tần số, trục.
   - ST chênh, sóng T, sóng Q bệnh lý nếu có.
   - Có gợi ý thiếu máu cơ tim cấp hay không (STEMI / NSTEMI gợi ý).
   - Có rối loạn nhịp nguy hiểm hay không.

2. Trả kết quả dưới dạng 1 JSON object duy nhất, KHÔNG thêm chữ nào khác, đúng mẫu:
{
  "ischemia": "none" | "possible" | "likely",
  "dangerous_arrhythmia": true hoặc false,
  "summary": "1-3 câu tóm tắt ngắn gọn, dễ hiểu cho bác sĩ tuyến cơ sở (tiếng Việt).",
  "details": "giải thích chi tiết hơn về phân tích ECG (tiếng Việt)."
}
"""


@app.post("/api/ecg-openai", response_model=EcgAIResult)
async def analyze_ecg(file: UploadFile = File(...)):
    """Nhận ảnh ECG, gửi lên OpenAI, trả về kết quả dạng JSON chuẩn."""
    content = await file.read()
    b64 = base64.b64encode(content).decode("utf-8")
    image_url = f"data:image/jpeg;base64,{b64}"

    # Gọi OpenAI Chat Completions (vision)
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # có thể đổi thành "gpt-4o" nếu tài khoản cho phép
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url},
                    },
                ],
            }
        ],
        temperature=0.1,
    )

    json_str = response.choices[0].message.content
    data = json.loads(json_str)

    # Dùng EcgAIResult để validate dữ liệu trả về
    return EcgAIResult(**data)


@app.get("/")
def root():
    return {"message": "ECG OpenAI backend is running."}