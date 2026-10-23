
"""
EC551 Boolean Minimizer

Quine-McCluskey prime implicant generation
and minimum literal SOP/POS cover selection.
"""

from itertools import combinations


def combine_patterns(a, b):
    
    differences = [
        i for i, (x, y) in enumerate(zip(a, b))
        if x != y
    ]

    if len(differences) != 1:
        return None

    i = differences[0]

    if a[i] == "-" or b[i] == "-":
        return None

    return a[:i] + "-" + a[i + 1:]


def covers(pattern, index, n):
    
    bits = format(index, f"0{n}b")

    return all(
        p == "-" or p == bit
        for p, bit in zip(pattern, bits)
    )


def find_prime_implicants(minterms, n):
    """Find prime implicants using Quine-McCluskey."""
    current = {
        format(m, f"0{n}b") for m in minterms
    }
    primes = set()

    while current:
        used = set()
        next_level = set()

        for a, b in combinations(sorted(current), 2):
            merged = combine_patterns(a, b)

            if merged is not None:
                used.update((a, b))
                next_level.add(merged)

        primes.update(current - used)
        current = next_level

    return sorted(primes)


def minimum_cover(minterms, n):
    """Choose a cover minimizing literals"""
    minterms = sorted(set(minterms))

    if not minterms:
        return [], [], []

    primes = find_prime_implicants(minterms, n)

    coverage = {
        p: {
            m for m in minterms
            if covers(p, m, n)
        }
        for p in primes
    }

    essentials = sorted({
        p
        for m in minterms
        for p in primes
        if m in coverage[p]
        and sum(
            m in coverage[q] for q in primes
        ) == 1
    })

    covered = set()
    for p in essentials:
        covered.update(coverage[p])

    remaining = set(minterms) - covered
    candidates = [
        p for p in primes if p not in essentials
    ]

    best = None

    # Search covers by increasing number of added terms.
    # Evaluate all covers to prioritize literal count.
    for count in range(len(candidates) + 1):
        for group in combinations(candidates, count):
            group_coverage = set()

            for p in group:
                group_coverage.update(coverage[p])

            if not remaining <= group_coverage:
                continue

            selected = tuple(sorted(
                set(essentials) | set(group)
            ))

            literals = sum(
                n - p.count("-") for p in selected
            )

            score = (literals, len(selected), selected)

            if best is None or score < best[0]:
                best = (score, selected)

    return list(best[1]), primes, essentials


def patterns_to_sop(patterns, variables):
    """Convert binary patterns to Verilog generator terms."""
    terms = []

    for pattern in patterns:
        term = []

        for bit, var in zip(pattern, variables):
            if bit == "0":
                term.append("!" + var)
            elif bit == "1":
                term.append(var)

        terms.append(term)

    return terms


def format_sop(terms):
    """minimized SOP """
    if not terms:
        return "0"

    if any(not term for term in terms):
        return "1"

    return " | ".join(
        "(" + " & ".join(term) + ")"
        for term in terms
    )


def format_pos(patterns, variables):
    """Format minimized POS """
    if not patterns:
        return "1"

    if any(all(bit == "-" for bit in p)
           for p in patterns):
        return "0"

    clauses = []

    for pattern in patterns:
        literals = []

        for bit, var in zip(pattern, variables):
            if bit == "0":
                literals.append(var)
            elif bit == "1":
                literals.append("!" + var)

        clauses.append(
            "(" + " | ".join(literals) + ")"
        )

    return " & ".join(clauses)


def minimize_logic(variables, on_set, off_set):
    """minimized SOP/POS """
    n = len(variables)

    sop_patterns, primes, essentials = minimum_cover(
        on_set, n
    )

    pos_patterns, _, _ = minimum_cover(
        off_set, n
    )

    sop_terms = patterns_to_sop(
        sop_patterns, variables
    )

    sop_literals = sum(
        len(term) for term in sop_terms
    )

    pos_literals = sum(
        n - p.count("-") for p in pos_patterns
    )

    return {
        "sop_terms": sop_terms,
        "minimized_sop": format_sop(sop_terms),
        "minimized_pos": format_pos(
            pos_patterns, variables
        ),
        "sop_literals_saved":
            len(on_set) * n - sop_literals,
        "pos_literals_saved":
            len(off_set) * n - pos_literals,
        "prime_implicant_count": len(primes),
        "essential_prime_implicant_count":
            len(essentials),
        "prime_implicants": primes,
        "essential_prime_implicants": essentials,
    }
