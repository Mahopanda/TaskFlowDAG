"""
操作 Dict 的範例
----------------
這個腳本展示了如何使用 TaskFlowDag 中的 Dag 模組操作字典。
透過定義數個節點，對給定的字典進行特定的操作，並返回操作後的結果。
"""

from dag_module.dag import Dag

# 初始化範例資料
data = {
    'numbers': [1, 2, 3, 4, 5],
    'details': {
        'name': 'Sample',
        'attributes': ['a', 'b', 'c']
    }
}

dag = Dag()

# 定義處理字典的函式

@dag.node
def add_ten(input_data):
    """對 'numbers' 列表中的每個數字加10。"""
    data = input_data if isinstance(input_data, dict) else input_data[0]
    data['numbers'] = [x + 10 for x in data['numbers']]
    return data

@dag.node
def change_name(input_data):
    """修改 'details' 中的 'name'。"""
    data = input_data if isinstance(input_data, dict) else input_data[0]
    data['details']['name'] = 'Modified Sample'
    return data

@dag.node
def reverse_attributes(input_data):
    """反轉 'details' 中的 'attributes' 列表。"""
    data = input_data if isinstance(input_data, dict) else input_data[0]
    data['details']['attributes'] = data['details']['attributes'][::-1]
    return data

# 定義 DAG 的流程
add_ten >> change_name >> reverse_attributes

# 使用 DAG 執行上述定義的函式，並輸出結果
result_data = dag.infer(data)

print(result_data)

"""
{
    "add_ten": {
        "numbers": [11, 12, 13, 14, 15],
        "details": {"name": "Modified Sample", "attributes": ["c", "b", "a"]},
    },
    "change_name": {
        "numbers": [11, 12, 13, 14, 15],
        "details": {"name": "Modified Sample", "attributes": ["c", "b", "a"]},
    },
    "reverse_attributes": {
        "numbers": [11, 12, 13, 14, 15],
        "details": {"name": "Modified Sample", "attributes": ["c", "b", "a"]},
    },
}
"""

dag.visualize(render=True)  # 這會生成 DAG 的圖形表示，幫助使用者理解節點之間的關係。

