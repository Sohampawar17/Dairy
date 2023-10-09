# Copyright (c) 2023, vivek and contributors
# For license information, please see license.txt

import datetime
import frappe
from frappe.model.document import Document

class MilkCollection(Document):
	@frappe.whitelist() 
	def calculate_data(self):
		self.get_document()

	#To calculate Total Amount 
	def get_document(self):
		count=0
		doc = frappe.get_doc('Rate Master', self.rate_group)
		for row in doc.get("rate_list"):
			if ((self.snf == row.snf) and (self.fat == row.fat)):
				self.rate = row.rate
				self.amount=self.litre*self.rate
				count+=1
		if(count==0):
			frappe.msgprint("Please Enter Right SNF or Fat value") 

	# To get Current shift
	@frappe.whitelist()
	def current_shift(self):
		now = datetime.datetime.now()
		p = now.strftime("%H%M%S")
		k = int(p)
		if 000000 <= k <= 115959:
			self.shift = "Morning"
		else:
			self.shift = "Evening"

	@frappe.whitelist()
	def get_rete_group(self):
		doc=frappe.get_all("Rate Master",filters={"milk_type":self.milk_type})
		for d in doc:
			self.rate_group=d.name


