import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.opc.part import Part
from docx.opc.packuri import PackURI
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches, Pt, RGBColor

BOOK = Path(__file__).parent
OUT = BOOK / "Soulknife.docx"
BODY = "Garamond"
ORNAMENT = "\u2020  \u2020"  # paired daggers


def base(doc):
    s = doc.styles["Normal"]
    s.font.name = BODY
    s.font.size = Pt(11.5)
    pf = s.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.first_line_indent = Inches(0.3)
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.15
    for sec in doc.sections:
        sec.page_width = Inches(6)
        sec.page_height = Inches(9)
        sec.top_margin = sec.bottom_margin = Inches(0.75)
        sec.left_margin = sec.right_margin = Inches(0.75)


FN_BASE = 2


def add_footnote_part(doc, notes):
    W = nsdecls("w")
    footnotes = "".join(
        f'<w:footnote w:id="{fid}"><w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>'
        f'<w:r><w:rPr><w:vertAlign w:val="superscript"/><w:sz w:val="18"/></w:rPr><w:footnoteRef/></w:r>'
        f'<w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t xml:space="preserve"> {txt}</w:t></w:r></w:p></w:footnote>'
        for fid, txt in notes
    )
    xml = (
        f'<w:footnotes {W}>'
        f'<w:footnote w:type="separator" w:id="-1"><w:p><w:r><w:separator/></w:r></w:p></w:footnote>'
        f'<w:footnote w:type="continuationSeparator" w:id="0"><w:p><w:r><w:continuationSeparator/></w:r></w:p></w:footnote>'
        f'{footnotes}</w:footnotes>'
    )
    part = Part(PackURI("/word/footnotes.xml"),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml",
                xml.encode(), doc.part.package)
    doc.part.relate_to(part, RT.FOOTNOTES)


def footnote_ref(p, fid):
    p._p.append(parse_xml(
        f'<w:r {nsdecls("w")}><w:rPr><w:vertAlign w:val="superscript"/></w:rPr>'
        f'<w:footnoteReference w:id="{fid}"/></w:r>'))


def curly(text):
    return re.sub(r'(\s|^)"', lambda m: m.group(1) + "\u201c", text).replace('"', "\u201d")


def runs(p, text, refs):
    # inline **bold** / *italic* / [^N] footnote ref
    for i, chunk in enumerate(re.split(r"(\[\^\d+\])", curly(text))):
        if i % 2:  # odd chunks are [^N] markers
            fid = refs.get(chunk[2:-1])
            if fid is None:
                raise ValueError(f"footnote [^{chunk}] has no definition")
            footnote_ref(p, fid)
            continue
        for part in re.split(r"(\*\*.+?\*\*|\*.+?\*)", chunk):
            if not part:
                continue
            if part.startswith("**"):
                p.add_run(part[2:-2]).bold = True
            elif part.startswith("*"):
                p.add_run(part[1:-1]).italic = True
            else:
                p.add_run(part)


def chapter(doc, num, title, paras, refs):
    doc.add_page_break()
    for txt, size, before in [
        *([("Chapter " + num, 14, 60)] if num else []),
        (title, 22 if num else 18, 60 if num else 80),
        (ORNAMENT, 12, 14),
    ]:
        p = doc.add_paragraph(style="Heading 1" if txt == title else None)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = None
        p.paragraph_format.space_before = Pt(before)
        r = p.add_run(txt)
        r.font.name = BODY
        r.font.size = Pt(size)
        if txt != ORNAMENT:
            r.font.color.rgb = RGBColor(0x40, 0x40, 0x40)
    doc.add_paragraph().paragraph_format.first_line_indent = None
    after_break = False
    for para in paras:
        if para.startswith("> "):  # blockquote: in-world document, indented italic
            q = doc.add_paragraph()
            q.paragraph_format.first_line_indent = None
            q.paragraph_format.left_indent = Inches(0.35)
            q.paragraph_format.space_before = Pt(6)
            q.paragraph_format.space_after = Pt(6)
            r = q.add_run(curly(para[2:]))
            r.italic = True
            after_break = False
            continue
        if para == "---":  # scene break -> blank space
            sp = doc.add_paragraph()
            sp.paragraph_format.first_line_indent = None
            sp.paragraph_format.space_before = Pt(12)
            after_break = True
            continue
        p = doc.add_paragraph()
        if after_break:
            p.paragraph_format.first_line_indent = None
            after_break = False
        runs(p, para, refs)


def centered(doc, lines):
    doc.add_paragraph()
    for txt, size, before in lines:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = None
        p.paragraph_format.space_before = Pt(before)
        r = p.add_run(txt)
        r.font.size = Pt(size)
        if txt.isupper():
            r.bold = True


doc = Document()
base(doc)

title_lines = [l.lstrip("# ").strip() for l in (BOOK / "chapter-00-title.md").read_text().splitlines() if l.strip()]
centered(doc, [(title_lines[0].upper(), 28, 140), (title_lines[1].upper(), 13, 6), (ORNAMENT, 14, 20)])

# map page after the title
if (BOOK / "menzoberranzan-map.png").exists():
    doc.add_page_break()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = None
    p.add_run().add_picture(str(BOOK / "menzoberranzan-map.png"), width=Inches(4.5))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.first_line_indent = None
    r = cap.add_run("Menzoberranzan — map \u00a9 Wizards of the Coast, \u201cMenzoberranzan: City of Intrigue\u201d")
    r.font.size = Pt(8)
    r.italic = True

chapters = []
notes = []  # (footnote id, text) in document order
for f in sorted(BOOK.glob("chapter-*.md")):
    if "title" in f.name:
        continue
    text = f.read_text()
    m = re.match(r"#+\s+(?:Chapter\s+(\d+))?\s*[—–-]?\s*(.+)", text)
    num, name = (m.group(1), m.group(2).strip()) if m and m.group(1) else (None, m.group(2).strip() if m else f.stem)
    defs = dict(re.findall(r"^\[\^(\d+)\]:\s*(.+)$", text, re.M))
    paras = [ln.strip() for ln in text.splitlines()[1:]
             if ln.strip() and not ln.strip().startswith("[^")]
    # assign footnote ids in reading order; markers are per-file, ids are global
    refs = {}
    for para in paras:
        for marker in re.findall(r"\[\^(\d+)\]", para):
            if marker not in refs:
                fid = FN_BASE + len(notes)
                refs[marker] = fid
                notes.append((fid, curly(defs[marker].replace("*", ""))))
    if "readers-guide" in f.name:  # glossary goes at the end
        glossary = (num, name, paras, refs)
        continue
    chapters.append((num, name, paras, refs))

# contents page: just the header; ToC entries are added manually in Google Docs
doc.add_page_break()
centered(doc, [("CONTENTS", 16, 100)])

for num, name, paras, refs in chapters:
    chapter(doc, num, name, paras, refs)

# glossary as back matter, no first-line indent
num, name, paras, refs = glossary
chapter(doc, num, name, paras, refs)
for p in doc.paragraphs[-len(paras):]:
    p.paragraph_format.first_line_indent = None
    p.paragraph_format.space_after = Pt(6)

if notes:
    add_footnote_part(doc, notes)

doc.save(OUT)
print(OUT)