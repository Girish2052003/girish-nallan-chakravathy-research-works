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
    # Mathematics glyph fallback: LibreOffice formerly substituted red
    # inverted question marks in the archived nonzero-vector expression.
    assert "¿" not in text and "¡" not in text, "Mathematics glyph fallback in rendered PDF"

    normalized=" ".join(text.lower().split())
    assert "theorem 4.1" in normalized, "New ternary structural theorem absent from PDF"
    assert "corollary 4.1b" in normalized, "New ternary affine-label attack absent from PDF"
    assert "round-4 theorem" in normalized, "Round-4 direction-collision theorem absent from PDF"
    assert "theorem 4.4" in normalized, "Round-4 source/null theorem number absent from PDF"
    assert "0.9972" in normalized, "Round-4 R3 concrete certified gap absent from rendered PDF"
    assert "theorem 9.2" in normalized, "Round-5 public-decapsulation theorem missing in rendered PDF"
    assert "theorem 4.5" in normalized, "Round-6 second-difference subspace theorem absent from published PDF"
    assert "theorem 4.6" in normalized, "Round-7 public local right-inversion theorem not in PDF"
    assert "theorem 4.7" in normalized, "Round-7 constant-derivative subspace bound not in PDF"
    assert "3.39402" in normalized, "Round-7 finite R3 bound absent from rendered PDF"
    assert "3.62169" in normalized, "Round-6 R2 exact probability bound absent from published PDF"
    assert "shared-key recovery" in normalized, "Round-5 end-to-end KEM attack missing in rendered PDF"
print(f"Publication QA PASSED: {n_math} OfficeMath nodes, zero raw TeX-dollar formulas; correct noisy-field and MDS formulas in PDF")
