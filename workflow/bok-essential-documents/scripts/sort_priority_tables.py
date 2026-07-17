"""
Sort markdown tables by priority column (🔴→🟡→🟢).

Usage: python3 sort_priority_tables.py

Reads a markdown file, identifies all tables (header+separator+rows),
sorts rows within each table by the priority column, writes back.
"""

import sys

def priority_sort_key(row):
    cols = [c.strip() for c in row.split('|')]
    if len(cols) >= 4:
        p = cols[3]  # Priority is typically the 4th column (0=empty, 1=Doc, 2=Desc, 3=Priority, 4=Ref)
        if p.startswith('\U0001f534'):   # 🔴 Must Have
            return (0, cols[1])
        elif p.startswith('\U0001f7e1'): # 🟡 Nice to Have
            return (1, cols[1])
        elif p.startswith('\U0001f7e2'): # 🟢 Optional
            return (2, cols[1])
    return (9, '')

def sort_tables_in_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    output = []
    i = 0
    in_table = False
    table_header = []
    table_rows = []

    while i < len(lines):
        line = lines[i]
        # Detect table: header row with |...| followed by separator row with |---|
        if not in_table and line.startswith('|') and i + 1 < len(lines):
            next_line = lines[i+1]
            if next_line.startswith('|') and '---' in next_line:
                in_table = True
                table_header = [line, next_line]
                table_rows = []
                i += 2
                continue

        if in_table:
            if line.startswith('|'):
                table_rows.append(line)
                i += 1
                continue
            else:
                # End of table — sort and flush
                sorted_rows = sorted(table_rows, key=priority_sort_key)
                output.extend(table_header)
                output.extend(sorted_rows)
                in_table = False
                table_header = []
                table_rows = []
                continue

        output.append(line)
        i += 1

    # Flush trailing table
    if in_table and table_rows:
        sorted_rows = sorted(table_rows, key=priority_sort_key)
        output.extend(table_header)
        output.extend(sorted_rows)

    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 sort_priority_tables.py <markdown-file>')
        sys.exit(1)
    sort_tables_in_file(sys.argv[1])
    print('Done — all tables sorted by priority (🔴→🟡→🟢)')
