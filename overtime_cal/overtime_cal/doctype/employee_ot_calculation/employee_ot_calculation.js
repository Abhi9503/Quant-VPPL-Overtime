// Copyright (c) 2023, erpdata and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee OT Calculation', {
	refresh: function(frm) {
		$('.layout-side-section').hide();
		$('.layout-main-section-wrapper').css('margin-left', '0');
	},
    to_date: function(frm) {
		frm.clear_table("supervisor_list");
		frm.refresh_field('supervisor_list');
        frm.clear_table("employee_overtime_amount");
		frm.refresh_field('employee_overtime_amount');
        frm.clear_table("employee_overtime");
		frm.refresh_field('employee_overtime');
		frm.call({
			method:'get_ot_form',
			doc:frm.doc
		})
	},
    from_date: function(frm) {
		frm.clear_table("supervisor_list");
		frm.refresh_field('supervisor_list');
        frm.clear_table("employee_overtime_amount");
		frm.refresh_field('employee_overtime_amount');
        frm.clear_table("employee_overtime");
		frm.refresh_field('employee_overtime');
		frm.call({
			method:'get_ot_form',
			doc:frm.doc
		})
	},
    select_all: function(frm) {
		frm.call({
			method:'checkall',
			doc:frm.doc
		})
	}
});


frappe.ui.form.on('Employee OT Calculation', {
	get_overtime: function(frm) {
		frm.clear_table("employee_overtime");
		frm.refresh_field('employee_overtime');
		frm.call({
			method:'get_overtime',
			doc:frm.doc
		})
	}
});


frappe.ui.form.on('Employee OT Calculation', {
    download_file: function(frm) {
        // Check if the form is saved
        if (!frm.doc.__islocal) {
            frappe.call({
                method: 'download_file',
                doc: frm.doc,
                callback: function(r) {
                    if (r.message) {
                        var file_path = "https://machinedev.erpdata.in/files/output.csv";
                        window.open(file_path);
                    }
                }
            });
        } else {
            frappe.msgprint(__("Please save the form before downloading."));
        }
    }
});



frappe.ui.form.on('Employee OT Calculation', {
    download: function(frm) {
        // Check if the form is saved
        if (!frm.doc.__islocal) {
            frappe.call({
                method: 'download',
                doc: frm.doc,
                callback: function(r) {
                    if (r.message) {
                        var file_path = "https://machinedev.erpdata.in/files/output.csv";
                        window.open(file_path);
                    }
                }
            });
        } else {
            frappe.msgprint(__("Please save the form before downloading."));
        }
    }
});


// frappe.ui.form.on('Employee OT Calculation', {
//     refresh: function(frm) {
//         frm.fields_dict['from_date'].$input.css('background-color', '#D2E9FB');
//         frm.fields_dict['to_date'].$input.css('background-color', '#D2E9FB');
// 		//frm.fields_dict['supervisor_list'].grid.get_field('supervisor_name').$input.css('background-color', '#D2E9FB');
// 		console.log("Script is running!");
//     }
// });

// frappe.ui.form.on('EOC Employee LIst', {
//     ot_id: function(frm, cdt, cdn) {
//         frappe.after_ajax(function() {
//             var child = locals[cdt][cdn];
//             var parent = frm.doc;

//             if ('supervisor_id' in child.fields_dict) {
//                 child.fields_dict['supervisor_id'].$input.css('background-color', '#D2E9FB');
//             }
//         });
//     }
// });


frappe.ui.form.on('Employee OT Calculation', {
    refresh: function(frm) {
        // Style fields in the main table
           frm.fields_dict['from_date'].$input.css('background-color', '#D2E9FB');
            frm.fields_dict['to_date'].$input.css('background-color', '#D2E9FB');
        

        // Style fields in a child table (assuming a table named "child_table")
   
    }
});


frappe.ui.form.on('EOC Employee LIst', {
    to_date: function(frm) {
        // Style fields in the main table
        frm.fields_dict['supervisor_name'].$input.css('background-color', '#D2E9FB');
        frm.fields_dict['supervisor_id'].$input.css('background-color', '#D2E9FB');

        console.log("Script is running!");
    }
});



// frappe.ui.form.on('Employee OT Calculation', {
//     refresh: function(frm) {
//         // select the first row in the child table
//         var rows = document.getElementsByClassName("grid-row");
//             for (var i = 0; i < rows.length; i++) {
//               rows[i].style.backgroundColor = "#D2E9FB";
//             }
//     }
// });


// frappe.ui.form.on('EOC Employee LIst', {
//     ot_id: function(frm, cdt, cdn) {
//         var child = locals[cdt][cdn];
//         var parent = frm.doc;
// 		frappe.msgprint("HIIII.......")
// 		// var supervisorField = childRow.fields_dict['supervisor_id'].$input;
// 		// supervisorField.css('background-color', '#D2E9FB');
//         // Check if the supervisor_id field exists in the child table
//         if ('supervisor_id' in child.fields_dict) {
//             child.fields_dict['supervisor_id'].$input.css('background-color', '#D2E9FB');
//         }
//     }
// });

