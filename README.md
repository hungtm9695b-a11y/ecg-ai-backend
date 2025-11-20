# ECG OpenAI Backend

Backend nhỏ dùng FastAPI + OpenAI để đọc ECG từ ảnh (jpg/png), trả về kết quả dạng JSON.

## 1. Chạy trên máy (local)

```bash
# 1. Tạo & kích hoạt venv (tuỳ chọn)
python3 -m venv venv
source venv/bin/activate

# 2. Cài thư viện
pip install -r requirements.txt

# 3. Đặt biến môi trường OPENAI_API_KEY
export OPENAI_API_KEY="sk-...."

# 4. Chạy server
uvicorn main:app --reload --port 8001
```

Sau đó mở: `http://127.0.0.1:8001/docs` để test.

## 2. Deploy trên Render.com

1. Đẩy thư mục này lên GitHub (tạo repo mới, commit `main.py`, `requirements.txt`, `README.md`).
2. Vào https://dashboard.render.com → `New` → `Web Service`.
3. Kết nối với repo GitHub vừa tạo.
4. Cấu hình:
   - Environment: **Python**
   - Build Command:  
     `pip install -r requirements.txt`
   - Start Command:  
     `uvicorn main:app --host 0.0.0.0 --port 10000`
   - Auto deploy: On (tuỳ chọn)

5. Trong mục **Environment Variables** trên Render, thêm:
   - KEY: `OPENAI_API_KEY`
   - VALUE: `sk-...` (API key của bạn)

6. Deploy. Khi hiện status ✅ live, bạn có thể truy cập:
   - `https://tên-service-của-bạn.onrender.com/` → kiểm tra root.
   - `https://tên-service-của-bạn.onrender.com/docs` → xem Swagger UI.
   - Endpoint chính cho web:  
     `https://tên-service-của-bạn.onrender.com/api/ecg-openai`

## 3. Gọi từ frontend (JavaScript)

```js
const formData = new FormData();
formData.append("file", ecgFileInput.files[0]);

const res = await fetch("https://ten-service.onrender.com/api/ecg-openai", {
  method: "POST",
  body: formData,
});

const data = await res.json();
console.log(data.ischemia, data.dangerous_arrhythmia, data.summary);
```