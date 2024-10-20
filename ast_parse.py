import json
import re

# Define the AST Node class
class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type
        self.value = value
        self.left = left
        self.right = right

    def to_dict(self):
        result = {"type": self.type, "value": self.value}
        if self.left:
            result["left"] = self.left.to_dict()
        if self.right:
            result["right"] = self.right.to_dict()
        return result

    def print_tree(self, level=0):
        tree_representation = []
        indent = "    " * level
        if self.type == "operator":
            tree_representation.append(f"{indent}{self.value}")
            if self.left:
                tree_representation.extend(self.left.print_tree(level + 1))
            if self.right:
                tree_representation.extend(self.right.print_tree(level + 1))
        elif self.type == "operand":
            tree_representation.append(f"{indent}{self.value[0]} {self.value[1]} {self.value[2]}")
        return tree_representation

def parse_condition(condition):
    match = re.match(r"(\w+)\s*([<>=]+)\s*(.+)", condition.strip())
    if match:
        field, operator, value = match.groups()
        return Node("operand", (field, operator, value.strip().strip("'")))
    return None

def create_ast_from_input(rule_string):
    def process_stack(operator_stack, operand_stack):
        right = operand_stack.pop()
        left = operand_stack.pop()
        operator = operator_stack.pop()
        operator.left = left
        operator.right = right
        operand_stack.append(operator)

    tokens = re.split(r'(\band\b|\bor\b|\(|\))', rule_string)
    operand_stack = []
    operator_stack = []

    for token in tokens:
        token = token.strip()
        if token == "":
            continue
        if token == "(":
            operator_stack.append(token)
        elif token == ")":
            while operator_stack and operator_stack[-1] != "(":
                process_stack(operator_stack, operand_stack)
            operator_stack.pop()  # Pop the "("
        elif token.lower() in ("and", "or"):
            while (operator_stack and isinstance(operator_stack[-1], Node) and
                   operator_stack[-1].value in ("and", "or")):
                process_stack(operator_stack, operand_stack)
            operator_stack.append(Node("operator", token.lower()))
        else:
            condition_node = parse_condition(token)
            if condition_node:
                operand_stack.append(condition_node)
            else:
                print(f"Warning: Unable to parse condition '{token}'")

    while operator_stack:
        process_stack(operator_stack, operand_stack)

    if len(operand_stack) == 1:
        return operand_stack[0]
    else:
        print("Error: The rule could not be parsed correctly.")
        return None

def get_ast_and_parse_tree(rule_string):
    ast = create_ast_from_input(rule_string)
    parse_tree = []
    ast_json = None

    if ast:
        parse_tree = ast.print_tree()
        ast_json = json.dumps(ast.to_dict(), indent=4)

    return ast_json, parse_tree
