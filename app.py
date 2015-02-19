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
		if (False):
			inputData = json.load(open('vi.dat'))

		# get input from form
		else:
			inputData = {}
			inputData['first_name'] = self.request.POST["first_name"]
			inputData['last_name'] = self.request.POST["last_name"]
			inputData['address'] = self.request.POST["address"]
			inputData['city'] = self.request.POST["city"]
			inputData["state"			] = self.request.POST[	"state"				]
			inputData["zip"			    ] = self.request.POST[    "zip"			    ]
			inputData["ss"		        ] = self.request.POST[    "ss"		        ]
			inputData["spouse_ss"       ] = self.request.POST[    "spouse_ss"       ]
			inputData["filing_status"   ] = self.request.POST[    "filing_status"   ]
			inputData["routing_number"  ] = self.request.POST[    "routing_number"  ]
			inputData["account_number"  ] = self.request.POST[    "account_number"  ]
			inputData["occupation"	    ] = self.request.POST[    "occupation"	    ]
			inputData["real_estate"			] = self.request.POST["real_estate"				]
			inputData["mortgage_interest"	] = self.request.POST[    "mortgage_interest"	]
			inputData["gifts"				] = self.request.POST[    "gifts"				]
			inputData["taxable_interest"	] = self.request.POST[    "taxable_interest"	]
			inputData["taxable_refund"	    ] = self.request.POST["taxable_refund"	        ]
			inputData["homebuyer_credit"	] = self.request.POST[    "homebuyer_credit"	]
			inputData["box_1"		        ] = self.request.POST[    "box_1"		        ]
			inputData["box_2"		        ] = self.request.POST[    "box_2"		        ]
			inputData["box_3"		        ] = self.request.POST[    "box_3"		        ]
			inputData["box_4"		        ] = self.request.POST[    "box_4"		        ]
			inputData["box_5"		        ] = self.request.POST[    "box_5"		        ]
			inputData["box_6"		        ] = self.request.POST[    "box_6"		        ]
			inputData["box_12a"	            ] = self.request.POST["box_12a"	                ]
			inputData["box_12b"	            ] = self.request.POST["box_12b"	                ]
			inputData["box_16"	            ] = self.request.POST["box_16"	                ]
			inputData["box_17"	            ] = self.request.POST["box_17"	                ]

		# create pdf
		self.response.headers['Content-Type'] = 'application/pdf'
		self.response.headers['Content-Disposition'] = 'attachment;filename=f1040.pdf'
		outputStream = generate_f1040.generateForm(inputData)
		self.response.write(outputStream.getvalue())


application = webapp2.WSGIApplication([
	('/', MainPage),
], debug=True)
