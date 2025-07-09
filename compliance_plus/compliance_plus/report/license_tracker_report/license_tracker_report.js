// Copyright (c) 2025, KlyONIX Tech Consulting Pvt Ltd and contributors
// For license information, please see license.txt

frappe.query_reports["License Tracker Report"] = {
	"filters": [
		{
			"fieldname": "customer",
			"label": "Customer",
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname": "expiry_in_30_days",
			"label": "Expiry in Next 30 Days",
			"fieldtype": "Check",
			"depends_on": "eval:!doc.expired"
		},
		{
			"fieldname": "expired",
			"label": "Expired",
			"fieldtype": "Check",
			"depends_on": "eval:!doc.expiry_in_30_days"
		}
	]
}

