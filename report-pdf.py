import pymupdf

def generate_report(images, output_file):

    # convert the first image into a pdf file
    jpg = pymupdf.open(images[0])
    pdfbytes = jpg.convert_to_pdf()
    pdf = pymupdf.open("pdf", pdfbytes)

    # insert cover page with text
    cover_page = pdf.new_page(0, width = 595, height = 842)
    cover_page.insert_text(pymupdf.Point(50, 72),
                           "Report",
                           fontname = 'helv',
                           fontsize = 20,
                           rotate = 0)
    
    # save report
    pdf.save("report.pdf")

# run the report
generate_report(["temp/test_image.jpg"])