"""
Basic Example for TaskFlowDag
------------------------------
This script demonstrates a simple use-case of the Dag module from TaskFlowDag.
It constructs a Dag with several nodes and then infers the result.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from collections.abc import Sequence
from dag_module.dag import Dag

# Initialize a Dag with debug mode enabled
dag = Dag(debug=True)

@dag.node
def increment_input(x):
    """Increment input value. If input is a list, increment the first element."""
    return x[0] + 1 if isinstance(x, list) else x + 1

@dag.node
def add_two(x):
    """Add 2 to the input. Sum the elements if input is a sequence."""
    x = sum(x) if isinstance(x, Sequence) else x
    return x + 2

@dag.node
def add_three(x):
    """Add 3 to the input. Sum the elements if input is a sequence."""
    x = sum(x) if isinstance(x, Sequence) else x
    return x + 3

@dag.node
def sum_and_add_four(inputs):
    """Sum the inputs and add 4."""
    return sum(inputs) + 4

@dag.node
def add_five(x):
    """Add 5 to the input. Sum the elements if input is a sequence."""
    x = sum(x) if isinstance(x, Sequence) else x
    return x + 5

@dag.node
def end_node(x):
    """End node that simply returns its input."""
    return x

# Define the flow of the DAG
increment_input >> add_two >> sum_and_add_four >> add_five >> end_node
increment_input >> add_three >> sum_and_add_four >> add_five

# Infer the result of the DAG with an initial input of 1
result = dag.infer(1)
print(f"Final Result: {result}")


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