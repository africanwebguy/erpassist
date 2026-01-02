# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from erpassist.erpassist.core.action_registry import ActionRegistry

def after_install():
	"""
	Setup ERPAssist after installation
	"""
	# Create default settings
	create_default_settings()
	
	# Register default actions
	ActionRegistry.register_default_actions()
	
	frappe.db.commit()
	
	print("ERPAssist installation complete!")
	print("Please configure your OpenAI API key in ERPAssist Settings.")

def create_default_settings():
	"""
	Create default ERPAssist Settings
	"""
	if not frappe.db.exists("ERPAssist Settings"):
		settings = frappe.get_doc({
			"doctype": "ERPAssist Settings",
			"ai_model": "gpt-4o",
			"enable_audit_log": 1,
			"max_tokens": 4000
		})
		
		# Add default enabled modules
		for module in ["CRM", "Selling", "Buying", "Stock", "Accounting", "HR", "Payroll", "Projects"]:
			settings.append("enabled_modules", {
				"module_name": module,
				"enabled": 1
			})
		
		settings.insert()
		frappe.db.commit()
