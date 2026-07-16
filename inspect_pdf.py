print("Script started")

from app.services.pdf_inspector import inspect_pdf

print("Import successful")

inspect_pdf("data/ct200_manual.pdf")

print("Finished")