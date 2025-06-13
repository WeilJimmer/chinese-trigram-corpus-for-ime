import os
import pickle
from collections import defaultdict
from typing import Dict, List, Optional, Set

class Node:
    def __init__(self):
        self.children: Dict[str, Node] = {}
        self.score: int = 0
    def add_child(self, char: str) -> 'Node':
        if char not in self.children:
            self.children[char] = Node()
        return self.children[char]
    def get_child(self, char: str) -> Optional['Node']:
        return self.children.get(char)
    def get_children(self) -> List['Node']:
        return list(self.children.values())
    def get_self_score(self) -> int:
        return self.score
    def set_score(self, score: int):
        self.score = score
    def get_children_keys(self) -> List[str]:
        return list(self.children.keys())
    def get_ordered_children_keys(self) -> List[str]:
        """返回按照子節點分數降序排序的字符列表"""
        return [k for k, v in sorted(self.children.items(),key=lambda item: item[1].score,reverse=True)]

def build_tree_from_files(input_dir: str, min_score: int = 100) -> Node:
    """從多個文件建立字典樹"""
    print(f"開始建立字典樹，最小分數閾值: {min_score}")
    root = Node()
    file_count = 0
    entry_count = 0
    valid_entry_count = 0
    # 獲取所有輸出文件
    files = [f for f in os.listdir(input_dir) if f.startswith("output_") and f.endswith(".txt")]
    total_files = len(files)

    for filename in sorted(files):
        file_path = os.path.join(input_dir, filename)
        file_count += 1
        if file_count % 20 == 0:
            print(f"處理文件 {file_count}/{total_files}: {filename}")
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                entry_count += 1
                # 解析每行數據
                try:
                    path, freq_str = line.strip().split('\t')
                    freq = int(freq_str)
                    # 只處理分數大於閾值的項
                    if freq < min_score:
                        continue
                    valid_entry_count += 1
                    # 將路徑添加到樹中
                    current = root
                    for char in path:
                        current = current.add_child(char)
                    # 設置葉子節點的分數
                    current.set_score(freq)
                except ValueError:
                    print(f"警告: 跳過格式不正確的行: {line.strip()}")
    print(f"處理完成! 共處理 {file_count} 個文件, {entry_count} 條記錄, 有效記錄 {valid_entry_count} 條")
    return root

def calculate_node_scores(node: Node) -> int:
    """計算每個節點的分數 (子節點分數之和)"""
    if not node.children:
        return node.score
    total_score = 0
    for child in node.children.values():
        child_score = calculate_node_scores(child)
        total_score += child_score
    # 如果節點已經有分數（葉子節點），保留原有分數
    if node.score == 0:
        node.set_score(total_score)
    else:
        # 葉子節點的分數已經在建樹時設置，這裡加上子節點分數
        node.set_score(node.score + total_score)
    return node.score

def save_tree_to_binary(root: Node, output_file: str):
    """將樹保存為二進制文件"""
    with open(output_file, 'wb') as f:
        pickle.dump(root, f)
    print(f"樹已保存到: {output_file}")

def load_tree_from_binary(input_file: str) -> Node:
    """從二進制文件載入樹"""
    with open(input_file, 'rb') as f:
        root = pickle.load(f)
    return root

def test_tree(root: Node, test_words: List[str]):
    """測試樹的功能"""
    print("\n===== 測試樹結構 =====")
    print(f"根節點分數: {root.get_self_score()}")
    print(f"根節點子節點數: {len(root.get_children_keys())}")
    print(f"根節點前10個子節點: {root.get_ordered_children_keys()[:10]}")
    # 測試特定路徑
    for word in test_words:
        current = root
        path_exists = True
        for char in word:
            if current is None or not current.get_child(char):
                path_exists = False
                break
            current = current.get_child(char)
        if path_exists and current!=None:
            print(f"路徑 '{word}' 存在，分數: {current.get_self_score()}")
            next_chars = current.get_ordered_children_keys()[:5]
            if next_chars:
                print(f"  '{word}' 後可能的字符 (前5): {next_chars}")
        else:
            print(f"路徑 '{word}' 不存在")

def print_tree_stats(root: Node):
    """打印樹的統計信息"""
    total_nodes = [0]
    max_depth = [0]
    unique_chars = set()
    def dfs(node, depth):
        total_nodes[0] += 1
        max_depth[0] = max(max_depth[0], depth)
        for char, child in node.children.items():
            unique_chars.add(char)
            dfs(child, depth + 1)
    dfs(root, 0)
    print("\n===== 樹統計信息 =====")
    print(f"總節點數: {total_nodes[0]}")
    print(f"最大深度: {max_depth[0]}")
    print(f"唯一字符數: {len(unique_chars)}")
    print(f"根節點分數: {root.get_self_score()}")
    # 顯示分數最高的前10個一級路徑
    top_paths = [(char, child.get_self_score()) for char, child in root.children.items()]
    top_paths.sort(key=lambda x: x[1], reverse=True)
    print("\n分數最高的前10個一級路徑:")
    for char, score in top_paths[:10]:
        print(f"'{char}': {score}")

def main():
    input_dir = "trigram_output"  # 包含所有output_xxx.txt的目錄
    output_file = "trigram_tree.bin"  # 輸出的二進制文件
    min_score = 100  # 最小分數閾值
    if not os.path.exists(output_file):
        # 建立樹
        root = build_tree_from_files(input_dir, min_score)
        # 計算節點分數
        print("計算節點分數...")
        root_score = calculate_node_scores(root)
        print(f"樹根總分數: {root_score}")
        # 保存樹
        save_tree_to_binary(root, output_file)
    else:
        print(f"樹已存在，從 {output_file} 載入...")
        root = load_tree_from_binary(output_file)
        print(f"載入的樹根分數: {root.get_self_score()}")
    # 打印樹的統計信息
    print_tree_stats(root)
    # 測試樹
    test_words = ["男", "女", "你", "你好", "我是", "天氣", "臺灣", "程式", "設計"]
    test_tree(root, test_words)
    # 測試一些查詢
    print("\n===== 測試查詢 =====")
    current = root
    if current.get_child("我"):
        current = current.get_child("我")
        if current!=None:
            print(f"'我' 的分數: {current.get_self_score()}")
            print(f"'我' 後可能的字符 (前10): {current.get_ordered_children_keys()[:10]}")

if __name__ == "__main__":
    main()