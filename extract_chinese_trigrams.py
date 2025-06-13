import os
from collections import defaultdict

# 設定輸入與輸出
file_prefix = "wiki_0"
file_range = ["0t", "1t", "2t", "3t"]
files = [f"{file_prefix}{i}" for i in file_range]

# 輸出資料夾
output_dir = "trigram_output"
os.makedirs(output_dir, exist_ok=True)

# 建立 trigram 字典
trigram_freq = defaultdict(int)

# 中文判斷函數：只接受 \u4e00~\u9fff 範圍
def is_chinese_char(c):
    return '\u4e00' <= c <= '\u9fff'

# 處理所有檔案
for filename in files:
    print(f"讀取中: {filename}")
    with open(filename, "r", encoding="utf-8") as f:
        buffer = f.read()  # 一次讀入整個檔案

        length = len(buffer)
        for i in range(length - 2):
            c1, c2, c3 = buffer[i], buffer[i+1], buffer[i+2]
            if is_chinese_char(c1) and is_chinese_char(c2) and is_chinese_char(c3):
                trigram = c1 + c2 + c3
                trigram_freq[trigram] += 1
            if (i% 100000) == 0:
                print(f"處理到位置 {i} / {length} ({(i/length)*100:.2f}%)")
                print(f"當前 trigram 數量: {len(trigram_freq)}")

print(f"總 trigram 數量: {len(trigram_freq)}")

# 排序後分批寫入（每 10 萬筆存成一個檔案）
sorted_trigrams = sorted(trigram_freq.items(), key=lambda x: -x[1])

batch_size = 100_000
for i in range(0, len(sorted_trigrams), batch_size):
    batch = sorted_trigrams[i:i+batch_size]
    filename = os.path.join(output_dir, f"output_{i // batch_size:03d}.txt")
    print(f"寫入檔案: {filename}，包含 {len(batch)} 個 trigram")
    with open(filename, "w", encoding="utf-8") as f:
        for trigram, freq in batch:
            f.write(f"{trigram}\t{freq}\n")

print(f"輸出完成，共 {((len(sorted_trigrams) - 1) // batch_size) + 1} 個檔案。")
