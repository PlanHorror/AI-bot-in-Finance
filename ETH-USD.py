import yfinance as yf

# Tải dữ liệu lịch sử ETH/USD
eth_data = yf.download('ETH-USD', start='2023-01-01')
eth_data.columns = eth_data.columns.droplevel(1)

# Xuất dữ liệu ra CSV
eth_data.to_csv('eth_usd_data.csv')

# Hiển thị một phần dữ liệu
print(eth_data.head())
