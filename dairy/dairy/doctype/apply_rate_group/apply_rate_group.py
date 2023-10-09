# Copyright (c) 2023, Vivek and contributors
# For license information, please see license.txt
# more F U
import frappe
from frappe import _

# import pandas as pd
from datetime import date, timedelta
from frappe.model.document import Document
from datetime import datetime
from datetime import timedelta
from frappe import _

#
# vivek


class ApplyRateGroup(Document):

    # here we have get rate group accocrding to the milk type selected
    @frappe.whitelist()
    def currentrategroup(self):
        doc = frappe.db.get_list("Rate Master")
        for d in doc:
            d1 = frappe.get_doc("Rate Master", d.name)
            if self.milk_type == d1.milk_type and self.branch == d1.branch_id:
                self.rate_group = d.name

                break
                frappe.msgprint("Ther is no rate Group present in branch ")
        # else:
        #     frappe.msgprint("Ther is no rate Group present in branch "+ self.branch +" for milk type "+ self.milk_type + "  ")

    # To get list of all supplier that comes under that branch
    @frappe.whitelist()
    def list(self):
        doc = frappe.db.get_list(
            "Supplier", fields=["supplier_name", "milk_type", "branch_id","name"]
        )
        for d in doc:
            if d.milk_type == self.milk_type and d.branch_id == self.branch:
                self.append(
                    "supplier_list",
                    {
                        "supplier_id": d.name,
                        "supplier_name":d.supplier_name
                    },
                )

    # To change the rate group at supplier side
    @frappe.whitelist()
    def rateapply(self):
        for row in self.get("supplier_list"):
            if row.check:
                doc = frappe.db.get_list("Supplier")
                for d in doc:
                    d1 = frappe.get_doc("Supplier", d.name)
                    if d1.name == row.supplier_id:
                        frappe.db.set_value(
                            "Supplier", d.name, "rate_group", self.rate_group
                        )


                doc = frappe.db.get_list("Data Collection")
                for d in doc:
                    d2=frappe.get_doc("Data Collection",d.name)
                    frappe.msgprint(d2.supplier_id)
                    frappe.msgprint(row.supplier_id)
                    if d2.supplier_id==row.supplier_id:
                        x = self.from_date.split("-")
                        first_date = date(int(x[0]), int(x[1]), int(x[2]))
                        y = self.to_date.split("-")
                        last_date = date(int(y[0]), int(y[1]), int(y[2]))
                        delta = last_date - first_date
                        for j in range(delta.days + 1):
                            day = first_date + timedelta(days=j)
                            if day == d2.date:
                                d3 = frappe.get_doc("Rate Master", self.rate_group)
                                for k in d3.get("rate_list"):
                                    if k.snf == d2.snf and k.fat == d2.fat:
                                        new_rate = k.rate
                                        frappe.db.set_value(
                                            "Data Collection", d.name, "rate", new_rate
                                        )
                                        total_amt = new_rate * d2.litre
                                        frappe.db.set_value(
                                            "Data Collection",
                                            d.name,
                                            "amount",
                                            total_amt,
                                        )
                                        frappe.db.set_value(
                                            "Data Collection",
                                            d.name,
                                            "rate_group",
                                            self.rate_group,
                                        )
                                    # else:
                                    #     frappe.msgprint("Fat or SNF not Matching")

    # To give confirmation to users
    # @frappe.whitelist()
    # def msgapply(self):
    #     count = 0
    #     doc = frappe.db.get_list("Supplier", fields=["supplier_name", "rate_group"])
    #     for d in doc:
    #         # frappe.msgprint(d.supplier_name)
    #         for i in self.get("supplier_list"):
    #             if i.check:
    #                 count = count + 1
    #                 break
    #     if count == 0:
    #         frappe.msgprint(_("please select suppliers"))
    #     else:
    #         frappe.msgprint(_("Apply Successfully"))

    @frappe.whitelist()
    def checkall(self):
        children = self.get('supplier_list')
        if not children:
            return
        all_selected = all([child.check for child in children])  
        value = 0 if all_selected else 1 
        for child in children:
            child.check = value                     

        # for i in self.get("supplier_list"):
        #     if i.check:
        #         i.check = False
        #     else:
        #         i.check = True

        # doc = frappe.db.get_list("Supplier", fields=["supplier_name", "rate_group"])
        # for d in doc:
        # for i in self.get("supplier_list"):
        #     if i.check == False:
        #         i.check = True

                # for i in self.get("supplier_list"):
                #     if i.check==True:
                #         i.check = True
                #     else:
                #         i.check=True


# @frappe.whitelist()
# def shreeram(self):
# 	frappe.msgprint(_("Invalid Age"))

# @frappe.whitelist()
# def vivek(self):
# 	doc=frappe.db.get_list('Rate Master')
# 	for d in doc:
# 		d1=frappe.get_doc('Rate Master',d.name)
# 		if self.branch==d1.branch_id:
# 			self.rate_group=d.name
# 			break

# @frappe.whitelist()
# def abhi(self):
# 	doc=frappe.db.get_list('Rate Master')
# 	for d in doc:
# 		d1=frappe.db.get_list('Rate Master',fields=["milk_type"])
# 		if self.branch==d1.branch_id:
# 			self.milk_type=d1.milk_type
# 			break

# here,
#     if the suppliers

# @frappe.whitelist()
# def msgapply(self):
# 	count=0
# 	doc=frappe.db.get_list('Supplier',fields=['supplier_name','rate_group'])
# 	for d in doc:
# 		for i in self.get("supplier_list"):
# 			if(i.check):
# 				if(d.supplier_name==i.supplier_name):
# 					if(d.rate_group!=self.rate_group):
# 						count= count+1
# 						break
# 			# else:
# 			# 	count+=1
# 	if count==0:
# 		frappe.msgprint(_("Apply Successfully"))
# 	else:
# 		frappe.msgprint(_("Application Failed"))

#  here if the  single suppliers are not selected then it show message "please select suppliers" else it print "Apply Successfully"
