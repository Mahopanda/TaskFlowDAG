import pandas as pd
from dag_module.dag import Dag

# 創建DAG實例
dag = Dag()

# 定義初始化DataFrame
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
})

def process_df(input_data, df=None):
    """
    輔助函式：對輸入數據進行預處理，確保其為DataFrame格式。
    
    Parameters:
    - input_data: 輸入數據，可以是DataFrame或其他格式
    - df (optional): 提供一個既有的DataFrame，預設為None
    
    Returns:
    - DataFrame
    """
    if df is None:
        df = input_data if isinstance(input_data, pd.DataFrame) else input_data[0]
    return df

@dag.node
def add_column(input_data):
    """
    定義一個新增列的DAG節點，此節點新增一列D，其值為A和B的和。
    
    Parameters:
    - input_data: 輸入的DataFrame
    
    Returns:
    - DataFrame: 更新後的DataFrame
    """
    df = process_df(input_data)
    df['D'] = df['A'] + df['B']
    return df

@dag.node
def multiply_column(input_data):
    """
    定義一個乘法列的DAG節點，此節點新增一列E，其值為D列的值乘以2。
    
    Parameters:
    - input_data: 輸入的DataFrame
    
    Returns:
    - DataFrame: 更新後的DataFrame
    """
    df = process_df(input_data)
    df['E'] = df['D'] * 2
    return df

@dag.node
def drop_column(input_data):
    """
    定義一個刪除列的DAG節點，此節點刪除A和B兩列。
    
    Parameters:
    - input_data: 輸入的DataFrame
    
    Returns:
    - DataFrame: 更新後的DataFrame
    """
    df = process_df(input_data)
    df = df.drop(columns=['A', 'B'])
    return df

# 定義DAG的結構
add_column >> multiply_column >> drop_column

# 使用DAG執行並處理DataFrame
result_df = dag.infer(df)
print(result_df)

# 可選：顯示DAG的視覺化結構
dag.visualize(render=True)
