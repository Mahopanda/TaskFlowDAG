"""
多分支範例
----------------------
這個腳本展示了如何使用TaskFlowDag的DAG模塊進行多重分支決策。
從一個包含姓名、年齡和工作的dataframe開始，基於年齡和工作進行分類，並輸出結果。
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
    """基於年齡的均值進行分組"""
    if dataframe['age'].mean() > 30:
        return dataframe, 'older_group'
    else:
        return dataframe, 'younger_group'

@dag.decision
def filter_job(dataframe):
    """確定是否有工程師在數據中"""
    if dataframe['job'].str.contains('Engineer').any():
        return dataframe, 'engineer_present'
    else:
        return dataframe, 'no_engineer'

@dag.node
def older_group(dataframe):
    """設置組別為'older'"""
    dataframe['group'] = 'older'
    return dataframe

@dag.node
def younger_group(dataframe):
    """設置組別為'younger'"""
    dataframe['group'] = 'younger'
    return dataframe

@dag.node
def engineer_present(dataframe):
    """設置工程師狀態為'present'"""
    dataframe['engineer_status'] = 'present'
    return dataframe

@dag.node
def no_engineer(dataframe):
    """設置工程師狀態為'absent'"""
    dataframe['engineer_status'] = 'absent'
    return dataframe

@dag.node
def finalize(dataframe):
    """總結數據框的結果"""
    avg_age = dataframe['age'].mean()
    group = dataframe['group'].iloc[0]
    eng_status = dataframe['engineer_status'].iloc[0]
    return f"Average age: {avg_age}, Group: {group}, Engineer status: {eng_status}"

# 定義DAG的流程
extract_data >> filter_age
filter_age >> older_group >> filter_job
filter_age >> younger_group >> filter_job
filter_job >> engineer_present >> finalize
filter_job >> no_engineer >> finalize

# 更新分支映射
dag.update_branch_map('filter_age', 'older_group', 'younger_group')
dag.update_branch_map('filter_job', 'engineer_present', 'no_engineer')

# 執行DAG並輸出結果
result = dag.infer(df)
print(result)

"""
Node extract_data result:       name  age       job
0    Alice   25  Engineer
1      Bob   15   Student
2  Charlie   35    Doctor
3    David   50   Teacher
Node older_group result:       name  age       job  group
0    Alice   25  Engineer  older
1      Bob   15   Student  older
2  Charlie   35    Doctor  older
3    David   50   Teacher  older
Node engineer_present result:       name  age       job  group engineer_status
0    Alice   25  Engineer  older         present
1      Bob   15   Student  older         present
2  Charlie   35    Doctor  older         present
3    David   50   Teacher  older         present
Node finalize result: Average age: 31.25, Group: older, Engineer status: present
{'extract_data':       name  age       job  group engineer_status
0    Alice   25  Engineer  older         present
1      Bob   15   Student  older         present
2  Charlie   35    Doctor  older         present
3    David   50   Teacher  older         present, 'filter_age':       name  age       job  group engineer_status
0    Alice   25  Engineer  older         present
1      Bob   15   Student  older         present
2  Charlie   35    Doctor  older         present
3    David   50   Teacher  older         present, 'filter_job':       name  age       job  group engineer_status
0    Alice   25  Engineer  older         present
1      Bob   15   Student  older         present
2  Charlie   35    Doctor  older         present
3    David   50   Teacher  older         present, 'older_group':       name  age       job  group engineer_status
0    Alice   25  Engineer  older         present
1      Bob   15   Student  older         present
2  Charlie   35    Doctor  older         present
3    David   50   Teacher  older         present, 'engineer_present':       name  age       job  group engineer_status
0    Alice   25  Engineer  older         present
1      Bob   15   Student  older         present
2  Charlie   35    Doctor  older         present
3    David   50   Teacher  older         present, 'finalize': 'Average age: 31.25, Group: older, Engineer status: present'}
"""


# 生成DAG結構視覺化圖
dag.visualize(render=True)
