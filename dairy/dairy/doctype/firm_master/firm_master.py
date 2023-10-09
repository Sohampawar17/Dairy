# Copyright (c) 2023, vivek and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class FirmMaster(Document):
	def before_save(self):
		pass
