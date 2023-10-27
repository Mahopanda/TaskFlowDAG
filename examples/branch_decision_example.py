"""
分支範例
----------------------
這個腳本展示了如何使用TaskFlowDag的DAG模塊處理分支。
假設有一個CSV文件，我們的目的是從中提取資料，基於條件清洗它，然後儲存到不同的地方。
"""

import pandas as pd
from dag_module.dag import Dag

# 假設數據
data = {
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'age': [25, 15, 35, 50],
    'job': ['Engineer', 'Student', 'Doctor', 'Teacher']
}
df = pd.DataFrame(data)

dag = Dag(debug=True)

@dag.node
def extract_data(input_data):
    """提取數據"""
    return input_data

@dag.decision
def filter_age(dataframe):
    """基於年齡的均值過濾資料，並選擇後續操作"""
    if dataframe['age'].mean() > 30:
        return dataframe, 'transform_for_db'
    else:
        return dataframe, 'transform_for_api'

@dag.node
def transform_for_db(dataframe):
    """轉換資料以供數據庫使用"""
    dataframe['name'] = dataframe['name'].str.upper()
    return dataframe

@dag.node
def transform_for_api(dataframe):
    """轉換資料以供API使用"""
    dataframe['name'] = dataframe['name'].str.lower()
    return dataframe

@dag.node
def store_in_db(dataframe):
    """模擬存儲到數據庫的操作"""
    return "Stored in DB!"

@dag.node
def send_to_api(dataframe):
    """模擬發送到API的操作"""
    return "Sent to API!"

# 定義DAG的流程
extract_data >> filter_age
filter_age >> transform_for_db >> store_in_db
filter_age >> transform_for_api >> send_to_api

# 更新分支映射表
dag.update_branch_map('filter_age', 'transform_for_db', 'transform_for_api')

# 執行DAG並輸出結果
result = dag.infer(df)
print(result)

"""
Node extract_data result:       name  age       job
0    Alice   25  Engineer
1      Bob   15   Student
2  Charlie   35    Doctor
3    David   50   Teacher
Node transform_for_db result:       name  age       job
0    ALICE   25  Engineer
1      BOB   15   Student
2  CHARLIE   35    Doctor
3    DAVID   50   Teacher
Node store_in_db result: Stored in DB!
{'extract_data':       name  age       job
0    ALICE   25  Engineer
1      BOB   15   Student
2  CHARLIE   35    Doctor
3    DAVID   50   Teacher, 'filter_age':       name  age       job
0    ALICE   25  Engineer
1      BOB   15   Student
2  CHARLIE   35    Doctor
3    DAVID   50   Teacher, 'transform_for_db':       name  age       job
0    ALICE   25  Engineer
1      BOB   15   Student
2  CHARLIE   35    Doctor
3    DAVID   50   Teacher, 'store_in_db': 'Stored in DB!'}
"""
# 生成DAG結構視覺化圖
dag.visualize(render=True)
