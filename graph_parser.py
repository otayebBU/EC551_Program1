
import csv
import json
from itertools import product
from pathlib import Path


def parse_graph(file_path):
    """Read and validate a combinational logic graph."""

    with open(file_path, "r", encoding="utf-8") as file:
        circuit = json.load(file)

    inputs = circuit["inputs"]
    gates = circuit["gates"]
    output = circuit["output"]

    supported = {
        "AND", "OR", "NOT", "NAND",
        "NOR", "XOR", "XNOR", "BUF"
    }

    if not isinstance(inputs, list) or not isinstance(gates, list):
        raise ValueError("Inputs and gates must be lists.")

    if (
        not inputs
        or not all(isinstance(x, str) and x for x in inputs)
        or len(inputs) != len(set(inputs))
    ):
        raise ValueError("Input names must be unique and nonempty.")

    known_nodes = set(inputs)

    for gate in gates:
        gate_id = gate["id"]
        gate_type = gate["type"].upper()
        gate_inputs = gate["inputs"]

        if gate_type not in supported:
            raise ValueError(f"Unsupported gate: {gate_type}")

        if gate_id in known_nodes:
            raise ValueError(f"Duplicate node: {gate_id}")

        if gate_type in {"NOT", "BUF"}:
            if len(gate_inputs) != 1:
                raise ValueError(f"{gate_type} requires 1 input.")
        elif len(gate_inputs) < 2:
            raise ValueError(f"{gate_type} requires at least 2 inputs.")

        for source in gate_inputs:
            if source not in known_nodes:
                raise ValueError(
                    f"Unknown or not-yet-defined node: {source}"
                )

        known_nodes.add(gate_id)

    if output not in known_nodes:
        raise ValueError(f"Unknown output node: {output}")

    return circuit


def evaluate_gate(gate_type, values):
    """Calculate the output of one logic gate."""

    gate_type = gate_type.upper()

    if gate_type == "AND":
        return int(all(values))
    if gate_type == "OR":
        return int(any(values))
    if gate_type == "NOT":
        return 1 - values[0]
    if gate_type == "NAND":
        return 1 - int(all(values))
    if gate_type == "NOR":
        return 1 - int(any(values))
    if gate_type == "XOR":
        return sum(values) % 2
    if gate_type == "XNOR":
        return 1 - (sum(values) % 2)
    if gate_type == "BUF":
        return values[0]

    raise ValueError(f"Unsupported gate: {gate_type}")


def evaluate_circuit(circuit, input_values):
    """Evaluate the circuit for one input combination."""

    signals = dict(input_values)

    for gate in circuit["gates"]:
        values = [
            signals[name] for name in gate["inputs"]
        ]

        signals[gate["id"]] = evaluate_gate(
            gate["type"], values
        )

    return signals[circuit["output"]]


def generate_truth_table(circuit):
    """Generate all rows of the truth table."""

    variables = circuit["inputs"]
    table = []

    for combination in product([0, 1], repeat=len(variables)):
        input_values = dict(zip(variables, combination))
        output_value = evaluate_circuit(
            circuit, input_values
        )

        row = dict(input_values)
        row["F"] = output_value
        table.append(row)

    return table


def print_truth_table(circuit, table):
    """Print the truth table in the terminal."""

    columns = circuit["inputs"] + ["F"]

    print("\nTruth Table:")
    print(" | ".join(columns))
    print("-" * (4 * len(columns) - 3))

    for row in table:
        print(" | ".join(str(row[col]) for col in columns))


def export_truth_table(circuit, table, output_file="truth_table.csv"):
    """Export the truth table to a CSV file."""

    columns = circuit["inputs"] + ["F"]

    with open(
        output_file, "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(table)

    print(f"\nTruth table exported successfully: {output_file}")


def analyze_circuit(circuit):
    """Count gates and calculate the longest logic path."""

    gate_count = len(circuit["gates"])

    # Primary inputs start at depth 0.
    depths = {name: 0 for name in circuit["inputs"]}

    for gate in circuit["gates"]:
        input_depths = [
            depths[name] for name in gate["inputs"]
        ]

        # Each gate adds one logic level.
        depths[gate["id"]] = max(input_depths) + 1

    logic_depth = depths[circuit["output"]]

    print("\nCircuit Analysis:")
    print("Gate Count:", gate_count)
    print("Logic Depth:", logic_depth)

    return {
        "gate_count": gate_count,
        "logic_depth": logic_depth
    }

if __name__ == "__main__":



    # Example circuit: F = A*B + C
    example_circuit = {
        "inputs": ["A", "B", "C"],
        "gates": [
            {
                "id": "g1",
                "type": "AND",
                "inputs": ["A", "B"]
            },
            {
                "id": "g2",
                "type": "OR",
                "inputs": ["g1", "C"]
            }
        ],
        "output": "g2"
    }

    example_path = Path("example_graph.json")

    example_path.write_text(
        json.dumps(example_circuit, indent=4),
        encoding="utf-8"
    )

    circuit = parse_graph(example_path)

    print("Graph parsed successfully!")
    print("Primary inputs:", circuit["inputs"])
    print("Number of gates:", len(circuit["gates"]))
    print("Output node:", circuit["output"])

    truth_table = generate_truth_table(circuit)

    print_truth_table(circuit, truth_table)

    # Custom Command #1
    export_truth_table(circuit, truth_table, "truth_table.csv")
    
    analyze_circuit(circuit)

