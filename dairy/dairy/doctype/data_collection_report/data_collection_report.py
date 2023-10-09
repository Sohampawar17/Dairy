# Copyright (c) 2023, Vivek and contributors
# For license information, please see license.txt


import frappe
from frappe import _
# import pandas as pd
from datetime import date,timedelta
from frappe.model.document import Document
from datetime import datetime
from datetime import timedelta


class DataCollectionReport(Document):
	# To Get last Date from Start Date 
	@frappe.whitelist()	
	def date(self):
		doc=frappe.db.get_list('Dairy Branch',
		fields=['bill_period','branch_name'])
		for d in doc:
			if(d.branch_name==self.branch_name):
				Begindatestring = self.first_date
				Begindate = datetime.strptime(Begindatestring, "%Y-%m-%d")
				Enddate = Begindate + timedelta(days=int(d.bill_period))
				self.last_date=Enddate
				

	
	#To get Supplier List
	@frappe.whitelist()	
	def list(self):
		doc=frappe.db.get_list('Supplier',fields=['supplier_name','branch_id'])
		for d in doc:
			if(d.branch_id == self.branch_id):	
				self.append("supplier_list",{
				"supplier_name":d.supplier_name,
				}) 	
    
	@frappe.whitelist()
	def checkall(self):
		# doc = frappe.db.get_list("Supplier", fields=["supplier_name"])
		
		for i in self.get("supplier_list"):
			if i.check ==False:
				i.check=True




    #To Collect Data from Data Collection Doctype
	@frappe.whitelist()	
	def append_to_bill_child(self):
		count=0 
		litre_count=0
		doc=frappe.db.get_list('Data Collection',
		fields=['shift','date','amount','supplier_id','milk_type','fat','snf','rate','litre']
		)
		
		for d in doc:
			for row in self.get("supplier_list"):
				if(row.check):	
					if(d.supplier_id == row.supplier_name):
						x=self.first_date.split("-")
						first_date = date(int(x[0]),int(x[1]),int(x[2]))
						y=self.last_date.split("-")
						last_date = date(int(y[0]),int(y[1]),int(y[2]))
						delta  = last_date - first_date
						for i in range(delta.days +1):
							day = first_date + timedelta(days=i)
							if(day==d.date):
								# frappe.msgprint(_("for date {0}, the amount is {1}").format(d.date,d.amount))
								count+=d.amount
								litre_count+=d.litre
								self.append("bill_child",{
											"shift":d.shift,
											"date":d.date,
											"supplier_name":d.supplier_id,
											"milk_type":d.milk_type,
											"fat":d.fat,
											"snf":d.snf,
											"litre":d.litre,
											"rate":round(float(d.rate),2),
											"total":round(d.amount,2)
					
					})	
		self.total=round(count,2)
		self.total_litre=round(litre_count,2)
