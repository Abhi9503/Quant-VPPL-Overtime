# Copyright (c) 2023, erpdata and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import time_diff_in_hours
from datetime import datetime
from datetime import timedelta
from datetime import datetime as dt, timedelta, time
import csv
from dateutil import parser
import calendar
from frappe import _

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
		from_date =datetime.strptime(self.from_date, '%Y-%m-%d').date()
		for i in self.get('supervisor_list'):
			if i.check :
				emp = frappe.get_all("Child OT Form", 
									filters={"parent": i.ot_id},
									fields=["worker_name","worker_id","employee_overtime_hrs"])  

				for e in emp:	
					basic_c = personal_pay_c = fixed_allowance_c = dearness_allowance_c = 0
					employee_payroll_li = frappe.db.sql("""
						SELECT basic_c, hra_c, personal_pay_c, fixed_allowance_c, dearness_allowance_c, medical_allowance_c,
							from_date, petrol_allowance, p_allowance_in_amount
						FROM `tabEmployee Payroll` 
						WHERE parent = '{0}' ORDER BY from_date DESC
					""".format(e.worker_id), as_dict=True)
					
     
					if employee_payroll_li:
						for p in employee_payroll_li:
							if( p["from_date"]):
								if from_date >= p["from_date"]:
									basic_c = p["basic_c"]
									personal_pay_c = p["personal_pay_c"]
									fixed_allowance_c = p["fixed_allowance_c"]   
									dearness_allowance_c = p["dearness_allowance_c"]
									break
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
    
	@frappe.whitelist()
	def get_month_dates(self,input_date):
		selected_date = str(input_date)
		date_li = selected_date.split("-")
		year= int(date_li[0])
		month_num = int(date_li[1])
		num_days_in_month = calendar.monthrange(year,month_num)[1]
		start_date =datetime(year,month_num, 1).date()
		end_date =datetime(year, month_num, num_days_in_month).date()
		date_li = str(start_date).split("-")
		self.year = date_li[0]
		month_num = int(date_li[1])
		self.month = _(calendar.month_name[month_num]) 
		self.from_date=start_date
		self.to_date=end_date
		self.get_ot_form()
