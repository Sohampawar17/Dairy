        # Copyright (c) 2023, Vivek and contributors
import frappe
from frappe import _

# import pandas as pd
from datetime import date 
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta
from frappe.model.document import Document
from datetime import datetime
from datetime import timedelta
from collections import defaultdict



class BillProcess(Document):

            # To get Supplier List
            @frappe.whitelist()
            def list(self):
                doc = frappe.db.get_list("Supplier", fields=["supplier_name", "branch_id","name"])
                for d in doc:
                    if d.branch_id == self.branch_id:
                        self.append(
                            "supplier_list",
                            {
                                "supplier_name": d.supplier_name,
                                "supplier_id":d.name
                            },
                        )

            @frappe.whitelist()
            def selectall(self):
                children = self.get('supplier_list')
                if not children:
                    return
                all_selected = all([child.check for child in children])  
                value = 0 if all_selected else 1 
                for child in children:
                    child.check = value 
                # To Collect Data from Data Collection Doctype

# ---------------------------------------------------------------------------------------------------------------------------------------------------

            @frappe.whitelist()
            def show_data(self):

                for row in self.get('supplier_list'):
                        if row.check:
                            doc = frappe.db.get_list(
                                "Data Collection",
                                fields=[
                                    "date",
                                    "amount",
                                    "supplier_id",
                                    "milk_type",
                                    "fat",
                                    "snf",
                                    "rate",
                                    "litre",
                                    "bill_status",
                                    "supplier_name",
                                ],
                            )
                            for d in doc:
                                if row.supplier_id==d.supplier_id:
                                    x = self.first_date.split("-")
                                    first_date = date(int(x[0]), int(x[1]), int(x[2]))
                                    y = self.last_date.split("-")
                                    last_date = date(int(y[0]), int(y[1]), int(y[2]))
                                    delta = last_date - first_date
                                    for i in range(delta.days + 1):
                                        day = first_date + timedelta(days=i)
                                        if(day == d.date):
                                            self.append(
                                                "data_collection",
                                                {
                                                    "supplier_id": d.supplier_id,
                                                    "supplier_name": d.supplier_name,
                                                    "milk_type": d.milk_type,
                                                    "fat": d.fat,
                                                    "snf": d.snf,
                                                    "litre": d.litre,
                                                    "total": d.amount,
                                                },
                                            )

                litres_by_name = {}
                for row in self.data_collection:
                    name_surname = (row.supplier_id, row.supplier_name,row.milk_type)
                    if name_surname in litres_by_name:
                        litres_by_name[name_surname]["fat"] += int(row.fat)
                        litres_by_name[name_surname]["snf"] += int(row.snf)
                        litres_by_name[name_surname]["litre"] += int(row.litre)
                        litres_by_name[name_surname]["total"] += int(row.total)
                    else:
                        litres_by_name[name_surname] = {
                            "fat": row.fat,
                            "snf": row.snf,
                            "litre": row.litre,
                            "total": row.total,
                        }

                deduction_dict = {}
                deductions = frappe.get_all("Deduction Process", filters=None, fields=["name","first_date","status","branch_id"])
                for deduction in deductions:
                    if(str(deduction.first_date)==str(self.first_date) and deduction.status=="Not Deducted" and deduction.branch_id==self.branch_id): 
                        deduction_list = frappe.get_all("Child Deduction List", filters={"parent": deduction.name}, fields=["supplier_name", "current_deduction_amt"])
                        for row in deduction_list:
                                # deduction_dict[row.supplier_name] = int(row.current_deduction_amt)
                                if row.supplier_name in deduction_dict:
                                    # If the supplier already exists in the dictionary, add the current deduction amount to the existing value
                                    deduction_dict[row.supplier_name] += int(row.current_deduction_amt)
                                else:
                                    # If the supplier does not exist in the dictionary, create a new entry with the current deduction amount
                                    deduction_dict[row.supplier_name] = int(row.current_deduction_amt)


                for (supplier_id, supplier_name,milk_type), data in litres_by_name.items():
                    deduction = deduction_dict.get(supplier_id, 0)
                    self.append("bill_child",{
                        "supplier_id": supplier_id,
                        "supplier_name": supplier_name,
                        "milk_type": milk_type,

                        "avg_fat": data["fat"],
                        "avg_snf": data["snf"],
                        "avg_litre": data["litre"],
                        "total": data["total"],
                        "deduction_amount": deduction,
                        "total_amount":int(data["total"])-int(deduction)
                    })

                self.total = 0
                self.total_litre =0
                self.deduction_amount = 0
                self.bill_amount =0
                
                for row in self.bill_child:
                    self.total += row.total
                    self.total_litre += row.avg_litre
                    self.deduction_amount += row.deduction_amount
                self.bill_amount =  self.total - self.deduction_amount
                    
# -------------------------------------------------------------------------------------------------------------------------------------
        #    To update document status on before save event-
            @frappe.whitelist()
            def before_save(self):
                for i in self.get("bill_child"):
                    doc = frappe.db.get_list("Data Collection")
                    for d in doc:
                        d1 = frappe.get_doc("Data Collection", d.name)
                        if(i.supplier_id==d1.supplier_id):
                            x = self.first_date.split("-")
                            first_date = date(int(x[0]), int(x[1]), int(x[2]))
                            y = self.last_date.split("-")
                            last_date = date(int(y[0]), int(y[1]), int(y[2]))
                            delta = last_date - first_date
                            for j in range(delta.days + 1):
                                day = first_date + timedelta(days=j)
                                if day == d1.date:
                                    frappe.db.set_value(
                                                            "Data Collection", d.name, "bill_status", "billing in process"
                                                )    
                # this line is commented by vivek on 27-02                    
                # for i in self.get("bill_child"):
                #     a=frappe.db.get_list("Deduction Process")
                #     for b in a:
                #         c = frappe.get_doc("Deduction Process", b.name)
                #         if(str(c.first_date)==str(self.first_date) and c.status=="Not Deducted" and self.branch_id==c.branch_id):
                #             for i in c.get('deduction_list'):
                #                 for k in self.supplier_list:
                #                     if(k.supplier_id):
                #                         if(k.supplier_id==i.supplier_name):
                #                             i.status="Deduction in process"
                #                             i.save()
                #                             c.save()
                


           #To update document status on before submit event-
            @frappe.whitelist()
            def before_submit(self):
                for i in self.get("bill_child"):
                    doc = frappe.db.get_list("Data Collection")
                    for d in doc:
                        d1 = frappe.get_doc("Data Collection", d.name)
                        if i.supplier_id==d1.supplier_id:
                            x = self.first_date.split("-")
                            first_date = date(int(x[0]), int(x[1]), int(x[2]))
                            y = self.last_date.split("-")
                            last_date = date(int(y[0]), int(y[1]), int(y[2]))
                            delta = last_date - first_date
                            for j in range(delta.days + 1):
                                day = first_date + timedelta(days=j)
                                if day == d1.date:
                                    # frappe.msgprint('bill processed')
                                    frappe.db.set_value(
                                                            "Data Collection", d.name, "bill_status", "Billing done"
                                                )

                # for i in self.get("bill_child"):
                #     a=frappe.db.get_list("Deduction Process")
                #     for b in a:
                #         c = frappe.get_doc("Deduction Process", b.name)
                #         count=0
                #         if(str(c.first_date)==str(self.first_date) and self.branch_id==c.branch_id):
                #             for i in c.get('deduction_list'):
                #                 for k in self.supplier_list:
                #                     if(k.supplier_id):
                #                         if(k.supplier_id==i.supplier_name):
                #                             i.status="Deduction Done"
                #                             i.save()
                #                             c.save()
                                        
                #             if(count==0):
                #                 c.status="Deduction Done"   
                #             else:
                #                 c.status="Not Deducted"    
                #             c.save()  
                
                                                              
                for i in self.get("bill_child"):
                    doc=frappe.new_doc('Total Deduction Amount')
                    doc.supplier_name=i.supplier_id
                    doc.total_deduction_amount="-"+str(i.deduction_amount)
                    doc.date=self.today
                    doc.flag="Bill Process"
                    doc.insert()

                for i in self.get("bill_child"):
                    doc=frappe.new_doc('GL Entry')
                    doc.posting_date=self.today
                    doc.account=self.account_cr
                    # doc.party_type="Supplier"
                    # doc.party=i.supplier_id
                    doc.cost_center="Main - QT"
                    doc.credit=i.total_amount
                    doc.credit_in_account_currency=i.total_amount
                    doc.against=i.supplier_id
                    doc.voucher_type="Bill Process"
                    doc.voucher_no=self.name
                    doc.insert()

                    doc=frappe.new_doc('GL Entry')
                    doc.posting_date=self.today
                    doc.account=self.account_dr
                    doc.party_type="Supplier"
                    doc.party=i.supplier_id
                    doc.cost_center="Main - QT"
                    doc.debit=i.total_amount
                    doc.debit_in_account_currency=i.total_amount
                    doc.against=i.supplier_id
                    doc.voucher_type="Bill Process"
                    doc.voucher_no=self.name
                    doc.insert()



                # for row in self.get('supplier_list'):
                #     if row.check:
                #         doc = frappe.db.get_list(
                #             "Data Collection",
                #             fields=[
                #                 "date",
                #                 "amount",
                #                 "supplier_id",
                #                 "milk_type",
                #                 "fat",
                #                 "snf",
                #                 "rate",
                #                 "litre",
                #                 "supplier_name",
                #                 "rate_group",
                #                 "branch_id",
                #                 "supplier_name",
                #                 "name"
                #             ],
                #         )
                #         for d in doc:
                #             if row.supplier_id==d.supplier_id:
                #                 x = self.first_date.split("-")
                #                 first_date = date(int(x[0]), int(x[1]), int(x[2]))
                #                 y = self.last_date.split("-")
                #                 last_date = date(int(y[0]), int(y[1]), int(y[2]))
                #                 delta = last_date - first_date
                #                 for i in range(delta.days + 1):
                #                     day = first_date + timedelta(days=i)
                #                     if(day == d.date):
                #                         doc=frappe.new_doc('Data Collection History')
                #                         doc.supplier_name=d.supplier_name,
                #                         doc.supplier_id=d.supplier_id,
                #                         doc.milk_type=d.milk_type,
                #                         doc.fat=d.fat,
                #                         doc.snf=d.snf,
                #                         doc.amount=d.amount,
                #                         doc.rate=d.rate,
                #                         doc.litre=d.litre,
                #                         doc.rate_group=d.rate_group,
                #                         doc.branch_id=d.branch_id,
                #                         doc.date=d.date, 
                #                         doc.insert()
                #                         frappe.delete_doc("Data Collection",d.name)


                                                                                                    

            #To update document status on on_trash event-
            def on_trash(self):
                for i in self.get("bill_child"):
                    doc = frappe.db.get_list("Data Collection")
                    for d in doc:
                        d1 = frappe.get_doc("Data Collection", d.name)
                        if(i.supplier_id==d1.supplier_id and d1.bill_status=="billing in process" and (str(self.first_date)<=str(d1.date) and str(self.last_date)>=str(d1.date) )):
                                    
                                            frappe.db.set_value(
                                                                    "Data Collection", d.name, "bill_status", "Not Proceed"
                                                        )   

                # for i in self.get("bill_child"):
                #     a=frappe.db.get_list("Deduction Process")
                #     for b in a:
                #         c = frappe.get_doc("Deduction Process", b.name)
                #         if(str(c.first_date)==str(self.first_date) and c.status=="Deduction Done" or c.status=="Deduction in process"  and self.branch_id==c.branch_id):
                #             for i in c.get('deduction_list'):
                #                 for k in self.supplier_list:
                #                     if(k.supplier_id):
                #                         if(k.supplier_id==i.supplier_name):
                #                             i.status="Not Deducted"
                #                             i.save()
                #                             c.save()  
                #             c.status="Not Deducted"   
                #             c.save()                                  

    
            # #To update document status on on_cancel event-                                                                                             
            def on_cancel(self):
                # frappe.msgprint('bill processed')
                for i in self.get("bill_child"):
                    doc = frappe.db.get_list("Data Collection")
                    for d in doc:
                        d1 = frappe.get_doc("Data Collection", d.name)
                        if (i.supplier_id==d1.supplier_id) and (str(self.first_date)<=str(d1.date) and str(self.last_date)>=str(d1.date) ):
                            
                                    # frappe.msgprint('bill processed')
                                    frappe.db.set_value(
                                                            "Data Collection", d.name, "bill_status", "Not Proceed"
                                                )

                # for i in self.get("bill_child"):
                #     a=frappe.db.get_list("Deduction Process")
                #     for b in a:
                #         c = frappe.get_doc("Deduction Process", b.name)
                #         if(str(c.first_date)==str(self.first_date) and c.status=="Deduction Done" or c.status=="Deduction in process" and self.branch_id==c.branch_id):
                #             for i in c.get('deduction_list'):
                #                 for k in self.supplier_list:
                #                     if(k.supplier_id):
                #                         if(k.supplier_id==i.supplier_name):
                #                             i.status="Not Deducted"
                #                             i.save()
                #                             c.save()  
                #             c.status="Not Deducted"   
                #             c.save() 

                for i in self.get("bill_child"):
                    doc=frappe.new_doc('Total Deduction Amount')
                    doc.supplier_name=i.supplier_id
                    doc.total_deduction_amount=str(i.deduction_amount)
                    doc.date=self.today
                    doc.flag="Bill Process Canceled"
                    doc.insert()
                                                                       
         
                                


            @frappe.whitelist()
            def set_date_1(self):
                billperiod = ""
                doc = frappe.db.get_list("Dairy Branch", fields=["bill_period", "branch_name"])
                for d in doc:
                    if d.branch_name == self.branch_name:
                        billperiod = d.bill_period
                if billperiod == "7":
                    x = self.first_date.split("-")
                    if int(x[2]) >= 1 and int(x[2]) <= 7:
                        self.first_date = date(int(x[0]), int(x[1]), int(1))
                        Begindatestring = self.first_date
                        Begindate = datetime.strptime(str(Begindatestring), "%Y-%m-%d")
                        billperiod = int(billperiod) - 1
                        Enddate = Begindate + timedelta(days=int(str(billperiod)))
                        self.last_date = Enddate
                    elif int(x[2]) >= 8 and int(x[2]) <= 14:
                        self.first_date = date(int(x[0]), int(x[1]), int(8))
                        Begindatestring = self.first_date
                        Begindate = datetime.strptime(str(Begindatestring), "%Y-%m-%d")
                        billperiod = int(billperiod) - 1
                        Enddate = Begindate + timedelta(days=int(str(billperiod)))
                        self.last_date = Enddate
                    elif int(x[2]) >= 15 and int(x[2]) <= 21:
                        self.first_date = date(int(x[0]), int(x[1]), int(15))
                        Begindatestring = self.first_date
                        Begindate = datetime.strptime(str(Begindatestring), "%Y-%m-%d")
                        billperiod = int(billperiod) - 1
                        Enddate = Begindate + timedelta(days=int(str(billperiod)))
                        self.last_date = Enddate
                    elif int(x[2]) >= 22 and int(x[2]) <= 28 or 29 or 30 or 31:
                        year = int(x[0])
                        if (year % 4 == 0 and year % 100 != 0) or (
                            year % 400 == 0 and year % 100 == 0
                        ):
                            p = int(x[1])
                            d = {
                                1: 31,
                                2: 29,
                                3: 31,
                                4: 30,
                                5: 31,
                                6: 30,
                                7: 31,
                                8: 31,
                                9: 30,
                                10: 31,
                                11: 30,
                                12: 31,
                            }
                            for i in d:
                                if p == i:
                                    self.first_date = date(int(x[0]), int(x[1]), int(22))
                                    Begindatestring = self.first_date
                                    Begindate = datetime.strptime(
                                        str(Begindatestring), "%Y-%m-%d"
                                    )
                                    if d[i] == 31:
                                        billperiod = int(billperiod) + 2
                                    elif d[i] == 29:
                                        billperiod = int(billperiod) + 0
                                    elif d[i] == 30:
                                        billperiod = int(billperiod) + 1
                                    Enddate = Begindate + timedelta(days=int(str(billperiod)))
                                    self.last_date = Enddate

                        else:
                            p = int(x[1])
                            d = {
                                1: 31,
                                2: 28,
                                3: 31,
                                4: 30,
                                5: 31,
                                6: 30,
                                7: 31,
                                8: 31,
                                9: 30,
                                10: 31,
                                11: 30,
                                12: 31,
                            }
                            for i in d:
                                if p == i:
                                    self.first_date = date(int(x[0]), int(x[1]), int(22))
                                    Begindatestring = self.first_date
                                    Begindate = datetime.strptime(
                                        str(Begindatestring), "%Y-%m-%d"
                                    )
                                    if d[i] == 31:
                                        billperiod = int(billperiod) + 2
                                    elif d[i] == 28:
                                        billperiod = int(billperiod) - 1
                                    elif d[i] == 30:
                                        billperiod = int(billperiod) + 1
                                    Enddate = Begindate + timedelta(days=int(str(billperiod)))
                                    self.last_date = Enddate
                elif billperiod == "10":
                    x = self.first_date.split("-")
                    if int(x[2]) >= 1 and int(x[2]) <= 10:
                        self.first_date = date(int(x[0]), int(x[1]), int(1))
                        Begindatestring = self.first_date
                        Begindate = datetime.strptime(str(Begindatestring), "%Y-%m-%d")
                        billperiod = int(billperiod) - 1
                        Enddate = Begindate + timedelta(days=int(str(billperiod)))
                        self.last_date = Enddate
                    elif int(x[2]) >= 11 and int(x[2]) <= 20:
                        self.first_date = date(int(x[0]), int(x[1]), int(11))
                        Begindatestring = self.first_date
                        Begindate = datetime.strptime(str(Begindatestring), "%Y-%m-%d")
                        billperiod = int(billperiod) - 1
                        Enddate = Begindate + timedelta(days=int(str(billperiod)))
                        self.last_date = Enddate
                    elif int(x[2]) >= 21 and int(x[2]) <= 28 or 29 or 30 or 31:
                        year = int(x[0])
                        if (year % 4 == 0 and year % 100 != 0) or (
                            year % 400 == 0 and year % 100 == 0
                        ):
                            p = int(x[1])
                            d = {
                                1: 31,
                                2: 29,
                                3: 31,
                                4: 30,
                                5: 31,
                                6: 30,
                                7: 31,
                                8: 31,
                                9: 30,
                                10: 31,
                                11: 30,
                                12: 31,
                            }
                            for i in d:
                                if p == i:
                                    self.first_date = date(int(x[0]), int(x[1]), int(21))
                                    Begindatestring = self.first_date
                                    Begindate = datetime.strptime(
                                        str(Begindatestring), "%Y-%m-%d"
                                    )
                                    if d[i] == 31:
                                        billperiod = int(billperiod) -0
                                    elif d[i] == 29:
                                        billperiod = int(billperiod) -2
                                    elif d[i] == 30:
                                        billperiod = int(billperiod) -1
                                    Enddate = Begindate + timedelta(days=int(str(billperiod)))
                                    self.last_date = Enddate

                        else:
                            p = int(x[1])
                            d = {
                                1: 31,
                                2: 28,
                                3: 31,
                                4: 30,
                                5: 31,
                                6: 30,
                                7: 31,
                                8: 31,
                                9: 30,
                                10: 31,
                                11: 30,
                                12: 31,
                            }
                            for i in d:
                                if p == i:
                                    self.first_date = date(int(x[0]), int(x[1]), int(21))
                                    Begindatestring = self.first_date
                                    Begindate = datetime.strptime(
                                        str(Begindatestring), "%Y-%m-%d"
                                    )
                                    if d[i] == 31:
                                        billperiod = int(billperiod) +0
                                    elif d[i] == 28:
                                        billperiod = int(billperiod) - 3
                                    elif d[i] == 30:
                                        billperiod = int(billperiod) -1
                                    Enddate = Begindate + timedelta(days=int(str(billperiod)))
                                    self.last_date = Enddate

                elif billperiod == "15":
                    x = self.first_date.split("-")
                    if int(x[2]) >= 1 and int(x[2]) <= 15:
                        self.first_date = date(int(x[0]), int(x[1]), int(1))
                        Begindatestring = self.first_date
                        Begindate = datetime.strptime(str(Begindatestring), "%Y-%m-%d")
                        billperiod = int(billperiod) - 1
                        Enddate = Begindate + timedelta(days=int(str(billperiod)))
                        self.last_date = Enddate
                    elif int(x[2]) >= 16 and int(x[2]) <= 28 or 29 or 30 or 31:
                        year = int(x[0])
                        if (year % 4 == 0 and year % 100 != 0) or (
                            year % 400 == 0 and year % 100 == 0
                        ):
                            p = int(x[1])
                            d = {
                                1: 31,
                                2: 29,
                                3: 31,
                                4: 30,
                                5: 31,
                                6: 30,
                                7: 31,
                                8: 31,
                                9: 30,
                                10: 31,
                                11: 30,
                                12: 31,
                            }
                            for i in d:
                                if p == i:
                                    self.first_date = date(int(x[0]), int(x[1]), int(16))
                                    Begindatestring = self.first_date
                                    Begindate = datetime.strptime(
                                        str(Begindatestring), "%Y-%m-%d"
                                    )
                                    if d[i] == 31:
                                        billperiod = int(billperiod) - 0
                                    elif d[i] == 29:
                                        billperiod = int(billperiod) -2
                                    elif d[i] == 30:
                                        billperiod = int(billperiod) -1
                                    Enddate = Begindate + timedelta(days=int(str(billperiod)))
                                    self.last_date = Enddate

                        else:
                            p = int(x[1])
                            d = {
                                1: 31,
                                2: 28,
                                3: 31,
                                4: 30,
                                5: 31,
                                6: 30,
                                7: 31,
                                8: 31,
                                9: 30,
                                10: 31,
                                11: 30,
                                12: 31,
                            }
                            for i in d:
                                if p == i:
                                    self.first_date = date(int(x[0]), int(x[1]), int(16))
                                    Begindatestring = self.first_date
                                    Begindate = datetime.strptime(
                                        str(Begindatestring), "%Y-%m-%d"
                                    )
                                    if d[i] == 31:
                                        billperiod = int(billperiod) -0
                                    elif d[i] == 28:
                                        billperiod = int(billperiod)  -3
                                    elif d[i] == 30:
                                        billperiod = int(billperiod) -1
                                    Enddate = Begindate + timedelta(days=int(str(billperiod)))
                                    self.last_date = Enddate

                elif billperiod == "30":
                    x = self.first_date.split("-")
                    if int(x[2]) >= 1 and int(x[2]) <= 28 or 29 or 30 or 31:
                        year = int(x[0])
                        if (year % 4 == 0 and year % 100 != 0) or (
                            year % 400 == 0 and year % 100 == 0
                        ):
                            p = int(x[1])
                            d = {
                                1: 31,
                                2: 29,
                                3: 31,
                                4: 30,
                                5: 31,
                                6: 30,
                                7: 31,
                                8: 31,
                                9: 30,
                                10: 31,
                                11: 30,
                                12: 31,
                            }
                            for i in d:
                                if p == i:
                                    self.first_date = date(int(x[0]), int(x[1]), int(1))
                                    Begindatestring = self.first_date
                                    Begindate = datetime.strptime(
                                        str(Begindatestring), "%Y-%m-%d"
                                    )
                                    if d[i] == 31:
                                        billperiod = int(billperiod) -0
                                    elif d[i] == 29:
                                        billperiod = int(billperiod) - 2
                                    elif d[i] == 30:
                                        billperiod = int(billperiod) -1
                                    Enddate = Begindate + timedelta(days=int(str(billperiod)))
                                    self.last_date = Enddate

                        else:
                            p = int(x[1])
                            d = {
                                1: 31,
                                2: 28,
                                3: 31,
                                4: 30,
                                5: 31,
                                6: 30,
                                7: 31,
                                8: 31,
                                9: 30,
                                10: 31,
                                11: 30,
                                12: 31,
                            }
                            for i in d:
                                if p == i:
                                    self.first_date = date(int(x[0]), int(x[1]), int(1))
                                    Begindatestring = self.first_date
                                    Begindate = datetime.strptime(
                                        str(Begindatestring), "%Y-%m-%d"
                                    )
                                    if d[i] == 31:
                                        billperiod = int(billperiod) - 0
                                    elif d[i] == 28:
                                        billperiod = int(billperiod) - 3
                                    elif d[i] == 30:
                                        billperiod = int(billperiod) - 1
                                    Enddate = Begindate + timedelta(days=int(str(billperiod)))
                                    self.last_date = Enddate
                else:
                    frappe.msgprint("Please enter branch id")
              
   