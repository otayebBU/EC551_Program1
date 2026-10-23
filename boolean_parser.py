

import json
import re


def tokenize(expression):
    """Convert a Boolean expression into tokens."""
    expression = expression.strip()

    if "=" in expression:
        left, expression = expression.split("=", 1)
        if left.strip().upper() != "F":
            raise ValueError("Use F = ... for the output.")

    expression = re.sub(r"\s+", "", expression).upper()

    if not expression:
        raise ValueError("Boolean expression cannot be empty.")

    # Supported: A-Z, 0, 1, +, |, *, &, ^, !, ~, ', (, )
    tokens = re.findall(r"[A-Z01+|*&^!~'()]", expression)

    if "".join(tokens) != expression:
        raise ValueError("Expression contains unsupported characters.")

    return tokens


class BooleanParser:
    def __init__(self, expression):
        self.tokens = tokenize(expression)
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, expected=None):
        token = self.peek()
        if token is None:
            raise ValueError("Unexpected end of expression.")
        if expected is not None and token != expected:
            raise ValueError(f"Expected {expected}, got {token}.")
        self.pos += 1
        return token

    def parse(self):
        result = self.parse_or()
        if self.peek() is not None:
            raise ValueError(f"Unexpected token: {self.peek()}")
        return result

    def parse_or(self):
        left = self.parse_xor()
        while self.peek() in ("+", "|"):
            self.consume()
            right = self.parse_xor()
            left = ("OR", left, right)
        return left

    def parse_xor(self):
        left = self.parse_and()
        while self.peek() == "^":
            self.consume()
            right = self.parse_and()
            left = ("XOR", left, right)
        return left

    def parse_and(self):
        left = self.parse_not()
        while True:
            token = self.peek()
            if token in ("*", "&"):
                self.consume()
                right = self.parse_not()
                left = ("AND", left, right)
            elif token is not None and (
                token == "(" or token in ("!", "~")
                or token.isalpha() or token in ("0", "1")
            ):
                # Adjacent terms mean AND: AB, A(B+C)
                right = self.parse_not()
                left = ("AND", left, right)
            else:
                break
        return left

    def parse_not(self):
        if self.peek() in ("!", "~"):
            self.consume()
            return ("NOT", self.parse_not())

        node = self.parse_atom()

        while self.peek() == "'":
            self.consume()
            node = ("NOT", node)

        return node

    def parse_atom(self):
        token = self.peek()

        if token == "(":
            self.consume("(")
            node = self.parse_or()
            self.consume(")")
            return node

        if token is not None and (
            token.isalpha() or token in ("0", "1")
        ):
            return self.consume()

        raise ValueError(f"Unexpected token: {token}")


def expression_to_graph(expression):
    """Build a gate-level graph compatible with graph_parser.py."""
    tree = BooleanParser(expression).parse()

    variables = sorted(set(
        token for token in tokenize(expression)
        if token.isalpha()
    ))

    if not variables:
        raise ValueError("Include at least one input variable.")

    gates = []

    def build(node):
        if isinstance(node, str):
            if node in ("0", "1"):
                
                a = variables[0]
                gate_id = f"g{len(gates) + 1}"
                gates.append({
                    "id": gate_id,
                    "type": "AND" if node == "0" else "OR",
                    "inputs": [a, f"not_{a}"]
                })
                return gate_id
            return node

        operation = node[0]
        children = [build(child) for child in node[1:]]

        gate_id = f"g{len(gates) + 1}"
        gates.append({
            "id": gate_id,
            "type": operation,
            "inputs": children
        })
        return gate_id

    
    if "0" in tokenize(expression) or "1" in tokenize(expression):
        raise ValueError(
            "Constant 0/1 inputs are not supported yet."
        )

    output = build(tree)

  
    if not gates:
        gates.append({
            "id": "g1",
            "type": "BUF",
            "inputs": [output]
        })
        output = "g1"

    return {
        "inputs": variables,
        "gates": gates,
        "output": output
    }


def save_expression_graph(expression, filename="expression_graph.json"):
    graph = expression_to_graph(expression)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(graph, file, indent=2)

    return filename


if __name__ == "__main__":
    expression = input("Enter Boolean function: ")
    filename = save_expression_graph(expression)
    print(f"Created {filename}")
