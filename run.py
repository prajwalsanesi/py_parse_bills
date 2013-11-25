import glob, os, sys
pdf_files = glob.glob("./*.pdf")
import PARSE_BILLS


for fpdf in pdf_files:
	print PARSE_BILLS.getAmount(fpdf)
