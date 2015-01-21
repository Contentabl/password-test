import base64, httplib
import xml.etree.ElementTree as ET

BREAKFAST_COST = 20
LUNCH_COST = 25
DINNER_COST = 32
SNACKS_COST = 10
DESSERT_COST = 12
DELIVERY_COST = 29

"""
THESE FUNCTIONS ARE USED TO ACCESS Freshbooks
"""


# test script created to connect with my test Freshbooks account
def send_xml(xml):
	headers = {}
	body = '/api/2.1/xml-in'
	headers["Authorization"] = "Basic {0}".format(
	    base64.b64encode("{0}:{1}".format('27c32aad469c6d0828b2f6c1e52e7547', 'user')))
	headers["Content-type"] = "application/xml"


	# Enable the job
	conn = httplib.HTTPSConnection('mealstoheal.freshbooks.com')
	conn.request('POST', body, xml, headers)
	resp = conn.getresponse()
	return resp

def create_user(email, name):

	XML = """\
	<?xml version="1.0" encoding="utf-8"?>  
	<request method="client.create">  
	  <client>  
	    <first_name>""" + name + """</first_name>  
	    <email>""" + email + """</email>  
	  </client>  
	</request>"""

	resp = send_xml(XML).read()
	print resp
	root = ET.fromstring(resp)
	fbid = root[0].text
	print fbid
	return fbid

def delete_freshbookuser(fbid):
	if not fbid:
		fbid = 0
	XML = """\
	<?xml version="1.0" encoding="utf-8"?>  
	<request method="client.delete">  
	  <client_id>""" + str(fbid) + """</client_id>  
	</request>"""
	resp = send_xml(XML).read()
	root = ET.fromstring(resp)
	print root.get('status')
	return root.get('status')

def client_list():

	XML = """\
	<?xml version="1.0" encoding="utf-8"?>  
	<request method="client.list">   
	</request>"""
	resp = send_xml(XML).read()
	print resp
	root = ET.fromstring(resp)
	print root
	print root[0][0][0].text
	return "ok"

def create_invoice(meals,fbid):

	XML = """\
	<?xml version="1.0" encoding="utf-8"?>
	<request method="invoice.create">  
	  <invoice>  
	    <client_id>""" + str(fbid) + """</client_id>
	    <lines>"""
	if meals['breakfasts'] != 0:
		XML += """\  
	      <line>  
	        <name>Breakfast</name>
	        <unit_cost>""" + str(BREAKFAST_COST) + """</unit_cost>
	        <quantity>""" + str(meals['breakfasts']) + """</quantity> 
	      </line>"""
	if meals['lunches'] != 0:
		XML += """\  
	      <line>  
	        <name>Lunch</name>  
	        <unit_cost>""" + str(LUNCH_COST) + """</unit_cost>
	        <quantity>""" + str(meals['lunches']) + """</quantity> 
	      </line>"""

	if meals['dinners'] != 0:
		XML += """\  
	      <line>  
	        <name>Dinner</name>
	        <unit_cost>""" + str(DINNER_COST) + """</unit_cost>
	        <quantity>""" + str(meals['dinners']) + """</quantity> 
	      </line>"""
	if meals['snacks'] != 0:
		XML += """\  
	      <line>  
	        <name>Snacks</name>
	        <unit_cost>""" + str(SNACKS_COST) + """</unit_cost>
	        <quantity>""" + str(meals['snacks']) + """</quantity> 
	      </line>"""
	if meals['desserts'] != 0:
		XML += """\  
	      <line>  
	        <name>Dessert</name>
	        <unit_cost>""" + str(DESSERT_COST) + """</unit_cost>
	        <quantity>""" + str(meals['desserts']) + """</quantity> 
	      </line>"""

	XML += 	"""<line>  
	        <name>Delivery</name>
	        <unit_cost>""" + str(DELIVERY_COST) + """</unit_cost>
	        <quantity>1</quantity> 
	      </line>"""

	XML +=   """</lines>  
	  </invoice>  
	</request>"""

	resp = send_xml(XML).read()
	print resp
	root = ET.fromstring(resp)
	return root.get('status')

