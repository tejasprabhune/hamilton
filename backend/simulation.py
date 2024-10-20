import re

def open_bill():
    """
    Opens the bill and returns the clauses in a list.
    """

    # Open the bill
    with open('agriculture_bill.txt', 'r') as bill:
        bill_lines = bill.readlines()

        clauses = []

        current_clause = ""

        for i in range(len(bill_lines)):
            bill_lines[i] = parse_line(bill_lines[i])
            if "SECTION" in bill_lines[i]:
                if current_clause:
                    clauses.append(current_clause)
                    current_clause = ""
                current_clause += bill_lines[i]
            else:
                current_clause += bill_lines[i]

        clauses.append(current_clause)


    return clauses

def parse_line(line):
    """
    Parses a line of the bill into HTML with <p> tags and correct indenting.
    """

    line = line.replace("\n", "")

    u_alpha_re = re.compile(r'\([A-Z]\)')
    num_re = re.compile(r'\([0-9]\)')

    if u_alpha_re.match(line):
        return f'<p style="padding-left: 2em" class="clause-text">{line}</p>'
    elif num_re.match(line):
        return f'<p style="padding-left: 1em" class="clause-text">{line}</p>'
    else:
        return f'<p class="clause-text">{line}</p>'


def get_senator(senator_id):
    pass

def start_conversation(clause_id, clause, senator1, senator2):
    pass
