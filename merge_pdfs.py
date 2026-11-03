import argparse
import sys

from pypdf import PdfReader, PdfWriter


def merge_double_sided(front_path, back_path, output_path, reverse_back=True):
    """
    Merge two PDFs representing front and back sides of scanned documents.

    Args:
        front_path (str): Path to PDF with front sides (always in ascending order)
        back_path (str): Path to PDF with back sides
        output_path (str): Path where the merged PDF will be saved
        reverse_back (bool): If True, will use back pages in descending order
                           (for auto-feed scanners where backs are in reverse)

    Raises:
        ValueError: If the two PDFs do not have the same number of pages.
    """
    front_pdf = PdfReader(front_path)
    back_pdf = PdfReader(back_path)

    total_pages = len(front_pdf.pages)
    if total_pages != len(back_pdf.pages):
        raise ValueError(
            f"Front and back PDFs must have the same number of pages "
            f"(front has {total_pages}, back has {len(back_pdf.pages)})"
        )

    output = PdfWriter()
    for front_index in range(total_pages):
        output.add_page(front_pdf.pages[front_index])
        # Auto-feed scanners return the backs last-to-first.
        back_index = total_pages - 1 - front_index if reverse_back else front_index
        output.add_page(back_pdf.pages[back_index])

    with open(output_path, "wb") as output_file:
        output.write(output_file)


def main(argv=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""Merge two PDFs containing front and back sides of scanned documents.

Typical auto-feed scanner scenario (default behavior):
- Front PDF order: page1_front, page2_front, ..., page11_front
- Back PDF order:  page11_back, page10_back, ..., page1_back

Manual scanning scenario:
- Front PDF order: page1_front, page2_front, ..., page11_front
- Back PDF order:  page1_back, page2_back, ..., page11_back
Use --no-reverse-back""",
    )
    parser.add_argument("front_pdf", help="Path to PDF containing front sides")
    parser.add_argument("back_pdf", help="Path to PDF containing back sides")
    parser.add_argument("output_pdf", help="Path for merged output PDF")
    parser.add_argument(
        "--no-reverse-back",
        action="store_false",
        dest="reverse_back",
        help="Use if back sides are in same order as front sides",
    )
    args = parser.parse_args(argv)

    try:
        merge_double_sided(args.front_pdf, args.back_pdf, args.output_pdf, args.reverse_back)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print("PDF successfully merged!")
    print(f"Back pages were used in {'reverse' if args.reverse_back else 'original'} order")
    return 0


if __name__ == "__main__":
    sys.exit(main())
