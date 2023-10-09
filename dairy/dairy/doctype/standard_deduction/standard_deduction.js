// Copyright (c) 2023, Vivek and contributors
// For license information, please see license.txt


frappe.ui.form.on('Standard Deduction', {
    refresh: function(frm) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper').css('margin-left', '0');
    }
});
frappe.ui.form.on('Standard Deduction', {
	branch_id: function (frm) {
		frm.clear_table("supplier_list")
		frm.refresh_field('supplier_list')

	}
});

frappe.ui.form.on('Standard Deduction', {
	show: function (frm) {
		frm.clear_table("deduction_list")
		frm.refresh_field('deduction_list')
	}
});

frappe.ui.form.on('Standard Deduction', {
	first_date: function (frm) {
		frm.clear_table("supplier_list")
		frm.refresh_field('supplier_list')
		frm.call({
			method: 'showlist',//function name defined in python
			doc: frm.doc, //current document
		});
	}
});

frappe.ui.form.on('Standard Deduction', {
	first_date: function (frm) {
		frm.call({
			method: 'set_date',//function name defined in python
			doc: frm.doc, //current document
		});
	}
});



frappe.ui.form.on('Standard Deduction', {
	show: function (frm) {
		frm.call({
			method: 'get_document',//function name defined in python
			doc: frm.doc, //current document
		});
	}
});



frappe.ui.form.on('Standard Deduction', {

	check_all: function (frm) {
		frm.call({
			method: 'checkall',//function name defined in python
			doc: frm.doc, //current document
		});
	}
});	