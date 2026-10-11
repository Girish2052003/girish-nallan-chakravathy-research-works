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
# Poppler/LibreOffice versions differ in spaces around mathematical operators.
# Normalize whitespace only; retain every symbol and number in these checks.
compact="".join(text.split())
assert "ν=3/16" in compact, "Noise rate mathematical symbol vanished from rendered PDF"
assert "M≤1024" in compact, "Core finite field inequality absent from rendered PDF"
# Apply the glyph gate to BOTH publications. The short archive also contained
# broken set-difference and floor delimiters under newer LibreOffice builds.
badpos=next((i for i,ch in enumerate(text) if ch in "¿¡"),None)
assert badpos is None, f"Mathematics glyph fallback in rendered PDF near: {text[max(0,badpos-160):badpos+160]!r}"
if "EUROCRYPT_2028" in docx:
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
    assert "corollary 4.6a" in normalized, "Round-7 public fiber translation corollary missing"
    assert "3.39402" in normalized, "Round-7 finite R3 bound absent from rendered PDF"
    assert "theorem 12.9" in normalized, "Round-8 public global CSP theorem missing from rendered PDF"
    assert "public global witness" in normalized, "Round-8 adversary claim missing from rendered PDF"
    assert "overlap alone" in normalized, "Round-8 negative security boundary missing from rendered PDF"
    assert "lemma 1.1" in normalized, "Key-indistinguishability security target missing from rendered PDF"
    assert "theorem 4.8" in normalized, "Public oracle inversion theorem missing from rendered PDF"
    assert "corollary 4.8a" in normalized, "Uniform public fiber sampler missing from rendered PDF"
    assert "corollary 4.8b" in normalized, "Scoped local KEM correctness-to-recovery result missing from PDF"
    assert "theorem 12.10" in normalized, "Global constant-shift criterion missing from rendered PDF"
    assert "11,678" in normalized, "Public oracle reproduction count missing from rendered PDF"
    # A renderer may wrap between "machine-" and "checked". Strip only
    # whitespace here, retaining every letter and the literal hyphen.
    assert "nomachine-checked" in compact.lower(), "Follow-up verification limitation missing from rendered PDF"
    assert "3.62169" in normalized, "Round-6 R2 exact probability bound absent from published PDF"
    assert "shared-key recovery" in normalized, "Round-5 end-to-end KEM attack missing in rendered PDF"
if "SG_DIFRA_REVISED" in docx:
    normalized=" ".join(text.lower().split())
    assert "appendix c." in normalized, "Short revised PDF missing Round-8 appendix"
    assert "round-8" in normalized, "Round-8 scientific status absent from revised PDF"
    assert "appendix d." in normalized, "Short revised PDF missing October 11 follow-up"
    assert "corollaries 4.8" in normalized, "Short revised PDF missing follow-up theorem pointers"
print(f"Publication QA PASSED: {n_math} OfficeMath nodes, zero raw TeX-dollar formulas; correct noisy-field and MDS formulas in PDF")
