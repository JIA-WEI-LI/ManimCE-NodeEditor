<!-- Language Switch -->
<p align="right">
  🌐 <strong>語言：</strong>
  <a href="./README.md">English</a> &nbsp;| &nbsp; 
  <a href="./README.zh-TW.md">繁體中文</a>
</p>

# ManimCE Node Editor — 視覺化動畫製作工具

[![Version](https://img.shields.io/badge/version-v0.2.0.dev9-orange)](#)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](#)
[![Qt](https://img.shields.io/badge/Qt-PyQt5-blue)](#)
[![License](https://img.shields.io/github/license/JIA-WEI-LI/ManimCE-NodeEditor?color=blue)](./LICENSE)
![Size](https://img.shields.io/github/repo-size/JIA-WEI-LI/ManimCE-NodeEditor?color)

[![Development](https://img.shields.io/badge/status-in%20development-yellow)](#)
[![GitHub issues](https://img.shields.io/github/issues/JIA-WEI-LI/ManimCE-NodeEditor)](https://github.com/JIA-WEI-LI/ManimCE-NodeEditor/issues)

一款基於 PyQt5 的視覺化節點編輯器，設計目的是為了**簡化 ManimCE 動畫影片的創作流程**。此工具提供直覺的節點式操作介面，協助使用者建立動畫邏輯，減少對 Manim 原始程式碼的依賴。

> [!WARNING]
> 此專案仍在開發階段，目前尚未完成

---

## 📈 專案目標與里程碑

### ✅ 當前進度

| 里程碑                                              | 進度     |
|-----------------------------------------------------|----------|
| 1. 基礎節點編輯器功能                               | ✅ 100%     |
| 2. 進階節點功能擴充                                 | ✅ 100%   |
| 3. 編輯器打包功能                                   | ❌ 0%       |
| 4. 嵌入其他視窗的整合介面                           | ❌ 0%       |
| 5. 節點編輯器功能完善                               | ❌ 0%       |
| 6. 支援多種 UI 主題樣式                             | ❌ 0%       |
| 7. 與 ManimCE 的基本邏輯整合                        | ❌ 0%       |
| 8. 與 ManimCE 的進階邏輯整合                        | ❌ 0%       |
| 9. 導出為獨立應用程式（EXE / APP）                  | ❌ 0%       |
| 10. 雙語教學網站與文件建置                          | ❌ 0%       |

---

## 🚀 主要特色

- 模組化架構，清楚區分核心邏輯、圖形與 UI 元件  
- 使用顏色區分的 Socket 類型，連接更直覺  
- 支援貝茲曲線與直線的平滑邊線渲染  
- 節點移動時會即時更新邊線  
- 可自訂的日誌系統，支援終端與檔案輸出  

---

## 💼 技術架構

- Python 3.12+
- PyQt5 (>= 5.15.9)
- ManimCE（整合中）
- QGraphicsScene / QGraphicsView 架構
- 自訂的序列化 / 反序列化系統

<!-- ## 📺 快速開始
```bash
git clone https://github.com/Magicsoldier19/manimce-node-editor.git
cd manimce-node-editor
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python NodeEditor/node_editor_main.py
``` -->

---

## 🎓 學習資源

官方教學網站建置中，預計提供以下內容：

- 雙語教學（英文與繁體中文）
- 教學影片與互動範例
- 自訂主題與元件擴充說明文件

---

## 🔼 未來功能計畫

### UI / UX 強化
- 主題切換
- 節點右鍵選單
- 拖曳建立節點

### 功能擴充
- 編輯歷史（Undo/Redo）
- 複製貼上節點與子圖
- 專案儲存與載入（JSON）

### 導出功能
- 將節點圖轉換為 ManimCE Python 代碼
- 內建動畫預覽器
- 可直接導出 `.py` 與影片檔

---

## 🔻 發佈節奏與標籤

- `v0.0.1` ：🎯 完成基本節點編輯功能  
- `v0.0.2` ：🔁 完善進階邏輯、邊線與序列化  

### 📦 當前版本
**`v0.0.2.dev9`** – 持續開發中  

---

## 📄 授權

本專案採用 [MIT License](./LICENSE)
