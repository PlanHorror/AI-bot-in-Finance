import requests
import pandas as pd
from datetime import datetime

# Gửi yêu cầu tới API
url = "https://api.alternative.me/fng/?limit=0"
response = requests.get(url)
data = response.json()

# Tạo danh sách để lưu dữ liệu
dates = []
fng_values = []
fng_classes = []

# Lọc dữ liệu từ ngày 1/1/2023
for entry in data['data']:
    timestamp = int(entry['timestamp'])  # Unix timestamp
    date = datetime.utcfromtimestamp(timestamp)  # Chuyển đổi Unix timestamp thành datetime
    if date >= datetime(2023, 1, 1):
        dates.append(date.strftime('%d/%m/%Y'))
        fng_values.append(entry['value'])
        fng_classes.append(entry['value_classification'])

# Tạo DataFrame và xuất ra CSV
df = pd.DataFrame({
    'date': dates,
    'fng_value': fng_values,
    'fng_classification': fng_classes
})

# Xuất dữ liệu ra CSV
df.to_csv('fng_data_from_2023.csv', index=False)
