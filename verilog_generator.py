
from pathlib import Path


def generate_verilog(variables, minimized_sop, output_file="generated.v"):
    """
    Generate structural Verilog from a minimized SOP expression.

    Example:
        variables = ["A", "B", "C"]
        minimized_sop = [["!A", "B"], ["A", "!C"]]

    Represents:
        F = (!A & B) | (A & !C)
    """

    lines = []
    lines.append("module generated_circuit (")

    for var in variables:
        lines.append(f"    input wire {var},")

    lines.append("    output wire F")
    lines.append(");")
    lines.append("")

    # Handle constant zero
    if not minimized_sop:
        lines.append("    supply0 const_zero;")
        lines.append("    buf g0(F, const_zero);")

    # Handle constant one
    elif any(len(term) == 0 for term in minimized_sop):
        lines.append("    supply1 const_one;")
        lines.append("    buf g0(F, const_one);")

    else:
        # Find all negated variables
        negated = sorted({
            literal[1:]
            for term in minimized_sop
            for literal in term
            if literal.startswith("!")
        })

        # Declare intermediate wires
        for var in negated:
            lines.append(f"    wire not_{var};")

        for i, _ in enumerate(minimized_sop):
            lines.append(f"    wire term_{i};")

        lines.append("")

        gate_id = 0

        # Generate NOT gates
        for var in negated:
            lines.append(
                f"    not g{gate_id}(not_{var}, {var});"
            )
            gate_id += 1

        # Generate AND gates for SOP terms
        for i, term in enumerate(minimized_sop):
            inputs = [
                f"not_{lit[1:]}" if lit.startswith("!") else lit
                for lit in term
            ]

            if len(inputs) == 1:
                lines.append(
                    f"    buf g{gate_id}(term_{i}, {inputs[0]});"
                )
            else:
                lines.append(
                    f"    and g{gate_id}(term_{i}, "
                    f"{', '.join(inputs)});"
                )

            gate_id += 1

        # Generate OR gate for final output
        term_wires = [
            f"term_{i}"
            for i in range(len(minimized_sop))
        ]

        if len(term_wires) == 1:
            lines.append(
                f"    buf g{gate_id}(F, {term_wires[0]});"
            )
        else:
            lines.append(
                f"    or g{gate_id}(F, "
                f"{', '.join(term_wires)});"
            )

    lines.append("")
    lines.append("endmodule")

    # Save generated Verilog
    verilog_code = "\n".join(lines) + "\n"

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(verilog_code, encoding="utf-8")

    return verilog_code


if __name__ == "__main__":
    # Test function: F = !A*B + A*!C
    variables = ["A", "B", "C"]
    minimized_sop = [["!A", "B"], ["A", "!C"]]

    result = generate_verilog(
        variables,
        minimized_sop,
        "generated.v"
    )

    print(result)
    print("Verilog file generated successfully!")
