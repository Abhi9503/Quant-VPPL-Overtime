# Copyright (c) 2023, erpdata and contributors
# For license information, please see license.txt

from frappe import _
import frappe
from frappe.model.document import Document
class OTForm(Document):
	def before_save(self):
		for i in self.get("child_ot_form"):
			i.date=self.date
   
	@frappe.whitelist()
	def check_repeat_entry(self,emp_id,dept,idx,date):
		for i in self.get("child_ot_form"):
			if(emp_id==i.worker_id and dept==i.department and i.idx!=idx and date==i.date):
				frappe.throw(f"Employee {emp_id} is already present in this table for date {date}")
			

				






















