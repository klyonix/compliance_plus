# Copyright (c) 2025, KlyONIX Tech Consulting Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime, timedelta

def execute(filters=None):
	today = datetime.today().date()
	next_30 = today + timedelta(days=30)

	columns = [
		{"label": "Customer Name", "fieldname": "customer_name", "fieldtype": "Link", "options": "Customer", "width": 180},
		{"label": "DL Component", "fieldname": "dl_component", "fieldtype": "Data", "width": 150},
		{"label": "DL License Number", "fieldname": "dl_license_number", "fieldtype": "Data", "width": 180},
		{"label": "DL Expiry Date", "fieldname": "dl_expiry_date", "fieldtype": "Data", "width": 130},
		{"label": "FSSAI Component", "fieldname": "fssai_component", "fieldtype": "Data", "width": 150},
		{"label": "FSSAI License Number", "fieldname": "fssai_license_number", "fieldtype": "Data", "width": 180},
		{"label": "FSSAI Expiry Date", "fieldname": "fssai_expiry_date", "fieldtype": "Data", "width": 130},
	]

	customer_filters = {}
	if filters and filters.get("customer"):
		customer_filters["name"] = filters["customer"]

	customers = frappe.get_all("Customer", filters=customer_filters, fields=["name", "customer_name"])
	data = []

	for customer in customers:
		dl_details = frappe.get_all("Drug License Details", filters={"parent": customer.name}, fields=["component", "license_number", "expiry_date"])
		fssai_details = frappe.get_all("FSSAI Details", filters={"parent": customer.name}, fields=["component", "license_number", "expiry_date"])

		max_rows = max(len(dl_details), len(fssai_details), 1)

		for i in range(max_rows):
			dl = dl_details[i] if i < len(dl_details) else {}
			fssai = fssai_details[i] if i < len(fssai_details) else {}

			dl_expiry = dl.get("expiry_date")
			fssai_expiry = fssai.get("expiry_date")

			show_row = True

			# Filtering logic
			if filters and (filters.get("expiry_in_30_days") or filters.get("expired")):
				show_row = False
				if filters.get("expiry_in_30_days"):
					if (dl_expiry and today <= dl_expiry <= next_30) or (fssai_expiry and today <= fssai_expiry <= next_30):
						show_row = True
				if filters.get("expired"):
					if (dl_expiry and dl_expiry < today) or (fssai_expiry and fssai_expiry < today):
						show_row = True

			if not show_row:
				continue

			# Format expiry coloring
			dl_expiry_display = dl_expiry
			if dl_expiry:
				if dl_expiry < today:
					dl_expiry_display = f'<span style="color:red">{dl_expiry}</span>'
				elif today <= dl_expiry <= next_30:
					dl_expiry_display = f'<span style="color:orange">{dl_expiry}</span>'

			fssai_expiry_display = fssai_expiry
			if fssai_expiry:
				if fssai_expiry < today:
					fssai_expiry_display = f'<span style="color:red">{fssai_expiry}</span>'
				elif today <= fssai_expiry <= next_30:
					fssai_expiry_display = f'<span style="color:orange">{fssai_expiry}</span>'

			data.append({
				"customer_name": customer.customer_name if i == 0 else "",
				"dl_component": dl.get("component", ""),
				"dl_license_number": dl.get("license_number", ""),
				"dl_expiry_date": dl_expiry_display or "",
				"fssai_component": fssai.get("component", ""),
				"fssai_license_number": fssai.get("license_number", ""),
				"fssai_expiry_date": fssai_expiry_display or "",
			})

	return columns, data

