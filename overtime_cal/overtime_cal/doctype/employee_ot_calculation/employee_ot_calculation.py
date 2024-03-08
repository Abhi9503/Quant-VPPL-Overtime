# Copyright (c) 2023, erpdata and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import time_diff_in_hours
from datetime import datetime
from datetime import timedelta
from datetime import datetime as dt, timedelta, time
import csv
import calendar

class EmployeeOTCalculation(Document):
	
	@frappe.whitelist()
	def get_ot_form(self):
		if self.from_date and self.to_date:
			doc = frappe.get_all("OT Form", 
							filters={"date": ["between", [self.from_date, self.to_date]]},
							fields=["name","supervisor_id","supervisor_name","date"],)
			if(doc):
				for d in doc:
					self.append('supervisor_list', {
												"ot_id":d.name,
												"supervisor_id":d.supervisor_id,
												"supervisor_name":d.supervisor_name,
												"date":d.date })
	@frappe.whitelist()
	def checkall(self):
		children = self.get('supervisor_list')
		if not children:
			return
		all_selected = all([child.check for child in children])  
		value = 0 if all_selected else 1 
		for child in children:
			child.check = value
   
   
	@frappe.whitelist()
	def get_overtime(self):
		num_days=0
		temp=str(self.from_date)
		lst=temp.split('-')
		year=int(lst[0])
		month=int(lst[1])
		date=int(lst[2])
		num_days=calendar.monthrange(int(year), int(month))[1]
		for i in self.get('supervisor_list'):
			if i.check :
				emp = frappe.get_all("Child OT Form", 
									filters={"parent": i.ot_id},
									fields=["worker_name","worker_id","employee_overtime_hrs"])  

				for e in emp:	
					basic_c=dearness_allowance_c=fixed_allowance_c=personal_pay_c = 0
					result = frappe.get_value("Employee Payroll", {"parent": e.worker_id}, ["basic_c", "dearness_allowance_c", "fixed_allowance_c", "personal_pay_c"])
					if result:
						basic_c, dearness_allowance_c, fixed_allowance_c, personal_pay_c = result
					rate=0
					total_amt=(basic_c+dearness_allowance_c+fixed_allowance_c+personal_pay_c)/num_days
					rate=total_amt/8
					self.append('employee_overtime',{
								"ot_id":i.ot_id,	
								"supervisor_name":i.supervisor_name,
								"supervisor_id":i.supervisor_id,
								"employee_name":e.worker_name,
								"employee_id":e.worker_id,
								"date":i.date,
								"employee_overtime_hrs":e.employee_overtime_hrs,
								"overtime_rate":rate,
								"total_amount":rate*e.employee_overtime_hrs
						})
		self.get_employee_sum()


	@frappe.whitelist()
	def get_employee_sum(self):
		employee_id_dict = {}
		for i in self.get('employee_overtime'):
			if i.employee_id not in employee_id_dict:
				employee_id_dict[i.employee_id] = {
					"ot_id": i.ot_id,
					"employee_name": i.employee_name,
					"employee_id": i.employee_id,
					"overtime_rate": i.overtime_rate,
					"employee_overtime_hrs":i.employee_overtime_hrs,
					"total_amount": i.total_amount,
					"overtime_rate":i.overtime_rate
				}
			else:
				employee_id_dict[i.employee_id]['total_amount'] += i.total_amount
				employee_id_dict[i.employee_id]['employee_overtime_hrs'] += i.employee_overtime_hrs

		for data in employee_id_dict:
			self.append('employee_overtime_amount', {
				"ot_id": employee_id_dict[data]['ot_id'],
				"employee_name": employee_id_dict[data]['employee_name'],
				"employee_id": employee_id_dict[data]['employee_id'],
				"overtime_rate": employee_id_dict[data]['overtime_rate'],
				"employee_overtime_hrs": employee_id_dict[data]['employee_overtime_hrs'],
				"total_overtime_amount": employee_id_dict[data]['total_amount'],
				"start_date":self.from_date,
				"end_date":self.to_date
			})

	
 
	@frappe.whitelist()
	def download_file(self):
		data = frappe.get_all('Employee Overtime Amount', 	
									filters={'parent': self.name}, 
									fields=["ot_id", "employee_id","employee_name","overtime_rate","total_overtime_amount","employee_overtime_hrs"])

		file_path = frappe.get_site_path('public', 'files', 'output.csv')
		with open(file_path, 'w', newline='') as csvfile:
			fieldnames = ["ot_id", "employee_id","employee_name","employee_overtime_hrs","overtime_rate","total_overtime_amount"] 
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			for row in data:
				writer.writerow(row)
		return file_path		
	

	@frappe.whitelist()
	def download(self):
		data = frappe.get_all('EOC Employee Overtime', 	
									filters={'parent': self.name}, 
									fields=["ot_id", "supervisor_name","employee_id","employee_name","date","employee_overtime_hrs","overtime_rate","total_amount"])

		file_path = frappe.get_site_path('public', 'files', 'output.csv')
		with open(file_path, 'w', newline='') as csvfile:
			fieldnames = ["ot_id", "supervisor_name",'employee_id',"employee_name","date","employee_overtime_hrs","overtime_rate","total_amount"]  # Replace with your actual field names
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			for row in data:
				writer.writerow(row)
		return file_path	
	