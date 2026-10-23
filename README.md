# EC551 Programming Assignment 1 – Logic Synthesis Engine

## 1. Project Overview

This project implements a Python-based logic synthesis engine for digital combinational circuits.

The program reads a circuit description, analyzes its Boolean function, performs logic minimization, calculates circuit metrics, and automatically generates structural Verilog code.

The generated Verilog can be synthesized and simulated using AMD Vivado.

## 2. Project Structure

| File | Description |
|---|---|
| `main.py` | Main command-line interface that integrates all modules |
| `graph_parser.py` | Reads and validates JSON circuit descriptions, generates truth tables, and analyzes circuit structure |
| `logic_synthesis.py` | Computes canonical SOP/POS, inverse forms, and ON/OFF sets |
| `minimizer.py` | Performs Boolean minimization and calculates prime implicants |
| `verilog_generator.py` | Generates structural Verilog using logic gate primitives |
| `example_graph.json` | Example input circuit |
| `generated.v` | Example generated Verilog output |
| `truth_table.csv` | Exported truth table |
| `tests/test_synthesis.py` | Automated unit tests |

## 3. Features

The engine provides the following 12 operations:

1. Canonical SOP
2. Canonical POS
3. Inverse Canonical SOP
4. Inverse Canonical POS
5. Literal Minimized SOP and literals saved
6. Literal Minimized POS and literals saved
7. Prime Implicant Count
8. Essential Prime Implicant Count
9. ON-Set Minterms
10. OFF-Set Maxterms
11. Custom Command #1: Truth Table Export
12. Custom Command #2: Gate Count and Logic Depth

The program also generates structural Verilog code from the minimized SOP representation.

## 4. Requirements

- Python 3
- AMD Vivado for Verilog synthesis and simulation
- An FPGA development board for hardware demonstration

The Python implementation uses standard-library functionality.

## 5. How to Run

Open a terminal in the project directory.

### Run the Main Program

```bash
python main.py
```

By default, the program reads `example_graph.json` and generates `generated.v` and `truth_table.csv`.

### Use a Different Input File

```bash
python main.py your_circuit.json
```

To customize the output filenames:

```bash
python main.py your_circuit.json --output result.v --csv result.csv
```

### Input File Format

The program accepts JSON files describing combinational logic circuits. Each file specifies the primary inputs, logic gates, their connections, and the output node.

For example, the following JSON represents **F = (A AND B) OR C**:

```json
{
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
```

Save the circuit description as a `.json` file, then run:

```bash
python main.py example_graph.json
```

The program displays Boolean analysis results, generates a truth table, reports circuit metrics, and exports structural Verilog code.

## 6. Running Tests

Run the automated tests using:

```bash
python -m unittest discover -s tests -v
```

The current test suite includes three test cases:

- Constant-zero function
- Constant-one function
- Example combinational circuit

All three tests passed in our local test run.

## 7. Vivado Verification

We tested the structural Verilog generator using the Boolean function:

**F = (!A & B) | (A & !C)**

The generated Verilog was successfully synthesized in AMD Vivado using one LUT3. Behavioral simulation verified all eight input combinations with zero errors.

We also successfully ran the integrated Python application and generated a new Verilog file from the example circuit.

This verifies the tested Verilog example and confirms that the integrated application can execute successfully. Further testing on a physical FPGA development board is required for the hardware demonstration.

## 8. AI Usage Disclosure

ChatGPT was used as a supporting tool to explain technical concepts, assist with writing and modifying selected code sections, troubleshoot errors, and improve documentation.

The team was responsible for integrating the project modules, reviewing and testing the implementation, and verifying the results. We are prepared to explain the code and design decisions during the demonstration.