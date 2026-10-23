
"""
EC551 Logic Synthesis Engine
Canonical SOP, POS, inverse functions, and ON/OFF sets.
"""

from graph_parser import parse_graph, generate_truth_table


def get_on_off_sets(table):
    
    on_set = []
    off_set = []

    for index, row in enumerate(table):
        if row["F"] == 1:
            on_set.append(index)
        else:
            off_set.append(index)

    return on_set, off_set


def canonical_sop(variables, table):
    """ canonical Sum of Products."""
    terms = []

    for row in table:
        if row["F"] == 1:
            literals = []

            for var in variables:
                if row[var] == 0:
                    literals.append("!" + var)
                else:
                    literals.append(var)

            terms.append("(" + " & ".join(literals) + ")")

    return " | ".join(terms) if terms else "0"


def canonical_pos(variables, table):
    """canonical Product of Sums."""
    terms = []

    for row in table:
        if row["F"] == 0:
            literals = []

            for var in variables:
                if row[var] == 0:
                    literals.append(var)
                else:
                    literals.append("!" + var)

            terms.append("(" + " | ".join(literals) + ")")

    return " & ".join(terms) if terms else "1"


def invert_truth_table(table):
    """Flip F to generate the inverse truth table."""
    inverse = []

    for row in table:
        new_row = row.copy()
        new_row["F"] = 1 - row["F"]
        inverse.append(new_row)

    return inverse


def analyze_logic(circuit):
    """canonical expressions and ON/OFF counts."""
    variables = circuit["inputs"]
    table = generate_truth_table(circuit)

    on_set, off_set = get_on_off_sets(table)
    inverse = invert_truth_table(table)

    return {
        "variables": variables,
        "table": table,
        "on_set": on_set,
        "off_set": off_set,
        "canonical_sop": canonical_sop(variables, table),
        "canonical_pos": canonical_pos(variables, table),
        "inverse_sop": canonical_sop(variables, inverse),
        "inverse_pos": canonical_pos(variables, inverse),
        "on_count": len(on_set),
        "off_count": len(off_set),
    }


if __name__ == "__main__":
    circuit = parse_graph("example_graph.json")
    result = analyze_logic(circuit)

    print("Canonical SOP:", result["canonical_sop"])
    print("Canonical POS:", result["canonical_pos"])
    print("Inverse SOP:", result["inverse_sop"])
    print("Inverse POS:", result["inverse_pos"])
    print("ON-set:", result["on_set"])
    print("OFF-set:", result["off_set"])
    print("ON count:", result["on_count"])
    print("OFF count:", result["off_count"])
