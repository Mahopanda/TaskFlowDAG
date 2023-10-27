# TaskFlowDAG
TaskFlowDAG，靈感來自於 [world4jason](https://github.com/world4jason) 提出希望能將程式碼以DAG流程化、模組化管理的想法，基於這個概念開發了一個框架，讓開發者能夠以直觀的方式定義、組織和執行各種數據處理和計算任務的依賴關係。此框架的目標是簡化程式碼的管理，使問題的追踪和定位變得更加容易，並提供一個視覺化的工具來呈現整個流程，幫助開發者和新團隊成員更快速地瞭解和上手。

## 核心功能

1. **任務定義**：用戶可以使用裝飾器簡單地定義任務，並指定其輸入和輸出。此外，支援多種數據類型，如數值、列表、pandas DataFrame 和字典。
2. **流程設計**：開發者可以透過簡單的操作符（如`>>`）輕鬆定義任務之間的依賴關係，建立起完整的DAG流程。
3. **決策支援**：除了基本的計算任務外，此框架還支援決策節點，允許根據某些條件決定後續的執行路徑。
4. **可視化工具**：提供了一個`visualize()`方法，讓開發者和團隊成員可以直觀地查看整個DAG的結構，有助於問題的定位和流程的理解。
5. **Debug Mode**：使用者可以開啟調試模式，方便追踪和定位問題。


## 使用方法

## 安裝

請安裝需要的套件：

```bash
pip install -r requirements.txt
```


### 基本 DAG 流程範例
請參考 [basic.py](https://github.com/Mahopanda/TaskFlowDAG/blob/main/examples/basic.py)。

基本步驟為：

1. 定義你的 DAG。
2. 使用 @dag.node 裝飾器來標記每個節點函數。
3. 連接各個節點來建立你的 DAG。
4. 使用 dag.infer() 方法來執行 DAG。

![dag](https://github.com/Mahopanda/TaskFlowDAG/blob/main/images/dag.png)

---
### DataFrame DAG 流程範例
請參考 [df_dag_example.py]([https://github.com/Mahopanda/TaskFlowDAG/blob/main/examples/branch_decision_example.py](https://github.com/Mahopanda/TaskFlowDAG/blob/main/examples/df_dag_example.py))。

這個範例展示如何在 DAG 流程中使用 Pandas DataFrame。

![df_dag_example](https://github.com/Mahopanda/TaskFlowDAG/blob/main/images/df_dag_example.png)

---
### 操作字典的 DAG 範例
請參考 [dict_example.py](https://github.com/Mahopanda/TaskFlowDAG/blob/main/examples/dict_operations_example.py)。

基本步驟為：

1. 初始化你的 DAG 和輸入數據。
2. 使用 @dag.node 裝飾器來定義對字典的操作。
3. 連接各個節點，建立 DAG 的流程。
4. 使用 dag.infer() 方法來執行 DAG。

![dict_example](https://github.com/Mahopanda/TaskFlowDAG/blob/main/images/dict_example.png)

---
### 單一分支決策 DAG 範例
請參考 [branch_decision_example.py](https://github.com/Mahopanda/TaskFlowDAG/blob/main/examples/branch_decision_example.py)。

此範例教學：

1. 初始化你的 DAG 和輸入的 DataFrame。
2. 使用 @dag.node 和 @dag.decision 裝飾器來定義節點和決策。
3. 根據條件創建分支，並連接相應的節點。
4. 更新 DAG 的分支映射。
5. 使用 dag.infer() 方法執行 DAG。

![branch_decision_example](https://github.com/Mahopanda/TaskFlowDAG/blob/main/images/branch_decision_example.png)

---
### 多重分支決策 DAG 範例
請參考 [multi_branch_decision_example.py](https://github.com/Mahopanda/TaskFlowDAG/blob/main/examples/multi_branch_decision_example.py)。

此範例展示：

1. 初始化你的 DAG 和輸入的 DataFrame。
2. 使用 @dag.node 和 @dag.decision 裝飾器來定義多個節點和決策。
3. 在多個條件基礎上創建分支，並連接相應的節點。
4. 更新 DAG 的分支映射，確保正確的分支流程。
5. 使用 dag.infer() 方法執行 DAG。

![multi_branch_decision_example](https://github.com/Mahopanda/TaskFlowDAG/blob/main/images/multi_branch_decision_example.png)
