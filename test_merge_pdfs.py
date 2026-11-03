import pytest
from pypdf import PdfReader, PdfWriter

from merge_pdfs import main, merge_double_sided


def make_pdf(path, widths):
    """Write a PDF of blank pages. Each page width acts as a page label."""
    writer = PdfWriter()
    for width in widths:
        writer.add_blank_page(width=width, height=100)
    writer.write(str(path))
    return str(path)


def page_widths(path):
    return [int(page.mediabox.width) for page in PdfReader(str(path)).pages]


@pytest.fixture
def scans(tmp_path):
    front = make_pdf(tmp_path / "front.pdf", [101, 102, 103])
    back = make_pdf(tmp_path / "back.pdf", [203, 202, 201])  # auto-feed: last back first
    return front, back, tmp_path / "out.pdf"


def test_reverse_back_interleaves_pages_in_order(scans):
    front, back, out = scans
    merge_double_sided(front, back, out, reverse_back=True)
    assert page_widths(out) == [101, 201, 102, 202, 103, 203]


def test_no_reverse_keeps_back_order(scans):
    front, back, out = scans
    merge_double_sided(front, back, out, reverse_back=False)
    assert page_widths(out) == [101, 203, 102, 202, 103, 201]


def test_page_count_mismatch_raises(tmp_path):
    front = make_pdf(tmp_path / "front.pdf", [101, 102])
    back = make_pdf(tmp_path / "back.pdf", [201])
    with pytest.raises(ValueError, match="same number of pages"):
        merge_double_sided(front, back, tmp_path / "out.pdf")


def test_cli_returns_0_on_success(scans):
    front, back, out = scans
    assert main([front, back, str(out)]) == 0
    assert page_widths(out) == [101, 201, 102, 202, 103, 203]


def test_cli_returns_1_on_error(tmp_path, capsys):
    assert main([str(tmp_path / "missing.pdf"), str(tmp_path / "missing.pdf"), str(tmp_path / "out.pdf")]) == 1
    assert "Error:" in capsys.readouterr().err
