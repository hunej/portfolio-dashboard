#!/usr/bin/env python3
"""
自動填充股票資訊
================
從 yfinance 取得公司名稱和 GICS 分類，自動填入 graph.json
"""

import json
import yfinance as yf
from pathlib import Path
from datetime import datetime

# 路徑設定
DATA_PATH = Path(__file__).parent.parent / "data" / "graph.json"

# GICS Sector 對應（yfinance 的 sector 名稱可能略有不同）
SECTOR_MAP = {
    "Technology": "Information Technology",
    "Consumer Cyclical": "Consumer Discretionary",
    "Consumer Defensive": "Consumer Staples",
    "Healthcare": "Health Care",
    "Financial Services": "Financials",
    "Communication Services": "Communication Services",
    "Basic Materials": "Materials",
    "Industrials": "Industrials",
    "Energy": "Energy",
    "Utilities": "Utilities",
    "Real Estate": "Real Estate",
}


def load_graph():
    """載入 graph.json"""
    if DATA_PATH.exists():
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"nodes": [], "links": [], "_linkIdCounter": 0}


def save_graph(data):
    """儲存 graph.json"""
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def fetch_stock_info(ticker: str) -> dict:
    """從 yfinance 取得股票資訊"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # 取得 sector 並轉換
        raw_sector = info.get('sector', '')
        sector = SECTOR_MAP.get(raw_sector, raw_sector)
        
        return {
            'name': info.get('shortName') or info.get('longName', ''),
            'sector': sector,
            'industry': info.get('industry', ''),
        }
    except Exception as e:
        print(f"  ⚠️ 無法取得 {ticker} 資訊: {e}")
        return {}


def process_data(input_data):
    # Placeholder function for processing input data
    processed_data = input_data  # Replace with actual processing logic
    return processed_data

def save_processed_data(output_file, data):
    with open(output_file, 'w') as file:
        file.write(data)

def auto_fill():
    """自動填充缺少資訊的股票"""
    print("=" * 50)
    print("📊 自動填充股票資訊")
    print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    graph = load_graph()
    nodes = graph.get('nodes', [])
    
    if not nodes:
        print("❌ 沒有股票資料")
        return
    
    updated_count = 0
    
    for node in nodes:
        ticker = node.get('ticker', '')
        if not ticker:
            continue
        
        # 檢查是否需要填充
        needs_update = (
            not node.get('name') or
            not node.get('gicsSector') or
            not node.get('gicsIndustry')
        )
        
        if not needs_update:
            print(f"✓ {ticker}: 資料完整，跳過")
            continue
        
        print(f"🔄 {ticker}: 正在取得資訊...")
        info = fetch_stock_info(ticker)
        
        if not info:
            continue
        
        # 填充缺少的欄位
        if not node.get('name') and info.get('name'):
            node['name'] = info['name']
            print(f"   → 名稱: {info['name']}")
        
        if not node.get('gicsSector') and info.get('sector'):
            node['gicsSector'] = info['sector']
            print(f"   → Sector: {info['sector']}")
        
        if not node.get('gicsIndustry') and info.get('industry'):
            node['gicsIndustry'] = info['industry']
            print(f"   → Industry: {info['industry']}")
        
        # 更新時間戳
        node['updatedAt'] = datetime.now().isoformat() + 'Z'
        updated_count += 1
    
    # 儲存
    save_graph(graph)
    
    print("-" * 50)
    print(f"✅ 完成！更新了 {updated_count} 檔股票")
    print(f"📁 已儲存: {DATA_PATH}")


def fill_all(force: bool = False):
    """
    填充所有股票資訊
    force=True 時會覆蓋現有資料
    """
    print("=" * 50)
    print("📊 填充所有股票資訊" + (" (強制覆蓋)" if force else ""))
    print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    graph = load_graph()
    nodes = graph.get('nodes', [])
    
    if not nodes:
        print("❌ 沒有股票資料")
        return
    
    updated_count = 0
    
    for node in nodes:
        ticker = node.get('ticker', '')
        if not ticker:
            continue
        
        print(f"🔄 {ticker}: 正在取得資訊...")
        info = fetch_stock_info(ticker)
        
        if not info:
            continue
        
        # 更新欄位
        if info.get('name') and (force or not node.get('name')):
            node['name'] = info['name']
        
        if info.get('sector') and (force or not node.get('gicsSector')):
            node['gicsSector'] = info['sector']
        
        if info.get('industry') and (force or not node.get('gicsIndustry')):
            node['gicsIndustry'] = info['industry']
        
        node['updatedAt'] = datetime.now().isoformat() + 'Z'
        updated_count += 1
        
        print(f"   ✓ {node.get('name', 'N/A')} | {node.get('gicsSector', 'N/A')}")
    
    save_graph(graph)
    
    print("-" * 50)
    print(f"✅ 完成！更新了 {updated_count} 檔股票")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--force':
        fill_all(force=True)
    else:
        auto_fill()

    input_data = "Sample data"  # Replace with actual data source
    processed_data = process_data(input_data)
    save_processed_data('output.txt', processed_data)