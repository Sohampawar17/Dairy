// // Copyright (c) 2023, vivek and contributors
// // For license information, please see license.txt

// frappe.ui.form.on('Milk Collection', {
// 	// refresh: function(frm) {

// 	// }
// });
frappe.ui.form.on('Milk Collection', {
	refresh: function(frm) {
		$('.layout-side-section').hide();
		$('.layout-main-section-wrapper').css('margin-left', '0');
	}
});
	frappe.ui.form.on("Milk Collection", {
	onload: function(frm) {
	frm.set_query("supplier_id", function() {
	return {
	filters: [
	["Vendor Registration","branch","in", [frm.doc.branch_id]]
	]
	};
	});
	}
	});
	
// 	// --------------------------------------------------------------------------------------------------------
	frappe.ui.form.on('Milk Collection', {
	supplier_id: function(frm) {
	frm.call({
	method:'current_shift',//function name defined in python
	doc:frm.doc, //current document
	});
	}
	});
	
	frappe.ui.form.on('Milk Collection', {
	supplier_id: function(frm) {
	frm.call({
	method:'get_rete_group',//function name defined in python
	doc:frm.doc, //current document
	});
	}
	});
// 	// frappe.ui.form.on('Milk Collection', {
// 	// supplier_id: function(frm) {
// 	// frm.call({
// 	// method:'get_data',//function name defined in python
// 	// doc:frm.doc, //current document
// 	// });
// 	// }
// 	// });
	
	frappe.ui.form.on('Milk Collection', {
	calculate: function(frm) {
	frm.call({
	method:'calculate_data',//function name defined in python
	doc:frm.doc, //current document
	});
	}
	});
	
// 	// frappe.ui.form.on('Milk Collection', {
// 	// branch_id: function(frm) {
// 	// frm.call({
// 	// method:'today',//function name defined in python
// 	// doc:frm.doc, //current document
// 	// });
// 	// }
// 	// });
	
	