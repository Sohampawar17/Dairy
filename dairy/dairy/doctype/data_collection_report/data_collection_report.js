// Copyright (c) 2023, Vivek and contributors
// For license information, please see license.txt
frappe.ui.form.on('Data Collection Report', {

	show_result: function(frm) {
				frm.clear_table("bill_child")
				frm.refresh_field('bill_child')
				 }
});

frappe.ui.form.on('Data Collection Report', {

	branch_id: function(frm) {
				frm.clear_table("supplier_list")
				frm.refresh_field('supplier_list')
				 }
});




frappe.ui.form.on('Data Collection Report', {
	// refresh: function(frm) {

	// }
});



frappe.ui.form.on('Data Collection Report', {

	show_result: function (frm) {
		frm.call({
			method: 'append_to_bill_child',//function name defined in python
			doc: frm.doc, //current document
		});
	}
});




frappe.ui.form.on('Data Collection Report', {

	branch_id: function (frm) {
		frm.call({
			method: 'list',//function name defined in python
			doc: frm.doc, //current document
		});
	}
});

frappe.ui.form.on('Data Collection Report', {

	check_all: function (frm) {
		frm.call({
			method: 'checkall',//function name defined in python
			doc: frm.doc, //current document
		});
	}
});


frappe.ui.form.on('Data Collection Report', {

	first_date: function (frm) {
		frm.call({
			method: 'date',//function name defined in python
			doc: frm.doc, //current document
		});
	}
});


