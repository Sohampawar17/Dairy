# Copyright (c) 2023, vivek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class VendorRegistration(Document):
	def before_save(self):
		aadhar_list = frappe.get_all('Vendor Registration',filters={'aadhar_card': self.aadhar_card, 'name': ['!=', self.name]},fields ={'name','name1'})
		if aadhar_list:
			frappe.throw(f"Aadhar number must be unique aadhar Exist for vender '{aadhar_list[0].name1}'")

		exist_supp=frappe.get_all("Supplier",filters={"name":self.name})
		if(not exist_supp):
			doc=frappe.new_doc("Supplier")
			doc.supplier_type=self.supplier_type
			doc.supplier_group=self.vendor_group
			doc.supplier_name=self.name1
			doc.branch=self.branch
			doc.insert()
			self.supplier_doc=doc.name
			doc.save()
			frappe.db.set_value("Supplier",str(self.supplier_doc),"name",self.name)
		
			cust=frappe.new_doc("Customer")
			cust.customer_type=self.supplier_type
			cust.customer_group=self.vendor_group
			cust.customer_name=self.name1
			cust.branch=self.branch
			cust.territory="India"
			cust.insert()
			self.customer_doc=cust.name
			cust.save()
			frappe.db.set_value("Customer",str(self.customer_doc),"name",self.name)

			q=frappe.new_doc('Address')
			q.address_type="Billing"
			q.address_title=self.name 
			q.country="India"
			q.gst_category="Unregistered"
			q.pincode=self.pin_code
			q.address_line1 =self.village
			q.address_line2 =self.taluka
			q.city=self.district
			q.state=self.state
			q.append(
							"links",
							{
								"link_doctype": "Supplier",
								"link_name": self.name,
								"link_title": "",
								
							},
						)
			q.append(
							"links",
							{
								"link_doctype": "Customer",
								"link_name": self.name,
								"link_title": "",
								
							},
						)
			q.insert()
			qoc=q.name
			frappe.db.set_value("Supplier", self.name, "supplier_primary_address", qoc)
			frappe.db.set_value("Supplier", self.name, "primary_address", f"{self.village}\n{self.taluka}\n{self.district}\n{self.state}\n India")
			frappe.db.set_value("Customer",self.name, "customer_primary_address", qoc)
			frappe.db.set_value("Customer", self.name, "primary_address", f"{self.village}\n{self.taluka}\n{self.district}\n{self.state}\n India") 
		else:
			supplier_values = {
					"primary_address":f"{self.village}\n{self.taluka}\n{self.district}\n{self.state}\n India",
					"supplier_type": self.supplier_type,
					"supplier_name": self.name1,
					"supplier_group": self.vendor_group,
					"branch": self.branch,
				}
			frappe.db.set_value("Supplier", self.name, supplier_values)
			
			customer_value={
				"primary_address":f"{self.village}\n{self.taluka}\n{self.district}\n{self.state}\n India",
				"customer_name": self.name1,
				"customer_group": self.vendor_group,
				"branch": self.branch,
				"territory":"India"
			}
			frappe.db.set_value("Customer",self.name,customer_value)

			address_value={
				"address_line1":self.village,
				"address_line2":self.taluka,
				"city":self.district,
				"state":self.state,
				"country":"India",
				"pincode":self.pin_code
			}
			frappe.db.set_value("Customer",self.name+"-Billing",address_value)

	def on_trash(self):
		frappe.delete_doc("Supplier",self.name)
		frappe.delete_doc("Customer",self.name)
		
