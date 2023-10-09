import frappe
from frappe.model.document import Document

class VariableDeduction(Document):
    pass
		# @frappe.whitelist()
		# def on_submit(self):
		# 	doc=frappe.new_doc('GL Entry')
		# 	doc.posting_date=self.date
		# 	doc.account=self.accountdr
		# 	doc.party_type="Supplier"
		# 	doc.party=self.supplier
		# 	doc.cost_center="Main - QT"
		# 	doc.debit=self.deduction_amount
		# 	doc.debit_in_account_currency=self.deduction_amount
		# 	doc.against=self.accountcr
		# 	doc.voucher_type="Deduction Master"
		# 	doc.voucher_no=self.name
		# 	doc.insert()

		# 	doc=frappe.new_doc('GL Entry')
		# 	doc.posting_date=self.date
		# 	doc.account=self.accountcr
		# 	doc.cost_center="Main - QT"
		# 	doc.credit=self.deduction_amount
		# 	doc.credit_in_account_currency=self.deduction_amount
		# 	doc.against=self.supplier
		# 	doc.voucher_type="Deduction Master"
		# 	doc.voucher_no=self.name
		# 	doc.insert()


		# 	doc=frappe.new_doc('Total Deduction Amount')
		# 	doc.supplier_name=self.supplier
		# 	doc.total_deduction_amount=self.deduction_amount
		# 	doc.date=self.date
		# 	doc.flag="Deduction Master"
		# 	doc.insert()





# -----------------------------------------------------------------------------------
# import frappe
# from frappe.model.document import Document

# class VariableDeduction(Document):
#     def before_save(self):
#         journal_entry = frappe.new_doc("Journal Entry")
#         journal_entry.posting_date = self.date
#         journal_entry.company = "QUANTBIT TECHNOLOGY"
#         #journal_entry.remark = "Deduction Master {0}".format("Deduction Master")
#         journal_entry.append("accounts", {
#             "account": self.accountdr,
#             "debit_in_account_currency": self.deduction_amount,
#             "party_type": "Supplier",
#             "party": self.supplier,
#             "is_advance":"Yes"
#         })
#         journal_entry.append("accounts", {
#             "account": self.accountcr,
#             "credit_in_account_currency": self.deduction_amount,
#             "party_type": "Supplier",
#             "party": self.supplier
#         })
#         journal_entry.save()
#         journal_entry.submit()
#         self.journal_entry = journal_entry.name
# -------------------------------------------------------------------------------------------
# import frappe
# from frappe.model.document import Document

# class VariableDeduction(Document):
# 	def before_save(self):
# 		journal_entry = frappe.get_doc({
# 			"doctype": "Journal Entry",
# 			"posting_date": self.date,
# 			"company": "QUANTBIT TECHNOLOGY",
# 			"accounts": [
# 				{
# 					"account": self.accountdr,
# 					"debit_in_account_currency": self.deduction_amount,
# 					"party_type": "Supplier",
# 					"party": self.supplier,
# 					"is_advance":"Yes"
# 				},
# 				{
# 					"account": self.accountcr,
# 					"credit_in_account_currency": self.deduction_amount,
# 					"party_type": "Supplier",
# 					"party": self.supplier
# 				}
# 			]
# 		})
# 		journal_entry.submit()
# 		self.journal_entry = journal_entry.name
# 		self.save()

# # -------------------------------------------------------------------------------------------------------------------------
# import frappe
# from frappe.model.document import Document

# class VariableDeduction(Document):
# 	def before_save(self):
# 		journal_entry = frappe.get_doc({
# 			"doctype": "Journal Entry",
# 			"posting_date": self.date,
# 			"company": "QUANTBIT TECHNOLOGY",
# 			"accounts": [
# 				{
# 					"account": self.accountdr,
# 					"debit_in_account_currency": self.deduction_amount,
# 					"party_type": "Supplier",
# 					"party": self.supplier,
# 					"is_advance":"Yes"
# 				},
# 				{
# 					"account": self.accountcr,
# 					"credit_in_account_currency": self.deduction_amount,
# 					"party_type": "Supplier",
# 					"party": self.supplier
# 				}
# 			]
# 		})
# 		journal_entry.submit()
# 		self.journal_entry = journal_entry.name

# -------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------
# Copyright (c) 2023, vivek and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document

# class VariableDeduction(Document):
# 	def before_save(self):
# 		journal_entry = frappe.new_doc("Journal Entry")
# 		journal_entry.posting_date = self.date
# 		journal_entry.company = "QUANTBIT TECHNOLOGY"
# 		#journal_entry.remark = "Deduction Master {0}".format("Deduction Master")
# 		journal_entry.append("accounts", {
# 			"account": self.accountdr,
# 			"debit_in_account_currency": self.deduction_amount,
# 			"party_type": "Supplier",
# 			"party": self.supplier,
# 			"is_advance":"Yes"
# 		})
# 		journal_entry.append("accounts", {
# 			"account": self.accountcr,
# 			"credit_in_account_currency": self.deduction_amount,
# 			"party_type": "Supplier",
# 			"party": self.supplier
# 		})
# 		journal_entry.save()
# 		journal_entry.submit()
# 		self.journal_entry = journal_entry.name
# 		self.save()
		
# 		frappe.db.commit()
# ------------------------------------------------------------------------------------------------------------------------

 	# frappe.whitelist()
	# def avanti(self):
	# 	self.new_document()
		# self.account_dr()
		# self.account_cr()

	# @frappe.whitelist()
	# def avantii(self):
	# # 	doc=frappe.new_doc('Total Deduction Amount')
	# # 	doc.supplier_name=self.supplier
	# # 	doc.total_deduction_amount=self.deduction_amount
	# # 	doc.date=self.date
	# # 	doc.flag="Deduction Master"
	# # 	doc.insert()

	# # def account_dr(self):
	# 	doc=frappe.new_doc('GL Entry')
	# 	doc.posting_date=self.date
	# 	doc.account=self.accountdr
	# 	# doc.party_type=
	# 	# doc.party=
	# 	# doc.cost_center=
	# 	doc.debit=self.deduction_amount
	# 	# doc.credit=
	# 	# doc.account_currency=
	# 	doc.debit_in_account_currency=self.deduction_amount
	# 	# doc.credit_in_account_currency=
	# 	doc.against=self.accountcr
	# 	doc.voucher_type="Deduction Master"
	# 	doc.voucher_no=self.name
	# 	# doc.is_opening=
	# 	# doc.is_advance=
	# 	# doc.fiscal_year=
	# 	# doc.company=
	# 	# doc.is_cancelled=
	# 	doc.insert()

	# def account_cr(self):
	# 	doc=frappe.new_doc('Total Deduction Amount')
	# 	doc.supplier_name=self.supplier
	# 	doc.total_deduction_amount=self.deduction_amount
	# 	doc.date=self.date
	# 	doc.flag="Deduction Master"
	# 	doc.insert()



