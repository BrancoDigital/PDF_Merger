from PyPDF2 import PdfReader, PdfWriter
import argparse

def merge_double_sided(front_path, back_path, output_path, reverse_back=True):
    """
    Merge two PDFs representing front and back sides of scanned documents.
    
    Args:
        front_path (str): Path to PDF with front sides (always in ascending order)
        back_path (str): Path to PDF with back sides
        output_path (str): Path where the merged PDF will be saved
        reverse_back (bool): If True, will use back pages in descending order
                           (for auto-feed scanners where backs are in reverse)
    """
    # Create PDF readers for both files
    front_pdf = PdfReader(front_path)
    back_pdf = PdfReader(back_path)
    
    # Verify both PDFs have the same number of pages
    total_pages = len(front_pdf.pages)
    if total_pages != len(back_pdf.pages):
        raise ValueError("Front and back PDFs must have the same number of pages")
    
    # Create a PDF writer for the output
    output = PdfWriter()
    
    for front_index in range(total_pages):
        # Add front page (always in ascending order: 0, 1, 2, ...)
        output.add_page(front_pdf.pages[front_index])
        
        # Add back page
        if reverse_back:
            # Use descending order for backs: last, second-to-last, ...
            back_index = total_pages - 1 - front_index
        else:
            # Use ascending order for backs: 0, 1, 2, ...
            back_index = front_index
            
        output.add_page(back_pdf.pages[back_index])
    
    # Save the merged PDF
    with open(output_path, 'wb') as output_file:
        output.write(output_file)

def main():
    parser = argparse.ArgumentParser(
        description="""Merge two PDFs containing front and back sides of scanned documents.

Typical auto-feed scanner scenario (default behavior):
- Front PDF order: page1_front, page2_front, ..., page11_front
- Back PDF order:  page11_back, page10_back, ..., page1_back
Use --reverse-back (default) to pair them correctly

Manual scanning scenario:
- Front PDF order: page1_front, page2_front, ..., page11_front
- Back PDF order:  page1_back, page2_back, ..., page11_back
Use --no-reverse-back""")
    
    parser.add_argument('front_pdf', help='Path to PDF containing front sides')
    parser.add_argument('back_pdf', help='Path to PDF containing back sides')
    parser.add_argument('output_pdf', help='Path for merged output PDF')
    parser.add_argument('--no-reverse-back', action='store_false', dest='reverse_back',
                      help='Use if back sides are in same order as front sides')
    parser.set_defaults(reverse_back=True)

    args = parser.parse_args()

    try:
        merge_double_sided(args.front_pdf, args.back_pdf, args.output_pdf, args.reverse_back)
        print("PDF successfully merged!")
        if args.reverse_back:
            print("Back pages were used in reverse order")
        else:
            print("Back pages were used in original order")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()