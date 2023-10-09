# Copyright (c) 2023, Vivek and contributors
# For license information, please see license.txt

import frappe
# import pandas as pd
from frappe.model.document import Document

class RateMaster(Document):
	pass
	# def validate(self):
	# 	self.on_save()
	
	# def on_save(self):
	# 	data = pd.read_excel("/home/vivek/morant/sites/grizzlies.com"+self.attach)
	# 	data = data.set_index(data["Unnamed: 0"])
	# 	data.drop(["Unnamed: 0"],axis=1, inplace=True)
	# 	arr = []
	# 	for Y in data.index:
	# 		for X in data.columns:
	# 			arr.append([Y,X,data[X][Y]])
	
	# 	prabhu = pd.DataFrame(arr, columns=["Fat","SNF", "Rate"])

	# 	for i in range(0,len(prabhu)):
	# 		self.append("rate",{
	# 			'fat':prabhu.iloc[i][0],
	# 			'snf':prabhu.iloc[i][1],
	# 			'rate':prabhu.iloc[i][2]
	# 		})


