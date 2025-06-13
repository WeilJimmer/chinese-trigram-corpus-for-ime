# Chinese Trigram Corpus for IME 中文輸入法用三字詞語料庫

[English](#english) | [中文](#中文)

## 中文

### 專案簡介
本專案提供一份高品質的中文三字詞（Trigram）語料庫，專為中文輸入法（IME）開發設計。語料來源為中文維基百科，處理後適用於如注音輸入鍵盤等中文輸入法系統。

---

### 資料來源與處理方式
- **原始資料**：`zhwiki-latest-pages-articles.xml.bz2`（2025 年 6 月 1 日版本，約 3.1GB）
- **處理範圍**：擷取前 1200 MiB 的文章內容
- **字體轉換**：使用 [OpenCC](https://github.com/BYVoid/OpenCC) 將簡體中文轉換為台灣正體中文
- **字符範圍**：僅保留 Unicode 範圍 `\u4e00` 至 `\u9fff` 的中文字元
- **輸出格式**：共產生 356 個檔案（`output_000.txt` ~ `output_355.txt`），每檔含 10 萬筆 trigram 頻率資料

---

### 語料統計
- **總 trigram 數量**：35,539,139 條（約 3.55 億筆字元組合）
- **檔案數量**：356 個 `.txt` 檔案
- **排序方式**：依照頻率由高至低排序
- **檔案格式**：每行為 `trigram<tab>頻率` 格式

#### 範例格式

```
四個出	128
西亞海	128
首示眾	128
及江蘇	128
生中有	128
```

---

### 適用場景
- 中文輸入法候選詞預測
- 中文文本自動補全
- 中文語言模型訓練（如統計式或神經網路模型）

---

### 安裝與使用
1. 下載所需的 trigram 資料檔案
2. 根據應用場景選擇適當的頻率閾值篩選
3. 將資料整合至你的輸入法或自然語言處理系統中

---

### 處理腳本
本專案附有完整處理流程腳本 `extract_chinese_trigrams.py`，支援以下用途：
- 重現整體資料處理流程
- 調整參數以配合不同應用需求
- 處理其他中文語料來源

---

### 授權協議
本專案採用 **BSD 3-Clause License**，允許自由使用、修改與再散佈。

---

### 相關專案
- [ChineseInputKeyboardVRApp](https://github.com/WeilJimmer/ChineseInputKeyboardVRApp)：中文注音輸入法

---

### 致謝
感謝維基百科社群提供開放的中文語料資源。

---

## English

### Project Overview
This project provides a high-quality Chinese trigram corpus designed specifically for Input Method Editor (IME) development. The corpus is extracted from the Chinese version of Wikipedia and processed for use in systems such as the Zhuyin (Bopomofo) Input Keyboard App.

---

### Data Source and Processing
- **Source**: `zhwiki-latest-pages-articles.xml.bz2` (June 1, 2025 version, ~3.1GB)
- **Scope**: Extracted the first 1200 MiB of article content
- **Conversion**: Used [OpenCC](https://github.com/BYVoid/OpenCC) to convert Simplified Chinese into Traditional Chinese (Taiwan variant)
- **Character Filtering**: Only includes Chinese characters within Unicode range `\u4e00` to `\u9fff`
- **Output**: 356 files (`output_000.txt` to `output_355.txt`), each containing 100,000 trigrams

---

### Corpus Statistics
- **Total Trigrams**: 35,539,139 entries (~355 million character sequences)
- **File Count**: 356 `.txt` files
- **Sorting**: Sorted in descending order of frequency
- **Format**: Each line is formatted as `trigram<tab>frequency`

#### Example Format

```
四個出	128
西亞海	128
首示眾	128
及江蘇	128
生中有	128
```


---

### Use Cases
- Chinese IME candidate suggestion
- Chinese auto-completion
- Training character-level language models

---

### Installation & Usage
1. Download the trigram dataset files
2. Optionally filter by frequency thresholds as needed
3. Integrate into your IME or NLP pipeline

---

### Processing Script
This project includes a full preprocessing script: `extract_chinese_trigrams.py`, which enables you to:
- Reproduce the entire pipeline
- Customize parameters for your use case
- Apply the same logic to other Chinese corpora

---

### License
This project is licensed under the **BSD 3-Clause License**, permitting use, modification, and redistribution.

---

### Related Projects
- [ChineseInputKeyboardVRApp](https://github.com/WeilJimmer/ChineseInputKeyboardVRApp) – Chinese Zhuyin Input Keyboard

---

### Acknowledgments
Special thanks to the Wikipedia community for providing open and accessible Chinese language data.
