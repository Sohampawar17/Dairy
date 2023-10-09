frappe.ui.form.on("Apply Rate Group", {
	onload: function(frm) {
			frm.set_query("rate_group", function() {
			return {
				filters: [
					["Rate Master","branch_id","in", [frm.doc.branch]],
					["Rate Master","milk_type","in", [frm.doc.milk_type]]	
				]
			};
		});
	}
});


// ---------------------------------------------------------------------------------------------
// frappe.ui.form.on('Apply Rate Group', {
// 	show_list: function (frm) {
// 		frm.clear_table("supplier_list")
// 		frm.refresh_field('supplier_list')
// 	}
// });

// frappe.ui.form.on('Apply Rate Group', {
// 	check_all: function (frm) {
// 		// frm.clear_table("supplier_list")
// 		frm.refresh_field('supplier_list')
// 	}
// });



frappe.ui.form.on('Apply Rate Group', {
	milk_type: function (frm) {
		frm.clear_table("supplier_list")
		frm.refresh_field('supplier_list')
	}
});


// --------------------------------------------------------------------------------------------
frappe.ui.form.on('Apply Rate Group', {
	to_date: function (frm) {
		frm.call({
			method:'currentrategroup',//function name defined in python
			doc: frm.doc, //current document
		});
	}
});

frappe.ui.form.on('Apply Rate Group', {
	milk_type: function (frm) {
		frm.call({
			method: 'list',//function name defined in python
			doc: frm.doc, //current document
		});
	}
});


frappe.ui.form.on('Apply Rate Group', {
	apply: function (frm) {
		frm.call({
			method: 'rateapply',//function name defined in python
			doc: frm.doc, //current document
		});
	}
});

frappe.ui.form.on('Apply Rate Group', {
	check_all: function (frm) {
		frm.call({
			method: 'checkall',//function name defined in python
			doc: frm.doc, //current document
		});
	}
});



// frappe.ui.form.on('Apply Rate Group', {
// 	apply: function (frm) {
// 		frm.call({
// 			method: 'msgapply',//function name defined in python
// 			doc: frm.doc, //current document
// 		});
// 	}
// });
// frappe.ui.form.on('Apply Rate Group', {
// 	branch: function (frm) {
// 		frm.call({
// 			method: 'abhi',//function name defined in python
// 			doc: frm.doc, //current document
// 		});
// 	}
// });

// frappe.ui.form.on('Apply Rate Group', {
// 	show_list: function (frm) {
// 		frm.call({
// 			method: 'list',//function name defined in python
// 			doc: frm.doc, //current document
// 		});
// 	}
// });

// frappe.ui.form.on('Apply Rate Group', {
// 	apply: function (frm) {
// 		frm.call({
// 			method: 'shreeram',//function name defined in python
// 			doc: frm.doc, //current document
// 		});
// 	}
// });
