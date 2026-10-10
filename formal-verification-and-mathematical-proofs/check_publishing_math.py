#!/usr/bin/env python3
"""Fail the release if Pandoc or PDF conversion silently drops mathematics."""
import subprocess, sys, zipfile
from xml.etree import ElementTree as ET

if len(sys.argv)!=3: raise SystemExit("usage: check_publishing_math.py paper.docx paper.pdf")
docx,pdf=sys.argv[1:]
with zipfile.ZipFile(docx) as z:
    root=ET.fromstring(z.read("word/document.xml"))
MATH="{http://schemas.openxmlformats.org/officeDocument/2006/math}oMath"
TEXT="{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"
n_math=sum(1 for _ in root.iter(MATH))
literal=[(v.text or "")[:140] for v in root.iter(TEXT) if "$" in (v.text or "")]
assert n_math>=80, f"Insufficient OMML mathematical formulae: {n_math}"
assert not literal, f"Unconverted math appears as literal dollars: {literal[:5]}"
text=subprocess.run(["pdftotext","-layout",pdf,"-"],capture_output=True,text=True,check=True).stdout
assert len(text)>10000, "Unexpectedly short PDF or failed extraction"
assert "ν=3/16" in text or "ν =3/16" in text or "ν = 3/16" in text, "Noise rate mathematical symbol vanished from rendered PDF"
assert "M ≤ 1024" in text or "M ≤1024" in text, "Core finite field inequality absent from rendered PDF"
if "EUROCRYPT_2028" in docx:
    normalized=" ".join(text.lower().split())
    assert "theorem 4.1" in normalized, "New ternary structural theorem absent from PDF"
    assert "corollary 4.1b" in normalized, "New ternary affine-label attack absent from PDF"
    assert "round-4 theorem" in normalized, "Round-4 direction-collision theorem absent from PDF"
    assert "theorem 4.4" in normalized, "Round-4 source/null theorem number absent from PDF"
    assert "0.9972" in normalized, "Round-4 R3 concrete certified gap absent from rendered PDF"
print(f"Publication QA PASSED: {n_math} OfficeMath nodes, zero raw TeX-dollar formulas; correct noisy-field and MDS formulas in PDF")
