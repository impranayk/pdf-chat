from pypdf import PdfReader

reader = PdfReader("HR_Policy.pdf")
print(len(reader.pages), "pages")

page4 = reader.pages[3].extract_text()
print(page4[:200])
