// Copyright (c) 2024, erpdata and contributors
// For license information, please see license.txt
frappe.ui.form.on('Biometric Attendance Sync', {
	from_date: function(frm) {
		frm.call({
			method:"check_dates",
			doc:frm.doc
		})
	},
	to_date: function(frm) {
		frm.call({
			method:"check_dates",
			doc:frm.doc
		})
	},
	sync: function(frm) {
		frm.call({
			method:"sync_data",
			doc:frm.doc
		})
	},
	setup: function(frm) {
		frm.call({
			method:"get_current_date",
			doc:frm.doc
		})
	},
});