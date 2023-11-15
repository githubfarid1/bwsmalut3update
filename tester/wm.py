import fitz
# from fitz import TextWriter
doc = fitz.open("2.pdf")
page = doc[0]
tw = fitz.TextWriter(page.rect, opacity=0.3)
tw.append((50, 100), "COPY BWS")
page.clean_contents(sanitize=False)
page.write_text(rect=page.rect, writers=tw)
doc.save("new.pdf")
