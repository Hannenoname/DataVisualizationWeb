# Phân Tích Dữ Liệu Kinh Tế

Ứng dụng web phân tích và trực quan hóa các chỉ số kinh tế quan trọng của Việt Nam.

## Tính năng

- Phân tích đa chỉ số kinh tế (Core Inflation, Food Inflation, USD/VND, Brent Oil)
- Nhiều loại biểu đồ phân tích (đường, tương quan, theo mùa, xu hướng)
- Giải thích chi tiết về ý nghĩa của các chỉ số và mối quan hệ
- Giao diện người dùng thân thiện, dễ sử dụng
- Responsive design cho mọi thiết bị

## Cài đặt

1. Clone repository:
```bash
git clone <repository-url>
cd EconomicDataAnalyzer
```

2. Tạo môi trường ảo và kích hoạt:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## Chạy ứng dụng

1. Chạy ứng dụng Streamlit:
```bash
streamlit run src/app.py
```

2. Mở trình duyệt và truy cập:
```
http://localhost:8501
```

## Cấu trúc thư mục

```
EconomicDataAnalyzer/
├── src/
│   ├── core/
│   │   ├── data_handler.py     # Xử lý dữ liệu
│   │   └── visualization_handler.py  # Tạo biểu đồ
│   └── app.py                  # Ứng dụng chính
├── static/
│   ├── css/
│   │   └── styles.css         # Styles
│   └── data/
│       └── economic_data.csv  # Dữ liệu
├── requirements.txt           # Dependencies
└── README.md                 # Hướng dẫn
```

## Sử dụng

1. Chọn chỉ số kinh tế muốn phân tích từ panel bên trái
2. Chọn loại biểu đồ phù hợp từ panel bên phải
3. Xem biểu đồ và giải thích chi tiết ở phần chính
4. Tương tác với biểu đồ để xem thông tin chi tiết

## Yêu cầu hệ thống

- Python 3.8+
- Các thư viện trong requirements.txt
- Trình duyệt web hiện đại (Chrome, Firefox, Safari) 