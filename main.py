
import argparse

from graph_parser import (
    parse_graph,
    generate_truth_table,
    print_truth_table,
    export_truth_table,
    analyze_circuit,
)

from boolean_parser import save_expression_graph
from logic_synthesis import analyze_logic
from minimizer import minimize_logic
from verilog_generator import generate_verilog


def main():
    parser = argparse.ArgumentParser(
        description="EC551 Logic Synthesis Engine"
    )

   
    parser.add_argument(
        "input",
        nargs="?",
        default=None,
        help="Input JSON circuit file"
    )

   
    parser.add_argument(
        "--expr",
        type=str,
        help="Boolean expression, e.g. F = AB + C"
    )

  
    parser.add_argument(
        "--output",
        default="generated.v",
        help="Generated structural Verilog filename"
    )

   
    parser.add_argument(
        "--csv",
        default="truth_table.csv",
        help="Exported truth table filename"
    )

    args = parser.parse_args()


    if args.expr is not None:

        if args.input is not None:
            parser.error(
                "Use either a JSON input file or --expr, not both."
            )

        print("\n=== BOOLEAN EXPRESSION INPUT ===")
        print("Expression:", args.expr)

        # Convert Boolean expression into a gate-level JSON circuit
        input_file = save_expression_graph(
            args.expr,
            "expression_graph.json"
        )

        print("Converted to circuit:", input_file)

    else:

        input_file = args.input or "example_graph.json"

        print("\n=== DIGITAL LOGIC CIRCUIT INPUT ===")
        print("Circuit file:", input_file)

    
    circuit = parse_graph(input_file)
    variables = circuit["inputs"]

    print("\nInput variables:", variables)

    

    table = generate_truth_table(circuit)

    # -----------------------------------
    # STEP 4: Canonical logic analysis
    # -----------------------------------

    analysis = analyze_logic(circuit)

    # -----------------------------------
    # STEP 5: Minimize Boolean function
    # -----------------------------------

    minimized = minimize_logic(
        variables,
        analysis["on_set"],
        analysis["off_set"]
    )

    # -----------------------------------
    # STEP 6: Display 12 operations
    # -----------------------------------

    print("\n=== EC551 LOGIC SYNTHESIS ENGINE ===")

    print("\n1. Canonical SOP:")
    print(analysis["canonical_sop"])

    print("\n2. Canonical POS:")
    print(analysis["canonical_pos"])

    print("\n3. Inverse Canonical SOP:")
    print(analysis["inverse_sop"])

    print("\n4. Inverse Canonical POS:")
    print(analysis["inverse_pos"])

    print("\n5. Minimized SOP:")
    print(minimized["minimized_sop"])
    print(
        "Literals saved:",
        minimized["sop_literals_saved"]
    )

    print("\n6. Minimized POS:")
    print(minimized["minimized_pos"])
    print(
        "Literals saved:",
        minimized["pos_literals_saved"]
    )

    print("\n7. Prime Implicants:")
    print(minimized["prime_implicant_count"])

    print("\n8. Essential Prime Implicants:")
    print(minimized["essential_prime_implicant_count"])

    print("\n9. ON-set Minterms:")
    print(analysis["on_set"])
    print("Count:", analysis["on_count"])

    print("\n10. OFF-set Maxterms:")
    print(analysis["off_set"])
    print("Count:", analysis["off_count"])

    print("\n11. Truth Table Export:")
    print_truth_table(circuit, table)
    export_truth_table(circuit, table, args.csv)

    print("\n12. Circuit Analysis:")
    analyze_circuit(circuit)



    print("\n=== VERILOG GENERATION ===")

    generate_verilog(
        variables,
        minimized["sop_terms"],
        args.output
    )

    print("Structural Verilog saved to:", args.output)

    print("\n=== SYNTHESIS COMPLETE ===")


if __name__ == "__main__":
    main()
