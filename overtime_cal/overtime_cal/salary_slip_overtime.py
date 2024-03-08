import frappe

@frappe.whitelist()
def set_overtime(payroll_name):
    start_date,end_date=frappe.get_value("Payroll Entry",{"name":payroll_name},["start_date","end_date"])
    child_data=frappe.get_all("Payroll Employee Detail",{"parent":payroll_name},"employee")
    for i in child_data:
        overtime_hrs=frappe.get_value("Employee Overtime Amount",{"start_date":start_date,"end_date":end_date,"employee_id":i.employee},"employee_overtime_hrs")
        
        salary_slip=frappe.get_value("Salary Slip",{"payroll_entry":payroll_name,"employee":i.employee},"name")
        salary_struct=frappe.get_value("Salary Slip",{"payroll_entry":payroll_name,"employee":i.employee},"salary_structure")
        overtime_rate=frappe.get_value("Salary Structure",salary_struct,"custom_overtime_rate")
        
        if(overtime_hrs):
            doc=frappe.get_doc("Salary Slip",salary_slip)
            overtime_comp=True
            for i in doc.get("earnings"):
                if(i.salary_component=="Overtime" and i.amount==overtime_hrs*overtime_rate):
                    overtime_comp=False
            if(overtime_comp):
                doc.append("earnings",{
                    "salary_component":"Overtime",
                    "amount":overtime_hrs*overtime_rate
                })
                doc.save()


# import frappe

# @frappe.whitelist()
# def set_overtime(payroll_name):
#     start_date,end_date=frappe.get_value("Payroll Entry",{"name":payroll_name},["start_date","end_date"])
#     child_data=frappe.get_all("Payroll Employee Detail",{"parent":payroll_name},"employee")
#     for i in child_data:
#         overtime_hrs=frappe.get_value("Employee Overtime Amount",{"start_date":start_date,"end_date":end_date,"employee_id":i.employee},"total_overtime_amount")
        
#         salary_slip=frappe.get_value("Salary Slip",{"payroll_entry":payroll_name,"employee":i.employee},"name")
#         if(overtime_hrs):
#             doc=frappe.get_doc("Salary Slip",salary_slip)
#             overtime_comp=True
#             for i in doc.get("earnings"):
#                 if(i.salary_component=="Overtime" and i.amount==overtime_hrs):
#                     overtime_comp=False
#             if(overtime_comp):
#                 doc.append("earnings",{
#                     "salary_component":"Overtime",
#                     "amount":overtime_hrs
#                 })
#                 doc.save()