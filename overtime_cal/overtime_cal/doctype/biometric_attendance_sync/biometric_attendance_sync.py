# Copyright (c) 2024, erpdata and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import zk
from datetime import datetime, timedelta
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
		dict={
			'2024-03-20-3107': ['3107','2024-03-20 08:05:00','2024-03-20 08:00:00'], 
			'2024-03-19-3107': ['3107','2024-03-19 23:50:59'], 
		}
		for i in dict:
			if(dict[i]!='0'):
				employee_data=frappe.get_value("Employee",{"attendance_device_id":str(dict[i][0]),"status":"Active"},["default_shift","name"])
				shift_name,emp_id=employee_data
				if(employee_data):
					in_time = None
					out_time = None
					shift=None
					shift_details=frappe.get_value("Shift Type",{"name":shift_name},["start_time","end_time","begin_check_in_before_shift_start_time","allow_check_out_after_shift_end_time"])
					start_time,end_time,begin_check_in_before_shift,allow_check_out_after_shift=shift_details
		
					start_time = datetime.strptime(str(start_time), "%H:%M:%S")
					end_time = datetime.strptime(str(end_time), "%H:%M:%S")
					begin_check_in_before_shift = begin_check_in_before_shift
					allow_check_out_after_shift = allow_check_out_after_shift
		
					begin_check_in_before_shift_timedelta = timedelta(minutes=begin_check_in_before_shift)
					allow_check_out_after_shift_timedelta = timedelta(minutes=allow_check_out_after_shift)

					# Subtract begin_check_in_before_shift from start_time
					from_date = start_time - begin_check_in_before_shift_timedelta

					# Add allow_check_out_after_shift to end_time
					to_date = end_time + allow_check_out_after_shift_timedelta

					shift_in_time = from_date.time()
					shift_out_time = to_date.time()
		
					check_time1 = datetime.strptime("23:59:59", '%H:%M:%S').time()
					check_time2 = datetime.strptime("18:00:00", '%H:%M:%S').time()
					check_time3 = datetime.strptime("01:00:00", '%H:%M:%S').time()


					if shift_in_time <= check_time1 and shift_in_time >= check_time2:
						shift="Third Shift"
						if len(dict[i]) >= 2:
							in_time = dict[i][1]
							out_time = dict[i][-1]
							out_time=self.check_diff(in_time,out_time)
							if(not out_time or not in_time):
								original_string =i
								date_part = original_string[:10]
								date_obj=datetime.strptime(date_part, '%Y-%m-%d') + timedelta(days=-1)
								new_date_part=date_obj.strftime('%Y-%m-%d')
								new_string=new_date_part + original_string[10:]
								for j in dict:	
									if(j==new_string):
										if len(dict[j])>=2:
											in_time=dict[j][-1]
											datetime_obj=datetime.strptime(str(in_time), '%Y-%m-%d %H:%M:%S')
											time_part=datetime_obj.strftime('%H:%M:%S')
											time_part=datetime.strptime(time_part, '%H:%M:%S').time()
											if(time_part>=check_time2):
												in_time==dict[j][-1]
												dict[j]='0'
											else:
												in_time==None
								out_time = dict[i][-1]
					elif shift_out_time <= check_time1 and shift_out_time <= check_time3:
						shift="Second Shift"
						if len(dict[i]) >= 2:
							in_time = dict[i][1]
							out_time = dict[i][-1]
							out_time=self.check_diff(in_time,out_time)
							if(not out_time):
								original_string =i
								date_part = original_string[:10]
								date_obj=datetime.strptime(date_part, '%Y-%m-%d') + timedelta(days=1)
								new_date_part=date_obj.strftime('%Y-%m-%d')
								new_string=new_date_part + original_string[10:]
								for j in dict:
									if(j==new_string):
										if len(dict[j])>=2:
											out_time=dict[j][1]
											datetime_obj=datetime.strptime(str(out_time), '%Y-%m-%d %H:%M:%S')
											time_part=datetime_obj.strftime('%H:%M:%S')
											time_part=datetime.strptime(time_part, '%H:%M:%S').time()
											if(time_part<=check_time3):
												out_time==dict[j][1]
												dict[j]='0'
											else:
												out_time==None
					else:		
						shift="First Shift"
						frappe.throw("hello")
						if len(dict[i]) >= 2:
							in_time = dict[i][1]
							out_time = dict[i][-1]
							out_time=self.check_diff(in_time,out_time)
					count=0
					if(shift=="First Shift"):
						if(in_time):
							datetime_obj = datetime.strptime(str(in_time), '%Y-%m-%d %H:%M:%S')
							time_part = datetime_obj.strftime('%H:%M:%S')
							in_time = datetime.strptime(time_part,'%H:%M:%S').time()
						if(out_time):
							datetime_obj = datetime.strptime(str(out_time), '%Y-%m-%d %H:%M:%S')
							time_part = datetime_obj.strftime('%H:%M:%S')
							out_time = datetime.strptime(time_part,'%H:%M:%S').time()
						
					if(shift=="Second Shift" or shift=="Third Shift"):
						if in_time:
							current_date = in_time[:10]
							shift_in_time = current_date + " " + str(shift_in_time)  # Assuming shift_in_time is a time string
							shift_in_time = datetime.strptime(shift_in_time, '%Y-%m-%d %H:%M:%S')
							in_time = datetime.strptime(str(in_time), '%Y-%m-%d %H:%M:%S')
       
							current_date =str(in_time)[:10]
							date_obj=datetime.strptime(current_date, '%Y-%m-%d') + timedelta(days=1)
							new_date_part=date_obj.strftime('%Y-%m-%d')
							shift_out_time=new_date_part + " " + str(shift_out_time) 
							shift_out_time = datetime.strptime(shift_out_time, '%Y-%m-%d %H:%M:%S')
						if out_time:
							out_time = datetime.strptime(str(out_time), '%Y-%m-%d %H:%M:%S')
       
					if(in_time):
						if(in_time>=shift_in_time and in_time<=shift_out_time):
							count=frappe.db.exists("Employee Checkin", {"employee":emp_id,"time":in_time,"log_type":"IN"})
							if(not count):
								new_doc=frappe.new_doc("Employee Checkin")
								new_doc.employee=emp_id
								new_doc.time=in_time
								new_doc.log_type="IN"
								new_doc.save()	
					if(out_time):
						if(out_time<=shift_out_time and out_time>=shift_in_time):
							count=frappe.db.exists("Employee Checkin", {"employee":emp_id,"time":out_time,"log_type":"OUT"})
							if(not count):
								new_doc=frappe.new_doc("Employee Checkin")
								new_doc.employee=emp_id
								new_doc.time=out_time
								new_doc.log_type="OUT"
								new_doc.save()
						
							
				# frappe.msgprint(str(dict))

		# if(not self.from_date or not self.to_date):
		# 	frappe.throw("Please select from date and to date")
		# self.check_dates()
		# for i in self.get("machine_configuration"):
		# 	if(i.check):
		# 		attendance_dict=self.get_attendance_data(self.from_date,self.to_date,i.machine_ip,i.com_key,i.port_no,i.machine_code)
		# 		frappe.throw(str(attendance_dict))
	
	def check_diff(self,in_time,out_time):
		in_time = datetime.strptime(in_time, '%Y-%m-%d %H:%M:%S')
		out_time = datetime.strptime(out_time, '%Y-%m-%d %H:%M:%S')
		diff = out_time - in_time
		if diff <= timedelta(minutes=15):
			out_time = None
		return out_time
 
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
				return attendance_records
		except Exception as e:
			frappe.throw(f"There Is Connecting Issue With Machine {machine_code}")
		finally:
			if conn:
				conn.disconnect()