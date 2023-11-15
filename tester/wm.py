import fitz
# from fitz import TextWriter
doc = fitz.open("54.pdf")
page = doc[0]
tw = fitz.TextWriter(page.rect, opacity=0.3)
tw.append((50, 100), "COPY")
page.clean_contents()
page.write_text(rect=page.rect, writers=tw)


# page.add_stamp_annot(page.rect, fitz.STAMP_Draft)
doc.save("new.pdf")
