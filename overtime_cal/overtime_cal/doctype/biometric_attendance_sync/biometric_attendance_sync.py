# Copyright (c) 2024, erpdata and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import zk
from datetime import datetime
import re  

class BiometricAttendanceSync(Document):
	@frappe.whitelist()
	def check_dates(self):
		if(self.to_date and self.from_date):
			if(self.to_date < self.from_date):
				frappe.throw("From Date can not greater than To Date")
    
	@frappe.whitelist()
	def get_current_date(self):
		self.from_date=datetime.today()
		self.to_date=datetime.today()
	
	@frappe.whitelist()
	def sync_data(self):
		if(not self.from_date or not self.to_date):
			frappe.throw("Please select from date and to date")
		self.check_dates()
		for i in self.get("machine_configuration"):
			if(i.check):
				attendance_dict=self.get_attendance_data(self.from_date,self.to_date,i.machine_ip,i.com_key,i.port_no,i.machine_code)
				frappe.throw(str(attendance_dict))
	
	def get_attendance_data(self,start_date,end_date,machine_ip,common_key,port,machine_code):    
		zk_instance = zk.base.ZK(machine_ip, port=int(port), timeout=60, password=str(common_key))
		conn=""
		try:
			conn = zk_instance.connect()
			if conn:
				attendance_data = conn.get_attendance()
				conn.disable_device()
				pattern = r"<Attendance>: (\d+) : (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \((\d+), (\d+)\)"
				attendance_records={}
				for record in attendance_data:
					record_date = record.timestamp.date()
					if(record_date.strftime('%Y-%m-%d')>=start_date and record_date.strftime('%Y-%m-%d')<=end_date):   
						attendance_string=record
						match = re.match(pattern,str(attendance_string))
						if match:
							user_id = int(match.group(1))
							timestamp = match.group(2)
							dict_key=f"{record_date.strftime('%Y-%m-%d')}-{user_id}"
							if(dict_key not in attendance_records):
								attendance_records[dict_key]=[str(user_id),timestamp]
							else:
								attendance_records[dict_key].append(timestamp)
				return attendance_data
		except Exception as e:
			frappe.throw(f"There Is Connecting Issue With Machine {machine_code}")
		finally:
			if conn:
				conn.disconnect()