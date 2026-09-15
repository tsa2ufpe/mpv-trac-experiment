"""Second anonymization step: replace source-system identifiers with dense sequential integers.

Applied to every event log in ../event_logs and ../event_logs_original_pt after the initial
cleaning (anonym.py). Within each log, cases are numbered 0..N-1 in chronological order of their
first event (ties broken by order of first appearance), so the new identifier is not a function
of the source key and carries no information beyond the timestamps already present in the log.
In Schema A (JECs) the event identifier `id` is renumbered 0..M-1 in row order and `documentoID`
is replaced by a dense index in order of first appearance (empty values are preserved).

Every other column, the row order and the line terminator of each file are kept byte for byte.
The mapping from source identifiers to new ones is held in memory only and never written out.
Each log is an independent process instance population (no case occurs in two logs), so no
consistency across files is required.

Usage:  python renumber_ids.py            (run from data/anonymization)
"""
import gzip
import os

FAMILIES = ["juizados", "civel", "criminal", "eleitoral", "fazenda", "trabalho"]
UNITS = ["%s_%d" % (f, n) for f in FAMILIES for n in (1, 2, 3)]
HERE = os.path.dirname(os.path.abspath(__file__))
DIRS = [os.path.join(HERE, "..", "event_logs_original_pt"), os.path.join(HERE, "..", "event_logs")]


def read(path):
    raw = gzip.open(path, "rb").read()
    term = "\r\n" if b"\r\n" in raw[:4096] else "\n"
    lines = raw.decode("utf-8").split(term)
    trailing = lines[-1] == ""
    if trailing:
        lines.pop()
    return lines, term, trailing


def write(path, lines, term, trailing):
    text = term.join(lines) + (term if trailing else "")
    with open(path, "wb") as f:
        with gzip.GzipFile(filename=os.path.basename(path)[:-3], mode="wb", fileobj=f, mtime=0,
                           compresslevel=9) as g:
            g.write(text.encode("utf-8"))


def case_order(lines, schema_a):
    """Cases sorted by (first event timestamp, first appearance)."""
    header = lines[0].split(",")
    i_case, i_ts = (1 if schema_a else 0), header.index("dataInicio")
    first, order = {}, []
    for k, line in enumerate(lines[1:]):
        fields = line.split(",")
        case, ts = fields[i_case], fields[i_ts].replace("T", " ").strip()
        if case not in first:
            first[case] = [ts, k]
            order.append(case)
        elif ts < first[case][0]:
            first[case][0] = ts
    return sorted(order, key=lambda c: (first[c][0], first[c][1]))


for unit in UNITS:
    pairs = {d: read(os.path.join(d, unit + "_cleaned.csv.gz")) for d in DIRS}
    ref_lines = pairs[DIRS[0]][0]
    schema_a = ref_lines[0].startswith("id,")
    mapping = {case: str(i) for i, case in enumerate(case_order(ref_lines, schema_a))}
    for d, (lines, term, trailing) in pairs.items():
        out, docs = [lines[0]], {}
        for k, line in enumerate(lines[1:]):
            if schema_a:  # id,processoID,Case,<middle...>,usuarioID,documentoID,movimentoID
                head, rest = line.split(",", 3)[:3], line.split(",", 3)[3]
                middle, doc, mov = rest.rsplit(",", 2)
                if doc and doc not in docs:
                    docs[doc] = str(len(docs))
                line = ",".join([str(k), mapping[head[1]], head[2], middle, docs.get(doc, ""), mov])
            else:  # processoID,<rest...>
                case, rest = line.split(",", 1)
                line = mapping[case] + "," + rest
            out.append(line)
        write(os.path.join(d, unit + "_cleaned.csv.gz"), out, term, trailing)
    print("%-12s %6d cases renumbered" % (unit, len(mapping)))
