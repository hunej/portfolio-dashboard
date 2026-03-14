# 📊 Portfolio Dashboard

一個視覺化股票投資組合管理工具，支援：
- **📋 List View**：管理股票清單、撰寫投資論述、建立股票間關聯
- **🫧 Bubble Map**：以氣泡圖呈現持股，氣泡大小 = 市值，位置 = 股價相關性
- 
---

## 🚀 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 啟動服務

```bash
cd src
uvicorn main:app --reload --port 8000
```

### 3. 開啟瀏覽器

前往 `http://localhost:8000`

---

## 📁 專案結構

```
portfolio-dashboard/
├── src/
│   ├── main.py           # FastAPI 後端 API
│   ├── script.py         # 自動填充股票資訊（GICS、名稱）
│   └── bubble_data.py    # 產生 Bubble Map 資料（相關性計算）
├── static/
│   ├── index.html        # 前端介面
│   ├── gics.js           # GICS 產業分類資料
│   └── bubble_data.json  # Bubble Map 預計算資料
├── data/
│   └── graph.json        # 你的投資組合資料（nodes + links）
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 📝 使用說明

### List View — 管理股票清單

1. **新增股票**：點擊左下角 `+ Add Ticker`，輸入股票代號（如 `AAPL`）
2. **編輯資訊**：點選股票後，在右側面板編輯：
   - **Rating**：`BUY` / `WATCH` / `HOLDING` / `TODO` / `AVOID`
   - **Tags**：自訂標籤，如 `ai`, `dividend`, `growth`
   - **Thesis**：撰寫投資論述、催化劑、風險
3. **建立關聯**：展開下方 `Edges` 面板，點擊 `+ Add Edge` 建立股票間關係
   - 關係類型：`peer`（同業）、`supply_chain`（供應鏈）、`pair_trade`、`theme`

### Bubble Map — 視覺化分析

點擊上方 `🫧 Bubble Map` 頁籤，即可看到：
- **氣泡大小**：市值（Market Cap）
- **氣泡位置**：股價相關性（90日 Pearson 相關係數 + MDS 降維）
- **氣泡顏色**：可切換 `Rating` 或 `週報酬熱力圖`

> 💡 首次使用需先產生 Bubble Map 資料：
> ```bash
> cd src
> python bubble_data.py
> ```

---

## 📊 資料格式說明

### `data/graph.json` — 你的投資組合

```json
{
  "nodes": [
    {
      "id": "AAPL",
      "ticker": "AAPL",
      "name": "Apple Inc.",
      "gicsSector": "Information Technology",
      "gicsIndustry": "Technology Hardware, Storage & Peripherals",
      "rating": "HOLDING",
      "note": {
        "thesis": "iPhone + Services 生態系，定價權強...",
        "tags": ["big-tech", "hardware", "services"]
      },
      "createdAt": "2026-02-28T01:00:00Z",
      "updatedAt": "2026-03-02T11:45:30Z"
    }
  ],
  "links": [
    {
      "id": 1,
      "source": "AAPL",
      "target": "TSM",
      "relation": "supply_chain",
      "comment": "台積電是蘋果主要晶片代工廠"
    }
  ],
  "_linkIdCounter": 1
}
```

### Node 欄位說明

| 欄位 | 說明 | 範例 |
|------|------|------|
| `ticker` | 股票代號 | `AAPL` |
| `name` | 公司名稱 | `Apple Inc.` |
| `gicsSector` | GICS 產業分類 | `Information Technology` |
| `gicsIndustry` | GICS 細分產業 | `Technology Hardware...` |
| `rating` | 評級 | `BUY` / `WATCH` / `HOLDING` / `TODO` / `AVOID` |
| `note.thesis` | 投資論述 | 自由文字 |
| `note.tags` | 標籤 | `["ai", "dividend"]` |

### Link 欄位說明

| 欄位 | 說明 | 範例 |
|------|------|------|
| `source` | 來源股票 | `AAPL` |
| `target` | 目標股票 | `TSM` |
| `relation` | 關係類型 | `peer` / `supply_chain` / `pair_trade` / `theme` |
| `comment` | 備註 | `台積電是蘋果主要晶片代工廠` |

---

## 🔌 API 端點

| Method | Path | 說明 |
|--------|------|------|
| `GET` | `/graph` | 取得完整資料 |
| `GET` | `/node/{ticker}` | 取得單一股票 |
| `PUT` | `/node/{ticker}` | 新增/更新股票 |
| `DELETE` | `/node/{ticker}` | 刪除股票 |
| `GET` | `/links?ticker=AAPL` | 取得關聯 |
| `POST` | `/link` | 新增關聯 |
| `DELETE` | `/link/{id}` | 刪除關聯 |
| `GET` | `/bubble` | 取得 Bubble Map 資料 |

---

## ⌨️ 快捷鍵

| 快捷鍵 | 功能 |
|--------|------|
| `Ctrl/Cmd + S` | 儲存目前編輯 |
| `Esc` | 關閉彈出視窗 |
| `Tab` | 在 Thesis 欄位插入縮排 |

---

## 🛠️ 進階設定

### 自動填充股票資訊

新增股票後，可執行以下指令自動填充公司名稱和 GICS 分類：

```bash
cd src
python script.py
```

### 更新 Bubble Map 資料

Bubble Map 的位置資料是預計算的，建議每週執行一次：

```bash
cd src
python bubble_data.py
```

### 遠端存取（Cloudflare Tunnel）

```bash
cloudflared tunnel --url http://localhost:8000
```

---

## 📄 License

MIT License — 歡迎自由使用與修改。

---

## 🙏 致謝

- [TradingView Widget](https://www.tradingview.com/widget/) — 即時股價圖表
- [yfinance](https://github.com/ranaroussi/yfinance) — 股票資料取得
- [scikit-learn](https://scikit-learn.org/) — MDS 降維演算法
