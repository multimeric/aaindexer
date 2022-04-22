from pyparsing import *
from pyparsing import common
from string import ascii_uppercase
from itertools import chain


def visit_general_field(s, loc, toks):
    return toks[0], " ".join(toks[1:])


def visit_corr_field(s, loc, toks):
    if len(toks) == 0:
        return None
    else:
        return "corr", dict(list(toks))


def visit_index_field(s, loc, toks):
    names, values = toks
    ordered_names = list(chain.from_iterable(zip(*names)))
    pairs = dict(list(zip(ordered_names, values)))
    return "index", pairs


def visit_matrix_field(s, loc, toks):
    row_names, col_names, *vals = toks
    row = 0
    col = 0
    ret = {}
    for val in vals:
        key = row_names[row], col_names[col]
        ret[key] = val
        row += 1
        if row > col:
            row = 0
            col += 1

    return "matrix", ret


def visit_record(s, loc, toks):
    return dict(list(toks))


def visit_general_field_name(s, loc, toks):
    return {
        "H": "accession",
        "D": "description",
        "R": "pmid",
        "A": "authors",
        "T": "title",
        "J": "journal",
        "C": "correlation",
        "I": "index",
        "M": "matrix",
    }[toks[0]]


def grouper(s, loc, toks):
    return [list(toks)]


general_field_name = (
    Char(set(ascii_uppercase) - {"I", "C", "M"})
        .set_name("general_field_name")
        .add_parse_action(visit_general_field_name)
)
record_footer = (Literal("//") + LineEnd()).set_name("record_footer").suppress()
header_sep = Literal(" ").set_name("header_sep").suppress()
general_field_contents = SkipTo(LineEnd()) + LineEnd().suppress()
general_field_line = (Literal("  ").suppress() + general_field_contents).set_name(
    "general_field_line"
)
general_field = (
    (
            general_field_name
            + (
                    (header_sep + general_field_contents + Opt(general_field_line[1, ...]))
                    ^ LineEnd()
            )
    )
        .set_name("general_field")
        .set_parse_action(visit_general_field)
)
aa_name = (
    (Char(ascii_uppercase) + Literal("/").suppress() + Char(ascii_uppercase))
        .set_name("aa_name")
        .add_parse_action(grouper)
)

index_field = (
    (
            Literal("I").suppress()
            + White().suppress()
            + delimited_list(aa_name, delim=White()).add_parse_action(grouper)
            + White().suppress()
            + delimited_list(
        common.real, delim=White(), allow_trailing_delim=False
    ).add_parse_action(grouper)
            + LineEnd().suppress()
    )
        .set_name("index_field")
        .add_parse_action(visit_index_field)
)

corr_entry = (
    (Word(alphanums) + White().suppress() + common.real)
        .set_name("corr_entry")
        .set_parse_action(grouper)
)
corr_field = (
    (
            Literal("C").suppress()
            + (
                    (
                            header_sep
                            + delimited_list(corr_entry, delim=White())
                    )
                    ^ White(" ").suppress()
            )
            + LineEnd().suppress()
    )
        .set_name("corr_field")
        .add_parse_action(visit_corr_field)
)
matrix_field = (
    (
            Literal("M").suppress()
            + header_sep
            + Literal("rows = ").suppress()
            + Word(ascii_uppercase).set_name("matrix_row_labels")
            + Literal(", cols = ").suppress()
            + Word(ascii_uppercase).set_name("matrix_column_labels")
            + LineEnd().suppress()
            + White().suppress()
            + delimited_list(common.real, White(), allow_trailing_delim=True)
    )
        .set_name("matrix_field")
        .add_parse_action(visit_matrix_field)
)
aaindex_field = (index_field ^ corr_field ^ matrix_field ^ general_field).set_name(
    "aaindex_record"
)
aaindex_record = (
    (aaindex_field[1, ...] + record_footer)
        .set_name("aaindex_record")
        .add_parse_action(visit_record)
)
aaindex_file = (
    aaindex_record[1, ...].set_name("aaindex_file").leave_whitespace(recursive=True).add_parse_action(lambda s, loc, toks: list(toks))
)
