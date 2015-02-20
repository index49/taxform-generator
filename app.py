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
import Cookie


class MainPage(webapp2.RequestHandler):

	def get(self):
		temp_data = {}
		temp_path = 'Templates/index.html'

		# TODO create cookie
		#self.response.set_cookie('name', 'value', expires=

		self.response.out.write(template.render(temp_path, temp_data))
	
	def post(self):

		# TODO if given username, retrieve from database
		if (False):
			inputData = json.load(open('vi.dat'))

		# get input from form
		else:
			inputData = {}
			info = {}
			info['first_name'] = self.request.POST["first_name"]
			info['last_name'] = self.request.POST["last_name"]
			info['address'] = self.request.POST["address"]
			info['city'] = self.request.POST["city"]
			info["state"			] = self.request.POST[	"state"				]
			info["zip"			    ] = self.request.POST[    "zip"			    ]
			info["ss"		        ] = self.request.POST[    "ss"		        ]
			info["spouse_ss"       ] = self.request.POST[    "spouse_ss"       ]
			info["filing_status"   ] = self.request.POST[    "filing_status"   ]
			info["routing_number"  ] = self.request.POST[    "routing_number"  ]
			info["account_number"  ] = self.request.POST[    "account_number"  ]
			info["occupation"	    ] = self.request.POST[    "occupation"	    ]
			inputData["info"] = info
			misc = {}
			misc["real_estate"			] = self.request.POST["misc.real_estate"				]
			misc["mortgage_interest"	] = self.request.POST[    "misc.mortgage_interest"	]
			misc["gifts"				] = self.request.POST[    "misc.gifts"				]
			misc["taxable_interest"	] = self.request.POST[    "misc.taxable_interest"	]
			misc["taxable_refund"	    ] = self.request.POST["misc.taxable_refund"	        ]
			misc["homebuyer_credit"	] = self.request.POST[    "misc.homebuyer_credit"	]
			inputData["misc"] = misc
			w2 = {}
			w2["1"		        ] = self.request.POST[    "w2.1"		        ]
			w2["2"		        ] = self.request.POST[    "w2.2"		        ]
			w2["3"		        ] = self.request.POST[    "w2.3"		        ]
			w2["4"		        ] = self.request.POST[    "w2.4"		        ]
			w2["5"		        ] = self.request.POST[    "w2.5"		        ]
			w2["6"		        ] = self.request.POST[    "w2.6"		        ]
			w2["12a"	        ] = self.request.POST["w2.12a"	                ]
			w2["12b"	        ] = self.request.POST["w2.12b"	                ]
			w2["16"	            ] = self.request.POST["w2.16"	                ]
			w2["17"	            ] = self.request.POST["w2.17"	                ]
			inputData["w2"] = w2

		# create pdf
		self.response.headers['Content-Type'] = 'application/pdf'
		self.response.headers['Content-Disposition'] = 'filename=f1040.pdf'
		outputStream = generate_f1040.generateForm(inputData)
		self.response.write(outputStream.getvalue())


application = webapp2.WSGIApplication([
	('/', MainPage),
], debug=True)
