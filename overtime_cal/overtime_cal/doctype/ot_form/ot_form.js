// Copyright (c) 2023, erpdata and contributors
// For license information, please see license.txt

frappe.ui.form.on('OT Form', {
    refresh: function(frm) {
                     $('.layout-side-section').hide();
                     $('.layout-main-section-wrapper').css('margin-left', '0');
    }
});


