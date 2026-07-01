"""
通过新浪财经API获取医药ETF易方达(512010)历史交易数据并存储为CSV
"""
import requests
import pandas as pd
from datetime import datetime
import os

# 工作目录
WORK_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(WORK_DIR, "512010_医药ETF易方达.csv")

def fetch_etf_data():
    """从新浪财经获取512010的历史日K线数据"""
    url = "https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData"
    params = {
        "symbol": "sh512010",
        "scale": "240",  # 日线
        "ma": "no",
        "datalen": "250"  # 最近250个交易日（约一年）
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Referer": "https://finance.sina.com.cn"
    }

    print("正在从新浪财经获取医药ETF易方达(512010)历史数据...")
    resp = requests.get(url, params=params, headers=headers, timeout=15)
    resp.encoding = 'utf-8'
    data = resp.json()

    if not data:
        raise ValueError("未获取到任何数据")

    df = pd.DataFrame(data)

    # 转换列名和数据类型
    df = df.rename(columns={
        'day': '日期',
        'open': '开盘价',
        'high': '最高价',
        'low': '最低价',
        'close': '收盘价',
        'volume': '成交量'
    })

    df['日期'] = pd.to_datetime(df['日期'])

    # 过滤最近一年（2025-07-01 到 2026-07-01）
    cutoff = datetime(2025, 7, 1)
    df = df[df['日期'] >= cutoff].copy()

    # 转换数据类型
    for col in ['开盘价', '最高价', '最低价', '收盘价']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df['成交量'] = pd.to_numeric(df['成交量'], errors='coerce')

    # 按日期排序
    df = df.sort_values('日期').reset_index(drop=True)

    print(f"成功获取 {len(df)} 条交易记录")
    print(f"日期范围: {df['日期'].min().strftime('%Y-%m-%d')} 至 {df['日期'].max().strftime('%Y-%m-%d')}")
    print(f"\n前5行预览:")
    print(df.head().to_string())
    print(f"\n后5行预览:")
    print(df.tail().to_string())

    return df


def main():
    df = fetch_etf_data()
    df.to_csv(CSV_PATH, index=False, encoding='utf-8-sig')
    print(f"\n数据已保存至: {CSV_PATH}")
    print(f"文件大小: {os.path.getsize(CSV_PATH):,} bytes")


if __name__ == "__main__":
    main()
