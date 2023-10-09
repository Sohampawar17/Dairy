# Copyright (c) 2023, Vivek and contributors
# For license information, please see license.txt
import frappe
from frappe import _

# import pandas as pd
from datetime import date 

from datetime import date, timedelta
from frappe.model.document import Document
from datetime import datetime
from datetime import timedelta

class StandardDeduction(Document):
    # Show Supplier List
    @frappe.whitelist()
    def showlist(self):
        farmer_list=[]
        doc=frappe.db.get_list('Milk Collection',filters={"branch_id":self.branch_id,"date": ["between", [self.first_date, self.last_date]]},
                                 fields=['supplier_id','supplier_name']
                                 )
        for d in doc:
            if(d.supplier_id not in farmer_list):
                farmer_list.append(d.supplier_id)
                self.append("supplier_list", {
                    "supplier_name": d.supplier_name,
                    "supplier_id":d.supplier_id
                    })
              
    @frappe.whitelist()
    def checkall(self):
        children = self.get('supplier_list')
        if not children:
            return
        all_selected = all([child.check for child in children])  
        value = 0 if all_selected else 1 
        for child in children:
            child.check = value 
                # To Collect Data from D                   




    @frappe.whitelist()
    def get_document(self):
        collection_dict={}
        for i in self.get("supplier_list"):  # first child table
            if (i.check):
                doc=frappe.db.get_list('Milk Collection',filters={"branch_id":self.branch_id,"date": ["between", [self.first_date, self.last_date]],"bill_status":False},
                                 fields=['supplier_id','supplier_name','milk_type',"litre","amount"]
                                 ) 
                for d in doc:
                    far_milk=d.supplier_id+""+d.milk_type
                    if(far_milk not in collection_dict):
                        collection_dict[far_milk]={
                                "supplier_id":d.supplier_id,
                                "supplier_name":d.supplier_name,
                                "milk_type":d.milk_type,
                                "litre":d.litre,
                                "amount":d.amount,
                                "liter_wise":0,
                                "percentage_wise":0,
                                "bill_wise":0,
                                "total_deduction_amt":0,
                                "liter_wise_amt":0,
                                "percentage_wise_amt":0,
                                "bill_wise_amt":0
                        }
                    else:
                        collection_dict[far_milk]["litre"]=collection_dict[far_milk]["litre"]+d.litre
                        collection_dict[far_milk]["amount"]=collection_dict[far_milk]["amount"]+d.amount
                for value in collection_dict:
                    if(collection_dict[value]["milk_type"]=="Cow"):
                        if(self.cow!=0):
                            collection_dict[value]["liter_wise"]=self.cow
                            collection_dict[value]["liter_wise_amt"]=collection_dict[value]["liter_wise"]*collection_dict[value]["litre"]
                            collection_dict[value]["total_deduction_amt"]=collection_dict[value]["total_deduction_amt"]+collection_dict[value]["liter_wise"]*collection_dict[value]["litre"]
                        if(self.cow2!=0):
                            collection_dict[value]["percentage_wise"]=self.cow2
                            collection_dict[value]["percentage_wise_amt"]=collection_dict[value]["percentage_wise"]*collection_dict[value]["amount"]/100
                            collection_dict[value]["total_deduction_amt"]=collection_dict[value]["total_deduction_amt"]+collection_dict[value]["percentage_wise"]*collection_dict[value]["amount"]/100
                        if(self.cow3!=0):
                            collection_dict[value]["bill_wise"]=self.cow3
                            collection_dict[value]["bill_wise_amt"]=collection_dict[value]["bill_wise"]
                            collection_dict[value]["total_deduction_amt"]=collection_dict[value]["total_deduction_amt"]+collection_dict[value]["bill_wise"]
                    if(collection_dict[value]["milk_type"]=="Buffalo"):
                        if(self.buffalo!=0):
                            collection_dict[value]["liter_wise"]=self.buffalo
                            collection_dict[value]["liter_wise_amt"]=collection_dict[value]["liter_wise"]*collection_dict[value]["litre"]
                            collection_dict[value]["total_deduction_amt"]=collection_dict[value]["total_deduction_amt"]+collection_dict[value]["liter_wise"]*collection_dict[value]["litre"]
                        if(self.buffalo1!=0):
                            collection_dict[value]["percentage_wise"]=self.buffalo1
                            collection_dict[value]["percentage_wise_amt"]=collection_dict[value]["percentage_wise"]*collection_dict[value]["amount"]/100
                            collection_dict[value]["total_deduction_amt"]=collection_dict[value]["total_deduction_amt"]+collection_dict[value]["percentage_wise"]*collection_dict[value]["amount"]/100
                        if(self.buffalo2!=0):
                            collection_dict[value]["bill_wise"]=self.buffalo2
                            collection_dict[value]["bill_wise_amt"]=collection_dict[value]["bill_wise"]
                            collection_dict[value]["total_deduction_amt"]=collection_dict[value]["total_deduction_amt"]+collection_dict[value]["bill_wise"]
                    self.append(
                        "deduction_list",{
                            "farmer_code": collection_dict[value]["supplier_id"],
                            "supplier_name": collection_dict[value]["supplier_name"],
                            "cowbuffalo":collection_dict[value]["milk_type"],
                            "total_liter":collection_dict[value]["litre"],
                            "liter_wise":collection_dict[value]["liter_wise"],
                            "percentage_wise":collection_dict[value]["percentage_wise"],
                            "bill_wise":collection_dict[value]["bill_wise"],
                            "liter_wise_amt":collection_dict[value]["liter_wise_amt"],
                            "percentage_wise_amt":collection_dict[value]["percentage_wise_amt"],
                            "bill_wise_amt":collection_dict[value]["bill_wise_amt"],
                            "total_deduction_amt":collection_dict[value]["total_deduction_amt"],
                            "total_amount":collection_dict[value]["amount"]
                        }
                    )
   
    #To set Date between two period
    @frappe.whitelist()
    def set_date(self):
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