#
# chemicalFormulas.py
#
# Copyright (c) 2003,2019 Paul McGuire
#

from mo_parsing import Word, Group, Optional
from mo_parsing.utils import alphas

atomicWeight = {
    "O": 15.9994,
    "H": 1.00794,
    "Na": 22.9897,
    "Cl": 35.4527,
    "C": 12.0107,
}

digits = "0123456789"

# Version 1
element = Word(alphas.upper(), alphas.lower(), max=2)
# for stricter matching, use this Regex instead
# element = Regex("A[cglmrstu]|B[aehikr]?|C[adeflmorsu]?|D[bsy]|"
#                 "E[rsu]|F[emr]?|G[ade]|H[efgos]?|I[nr]?|Kr?|L[airu]|"
#                 "M[dgnot]|N[abdeiop]?|Os?|P[abdmortu]?|R[abefghnu]|"
#                 "S[bcegimnr]?|T[abcehilm]|U(u[bhopqst])?|V|W|Xe|Yb?|Z[nr]")
elementRef = Group(element + Optional(Word(digits), default="1"))
formula = elementRef[...]

fn = lambda elemList: sum(atomicWeight[elem] * int(qty) for elem, qty in elemList)
import tests
formula.runTests(
    """\
    H2O
    C6H5OH
    NaCl
    """,
    fullDump=False,
    postParse=lambda _, tokens: "Molecular weight: {}".format(fn(tokens)),
)


# Version 2 - access parsed items by results name
elementRef = Group(
    element("symbol") + Optional(Word(digits), default="1")("qty")
)
formula = elementRef[...]

fn = lambda elemList: sum(
    atomicWeight[elem['symbol']] * int(elem['qty']) for elem in elemList
)
formula.runTests(
    """\
    H2O
    C6H5OH
    NaCl
    """,
    fullDump=False,
    postParse=lambda _, tokens: "Molecular weight: {}".format(fn(tokens)),
)


# Version 3 - convert integers during parsing process
integer = Word(digits).addParseAction(lambda t: int(t[0]))
elementRef = Group(element("symbol") + Optional(integer, default=1)("qty"))
formula = elementRef[...]

fn = lambda elemList: sum(atomicWeight[elem['symbol']] * elem['qty'] for elem in elemList)
formula.runTests(
    """\
    H2O
    C6H5OH
    NaCl
    """,
    fullDump=False,
    postParse=lambda _, tokens: "Molecular weight: {}".format(fn(tokens)),
)


# Version 4 - parse and convert integers as subscript digits
subscript_digits = "₀₁₂₃₄₅₆₇₈₉"
subscript_int_map = {e[1]: e[0] for e in enumerate(subscript_digits)}


def cvt_subscript_int(s):
    ret = 0
    for c in s[0]:
        ret = ret * 10 + subscript_int_map[c]
    return ret


subscript_int = Word(subscript_digits).addParseAction(cvt_subscript_int)

elementRef = Group(element("symbol") + Optional(subscript_int, default=1)("qty"))
formula = elementRef[...]
formula.runTests(
    """\
    H₂O
    C₆H₅OH
    NaCl
    """,
    fullDump=False,
    postParse=lambda _, tokens: "Molecular weight: {}".format(fn(tokens)),
)

