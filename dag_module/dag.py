from typing import Callable, Dict, List, Union
from collections.abc import Sequence
from collections import defaultdict
from functools import wraps
import pandas as pd

class Node:
    def __init__(self, func, dag, name=None):
        self.function = func
        self.dag = dag
        self.name = name if name is not None else func.__name__
        self.dag.add_node(self.name, self.function)

    def __rshift__(self, other):
        """使用 >> 定義 DAG 的邊"""
        self.dag.add_edge(self.name, other.name)
        return other


class Dag:
    def __init__(self, debug=False):
        self.nodes = {}
        self.edges = {}
        self.start_node = None
        self.end_nodes = []
        self.last_added = None
        self.debug = debug
        self.branch_map = {}

    def node(self, func):
        """裝飾器用於將函數添加為 DAG 的節點"""
        return Node(func, self)
        
    
    def add_node(self, name, func):
        self.nodes[name] = func
        if self.start_node is None:
            self.start_node = name
        if name not in self.end_nodes:
            self.end_nodes.append(name)
        self.last_added = name
        return self


    def add_edge(self, source, destination):
        if source not in self.nodes or destination not in self.nodes:
            raise ValueError(f"Both source {source} and destination {destination} should exist as nodes.")
        self.edges.setdefault(source, []).append(destination)
        return self

    def __rshift__(self, other):
        if self.name not in self.dag.edges:
            self.dag.edges[self.name] = []
    
        self.dag.edges[self.name].append(other.name)
    
        # 將other.name添加到end_nodes
        if other.name not in self.dag.end_nodes:
            self.dag.end_nodes.append(other.name)
        # 確保源節點不是結束節點
        if self.name in self.dag.end_nodes:
            self.dag.end_nodes.remove(self.name)
    
        return other





    def update_branch_map(self, decision_node, true_branch, false_branch):
        """更新決策節點的映射"""
        self.branch_map[decision_node] = {
            True: true_branch,
            False: false_branch
        }
    
    def infer(self, input_value):
        if not self._is_dag():
            raise ValueError("The graph contains a cycle, so it's not a valid DAG.")
    
        visited = set()
        queue = [self.start_node]
        memory = {}
    
        while queue:
            node = queue.pop(0)
            visited.add(node)
    
            parents = self._get_parents(node)
    
            if isinstance(input_value, (int, float, str)) and node == self.start_node:
                memory[node] = self.nodes[node]([input_value])
            elif isinstance(input_value, (dict, pd.DataFrame)) and node == self.start_node:
                memory[node] = self.nodes[node](input_value)
            elif node in self.branch_map:  # 處理決策節點
                result, next_node_name = self.nodes[node](memory[self._get_one_parent(node)])
                memory[node] = result  # 更新記憶體中的值
                queue.append(next_node_name)
                continue
            else:
                # 僅從memory中已有的parent節點獲取結果
                parent_values = [memory[parent] for parent in parents if parent in memory]
                input_data = parent_values if len(parent_values) > 1 else parent_values[0]
                memory[node] = self.nodes[node](input_data)
    
            # 如果是debug模式，印出每個節點的結果
            if self.debug:
                print(f"Node {node} result: {memory[node]}")
    
            next_nodes = self.edges.get(node, [])
            for neighbor in next_nodes:
                if neighbor not in visited and neighbor not in queue:
                    queue.append(neighbor)
    
        # 確認哪個結束節點已被訪問，然後從那個節點返回結果
        visited_end_nodes = [node for node in self.end_nodes if node in visited]
        if len(visited_end_nodes) > 0:
            return {node: memory[node] for node in visited_end_nodes}
        else:
            raise ValueError("No end node was visited during the DAG execution.")



    
    def _get_one_parent(self, node):
        parents = [source for source, destinations in self.edges.items() if node in destinations]
        return parents[0] if parents else None






    def _get_parents(self, node):
        return [source for source, destinations in self.edges.items() if node in destinations]
    
    
    def _is_dag(self):
        visited = set()
        being_visited = set()  # 新增一個集合來追踪當前正在被訪問的節點
    
        def visit(node):
            if node in being_visited:
                return False
            if node in visited:
                return True
            
            visited.add(node)
            being_visited.add(node)
            
            for neighbor in self.edges.get(node, []):
                if not visit(neighbor):
                    return False
            
            being_visited.remove(node)
            return True
        
        return all(visit(node) for node in self.nodes)

    
    def display_graph(self):
        for source, destinations in self.edges.items():
            for dest in destinations:
                print(f"{source} --> {dest}")

    
    def visualize(self, render=False, render_format='png', view=True):
        try:
            from graphviz import Digraph
        except ImportError:
            raise ImportError("Please install the graphviz package to use the visualize function.")

        dot = Digraph()

        # 增加節點
        for node_name in self.nodes.keys():
            dot.node(node_name)

        # 增加邊
        for src, destinations in self.edges.items():
            for dest in destinations:
                dot.edge(src, dest)

        # 渲染圖形（如果需要的話）
        if render:
            dot.render('graph', format=render_format, view=view)

        # 顯示圖
        return dot

    def decision(self, func):
        """裝飾器用於將函數添加為決策節點。這樣的函數應返回一個結果和下一個節點名稱的元組。"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        node = Node(wrapper, self)
        self.branch_map[node.name] = None  # 初始化為 None，稍後在添加邊時更新
        return node
