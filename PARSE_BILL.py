import pyPdf

def tryPasswd(path, pwds):
	fp = file(path, "rb")
	pdf = pyPdf.PdfFileReader(fp)
	ret = 0
	for p in pwds:
		try:
			ret = pdf.decrypt(p)
		except:
			pass
		if ret==1:
			return p
	return None


def getInfo(path, pwd):
	content = ""
	num_pages = 1
	p = file(path, "rb")
	pdf = pyPdf.PdfFileReader(p)
	try:
		ret = pdf.decrypt(pwd)
	except:
		#return '"'+path+'",'+'Unicode error '+pwd
		return '',
	if ret == 0:
		#return '"'+path+'",'+'Invalid password '+pwd
		return '',
	#print pdf.getDocumentInfo()
	#print pdf.getPage(3)
	voda_details = pdf.getPage(2).extractText().encode("ascii", "ignore")
	#print pwd,path
	#print 'pg[2]',pdf.getPage(2).extractText().encode("ascii", "ignore")
	return '"'+path+'",'+parse_voda2(voda_details)

def getAmount(pdf_file):
	p = file(pdf_file, "rb")
	pdf = pyPdf.PdfFileReader(p)
	airtel_details = pdf.getPage(0).extractText().encode("ascii", "ignore")
	#print '"'+pdf_file+'",'+airtel_details
	return parse_airtel(airtel_details)

import re
def parse_airtel(text):
	#airtel_re = 'Near Bridge(.+)security'
	airtel_re = 'amount due on or=\+-(.+)Near Bridge(\d{10})(\d+)(\d\d-...-\d\d\d\d)(\d+\.\d\d)(\d+\.\d\d)(\d+\.\d\d)(\d+\.\d\d)(\d+\.\d\d)(\d\d-...-\d\d\d\d)to(\d+)monthly charges(\d\d-...-\d\d\d\d).+Nivaata.+(\d\d-...-\d\d\d\d)`  ([0-9,\.]+)'
	#airtel_re = 'this month\'s charges.+`([\d,\.]+).+monthly charges(..-...-....)airtel number(\d+).+Limited(..-...-....)'
	match = re.search(airtel_re, text, flags=re.DOTALL)
	if match is not None:
		csv = match.groups()
		strn = str(csv)
		return strn[1:-1]
		#return '"'+csv[0]+'","'+csv[1]+'",'+csv[2]
	return 'Invalid Bill'
	
def parse_voda2(text):
	voda_re = 'details(.+?)Vodafone no.(\d+).+Total([\d\.]+)Note'
	match = re.search(voda_re, text)
	if match is not None:
		csv = match.groups()
		#strn = str(csv)
		return '"'+csv[0]+'","'+csv[1]+'",'+csv[2]
	return 'Invalid Bill'
