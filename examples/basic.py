"""
TaskFlowDag 的基本示範
----------------------
此腳本展示了使用 TaskFlowDag 中的 Dag 模組的簡單用例。
它建立了一個包含多個節點的 Dag，然後推斷出結果。
"""
from collections.abc import Sequence
from dag_module.dag import Dag

# 啟用調試模式初始化 Dag
dag = Dag(debug=True)

@dag.node
def increment_input(x):
    """增加輸入值。如果輸入是列表，則增加第一個元素。"""
    return x[0] + 1 if isinstance(x, list) else x + 1

@dag.node
def add_two(x):
    """對輸入增加2。如果輸入是序列，則加總其元素。"""
    x = sum(x) if isinstance(x, Sequence) else x
    return x + 2

@dag.node
def add_three(x):
    """對輸入增加3。如果輸入是序列，則加總其元素。"""
    x = sum(x) if isinstance(x, Sequence) else x
    return x + 3

@dag.node
def sum_and_add_four(inputs):
    """加總輸入然後增加4。"""
    return sum(inputs) + 4

@dag.node
def add_five(x):
    """對輸入增加5。如果輸入是序列，則加總其元素。"""
    x = sum(x) if isinstance(x, Sequence) else x
    return x + 5

@dag.node
def end_node(x):
    """結束節點，僅返回其輸入。"""
    return x

# 定義 DAG 的流程
increment_input >> add_two >> sum_and_add_four >> add_five >> end_node
increment_input >> add_three >> sum_and_add_four >> add_five

# 以初始輸入1推斷 DAG 的結果
result = dag.infer(1)
print(f"最終結果: {result}")


"""
Node increment_input result: 2
Node add_two result: 4
Node add_three result: 5
Node sum_and_add_four result: 13
Node add_five result: 18
Node end_node result: 18
Final Result: {'increment_input': 2, 'add_two': 4, 'add_three': 5, 'sum_and_add_four': 13, 'add_five': 18, 'end_node': 18}
"""

# 生成 DAG 圖
dag.visualize(render=True)