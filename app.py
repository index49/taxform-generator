import webapp2
import cgi
from google.appengine.ext.webapp import template
from PyPDF2 import PdfFileWriter, PdfFileReader
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import json
import generate_f1040


class MainPage(webapp2.RequestHandler):

	def get(self):
		temp_data = {}
		temp_path = 'Templates/index.html'
		self.response.out.write(template.render(temp_path, temp_data))
	
	def post(self):

		# TODO if given username, retrieve from database
		#inputData = json.load(open('vi.dat'))

		# get input from form
		inputData = {}
		inputData['first_name'] = self.request.POST["first_name"]
		inputData['last_name'] = self.request.POST["last_name"]
		inputData['address'] = self.request.POST["address"]

		# create pdf
		self.response.headers['Content-Type'] = 'application/pdf'
		self.response.headers['Content-Disposition'] = 'attachment;filename=f1040.pdf'
		outputStream = generate_f1040.generateForm(inputData)
		self.response.write(outputStream.getvalue())


application = webapp2.WSGIApplication([
	('/', MainPage),
], debug=True)
