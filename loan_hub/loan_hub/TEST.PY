import pikepdf

pdf_path = "Offer_Letter.pdf"

with pikepdf.open(pdf_path) as pdf:
    # Set creation date to 27th December 2022, 09:00:00
    pdf.docinfo['/CreationDate'] = "D:20221227090000"
    pdf.save("Offer_Letter_Updated.pdf")
