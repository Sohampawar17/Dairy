frappe.ui.form.on("Variable Deduction", {
	onload: function(frm) {
			frm.set_query("supplier", function() {
			return {
				filters: [
					["Vender List","branch","in", [frm.doc.branch]]
				]
			};
		});
	}
});
frappe.ui.form.on('Variable Deduction', {
    refresh: function(frm) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper').css('margin-left', '0');
    }
});
frappe.ui.form.on('Variable Deduction', {
	// avanti: function(frm) {
	// 	frm.call({
	// 		method:'avantii',//function name defined in python
	// 		doc:frm.doc, //current document
	// 	 });
	//  }
});
