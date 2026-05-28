"""Detailed inspection of docx for remaining 20 questions."""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

import docx

doc = docx.Document(r'E:\Project Peyo Peyo\Project ครูวิทย์\คลังข้อสอบ.docx')
table = doc.tables[0]
rows_from2 = table.rows[2:]

ns_w = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
ns_m = '{http://schemas.openxmlformats.org/officeDocument/2006/math}'

def extract_math_blocks(cell_elem):
    results = []
    for me in cell_elem.findall(f'.//{ns_m}oMath'):
        t_elems = me.findall(f'.//{ns_m}t')
        results.append(''.join(t.text or '' for t in t_elems).strip())
    return results

def extract_math_by_para(cell_elem):
    """Per-paragraph extraction of N. [math] patterns."""
    choices = {}
    for p in cell_elem.findall(f'.//{ns_w}p'):
        plain = ''.join(t.text or '' for t in p.findall(f'.//{ns_w}t')).strip()
        math_texts = []
        for me in p.findall(f'.//{ns_m}oMath'):
            math_texts.append(
                ''.join(t.text or '' for t in me.findall(f'.//{ns_m}t')).strip()
            )
        markers = re.findall(r'([1-5])\.', plain)
        for i, m in enumerate(markers):
            if i < len(math_texts):
                choices[int(m)] = math_texts[i]
    return choices

# Questions with math=5: 40, 48, 55, 61, 65, 70, 72, 85
# Questions with math=6: 77
# Questions with math=7: 89, 94, 100

math_questions = [40, 48, 55, 61, 65, 70, 72, 77, 85, 89, 94, 100]
plain_questions = [45, 62, 97, 98, 109, 117, 123, 142]

print("=== MATH QUESTIONS ===")
for db_num in math_questions:
    row_idx = db_num - 1
    cell = rows_from2[row_idx].cells[1]
    math_blocks = extract_math_blocks(cell._tc)
    para_choices = extract_math_by_para(cell._tc)

    print(f"\nQ{db_num}: math_blocks={len(math_blocks)}")
    for i, mb in enumerate(math_blocks):
        print(f"  block[{i}]: {repr(mb)}")
    if para_choices:
        print(f"  para_choices: {para_choices}")

    # Show each paragraph
    for p_idx, p in enumerate(cell._tc.findall(f'.//{ns_w}p')):
        plain = ''.join(t.text or '' for t in p.findall(f'.//{ns_w}t')).strip()
        has_math = bool(p.findall(f'.//{ns_m}oMath'))
        if plain or has_math:
            print(f"  para[{p_idx}]: {repr(plain[:80])} {'[HAS_MATH]' if has_math else ''}")

print("\n=== PLAIN TEXT QUESTIONS ===")
for db_num in plain_questions:
    row_idx = db_num - 1
    cell = rows_from2[row_idx].cells[1]
    print(f"\nQ{db_num}: full_text=")
    print(repr(cell.text[:500]))
    print("  paragraphs:")
    for p_idx, p in enumerate(cell._tc.findall(f'.//{ns_w}p')):
        plain = ''.join(t.text or '' for t in p.findall(f'.//{ns_w}t')).strip()
        if plain:
            print(f"  para[{p_idx}]: {repr(plain[:100])}")
