import pymupdf
from datetime import date

def generate_report(body1, images, output_file):

    # convert the first image into a pdf file
    jpg = pymupdf.open(images[0])
    pdfbytes = jpg.convert_to_pdf()
    pdf = pymupdf.open("pdf", pdfbytes)

    # insert cover page with text
    cover_page = pdf.new_page(0, width = 595, height = 842)
    cover_page.insert_text(pymupdf.Point(50, 100),
                           "The Best Countries by Coffee Quality",
                           fontname = 'helv',
                           fontsize = 20,
                           rotate = 0)
    cover_page.insert_text(pymupdf.Point(400, 72),
                           f"{date.today()}",
                           fontname = 'helv',
                           fontsize = 13,
                           rotate = 0)

    # write body
    rect = pymupdf.Rect(60, 150, 535, 800)
    cover_page.insert_htmlbox(rect, body1, css="* {font-family: halv; font-size:12px;}")

    # delete the initial image
    pdf.delete_page(-1)

    # add remaining images
    for i in range (0, len(images)):
        new_page = pdf.new_page(-1, width = 842, height = 595)
        new_page.insert_image(pymupdf.Rect(0, 0, 842, 595),
                              filename=f"{images[i]}")
    
    # save report
    pdf.save(output_file)

# run the report
# generate_report(f"<b>THis was a report {52}</b> THis was a report {52}THis was a report {52}THis was a report {52}THis was a report {52}THis was a report {52}THis was a report {52}THis was a report {52}THis was a report {52}", ["temp/test_image.jpg", "temp/test_image.jpg", "temp/test_image.jpg"], "report.pdf")