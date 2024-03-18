// Copyright (c) 2023, erpdata and contributors
// For license information, please see license.txt

frappe.ui.form.on('OT Form', {
    refresh: function(frm) {
                     $('.layout-side-section').hide();
                     $('.layout-main-section-wrapper').css('margin-left', '0');
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

frappe.ui.form.on('Child OT Form', {
    worker_id: function(frm,cdt,cdn) {
        var r=locals[cdt][cdn];
        frm.call({
            method:'check_repeat_entry',
            doc:frm.doc,
            args:{
                "emp_id":r.worker_id,
                "dept":r.department,
                "idx":r.idx
            }
        })
    }
});
