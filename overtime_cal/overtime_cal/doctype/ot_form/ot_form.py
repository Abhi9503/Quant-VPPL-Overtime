# Copyright (c) 2023, erpdata and contributors
# For license information, please see license.txt

from frappe import _
import frappe
from frappe.model.document import Document
import datetime 
class OTForm(Document):
	def before_save(self):
		for i in self.get("child_ot_form"):
			i.date=self.date
   
	# @frappe.whitelist()
	# def get_current_user_name(self):
	# 	if not self.supervisor_name and not self.supervisor_id:
	# 		user_name = frappe.session.user
	# 		doc = frappe.get_all("Employee", 
	# 							filters={"user_id":user_name},
	# 							fields=["name","employee_name"],)
	# 		if doc:
	# 			for d in doc :
	# 				self.supervisor_id = d.name
	# 				self.supervisor_name = d.employee_name
			

	# @frappe.whitelist()
	# def get_current_user_name(self):
	# 	user_name = frappe.session.user
	# 	doc = frappe.get_doc("Employee", user_name)
	# 	# frappe.throw(str(doc.full_name))
	# 	self.supervisor_id= str(doc.name)
	# 	self.supervisor_name = str(doc.full_name)
			

				






















