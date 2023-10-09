// Copyright (c) 2023, Vivek and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bill Process', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on('Bill Process', {
    refresh: function(frm) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper').css('margin-left', '0');
    }
});
// Copyright (c) 2023, Vivek and contributors
// For license information, please see license.txt
frappe.ui.form.on('Bill Process', {

	show_result: function(frm) {
				frm.clear_table("bill_child")
				frm.refresh_field('bill_child')
				 }
});

frappe.ui.form.on('Bill Process', {

	branch_id: function(frm) {
				frm.clear_table("supplier_list")
				frm.refresh_field('supplier_list')
				 }
});


frappe.ui.form.on('Bill Process', {

	show_data: function (frm) {
		frm.call({
			method: 'show_data',//function name defined in python
			doc: frm.doc, //current document
		});
	}
});


frappe.ui.form.on('Bill Process', {

	check_all: function (frm) {
		frm.call({
			method: 'selectall',//function name defined in python
			doc: frm.doc, //current document
		});
	}
});


frappe.ui.form.on('Bill Process', {

	show_result: function (frm) {
		frm.call({
			method: 'button',//function name defined in python
			doc: frm.doc, //current document
		});
	}
});




frappe.ui.form.on('Bill Process', {

	branch_id: function (frm) {
		frm.call({
			method: 'list',//function name defined in python
			doc: frm.doc, //current document
		});
	}
});



frappe.ui.form.on('Bill Process', {
	first_date: function (frm) {
		frm.call({
			method:'set_date_1',//function name defined in python
			doc: frm.doc, //current document
		});
	}
});

frappe.ui.form.on('Bill Process', {
	do_billing: function (frm) {
		frm.call({
			method:'dobill',//function name defined in python
			doc: frm.doc, //current document
		});
	}
});

frappe.ui.form.on('Bill Process', {
	do_billing: function (frm) {
		frm.call({
			method:'Push_in_Total_deduction_amount',//function name defined in python
			doc: frm.doc, //current document
		});
	}
});


// ----------------------------------------------------------------------------------------------------------------------

