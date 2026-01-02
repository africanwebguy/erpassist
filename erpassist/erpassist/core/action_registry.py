# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
import json

class ActionRegistry:
	"""
	Registry of all allowed actions in ERPAssist
	Implements whitelist approach - only registered actions can be executed
	"""
	
	def __init__(self):
		self.actions = {}
		self._load_actions()
	
	def _load_actions(self):
		"""
		Load all enabled actions from ERPAssist Action Registry
		"""
		actions = frappe.get_all(
			"ERPAssist Action Registry",
			filters={"enabled": 1},
			fields=["*"]
		)
		
		for action in actions:
			# Load allowed roles
			roles = frappe.get_all(
				"ERPAssist Action Role",
				filters={"parent": action.name},
				fields=["role"]
			)
			action["allowed_roles"] = [r.role for r in roles]
			
			self.actions[action.action_name] = action
	
	def get_action(self, action_name):
		"""
		Get a specific action by name
		"""
		return self.actions.get(action_name)
	
	def get_available_actions(self, user_roles):
		"""
		Get all actions available to a user based on their roles
		"""
		available = []
		
		for action_name, action in self.actions.items():
			# Check if user has any of the required roles
			if not action.get("allowed_roles"):
				# If no roles specified, available to all
				available.append(action)
			else:
				# Check if user has any required role
				has_permission = any(role in user_roles for role in action["allowed_roles"])
				if has_permission:
					available.append(action)
		
		return available
	
	def is_action_allowed(self, action_name, user_roles):
		"""
		Check if an action is allowed for given user roles
		"""
		action = self.get_action(action_name)
		
		if not action:
			return False
		
		if not action.get("allowed_roles"):
			return True
		
		return any(role in user_roles for role in action["allowed_roles"])
	
	@staticmethod
	def register_default_actions():
		"""
		Register default actions for common ERPNext operations
		This should be called during installation/setup
		"""
		default_actions = [
			# CRM Actions
			{
				"action_name": "view_leads_summary",
				"action_category": "QUERY",
				"module": "CRM",
				"description": "View summary of leads",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "erpassist.erpassist.handlers.crm.get_leads_summary",
				"allowed_roles": ["Sales User", "Sales Manager", "System Manager"]
			},
			{
				"action_name": "view_opportunities",
				"action_category": "QUERY",
				"module": "CRM",
				"description": "View opportunities",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "erpassist.erpassist.handlers.crm.get_opportunities",
				"allowed_roles": ["Sales User", "Sales Manager", "System Manager"]
			},
			
			# Selling Actions
			{
				"action_name": "view_sales_orders",
				"action_category": "QUERY",
				"module": "Selling",
				"description": "View sales orders",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "erpassist.erpassist.handlers.selling.get_sales_orders",
				"allowed_roles": ["Sales User", "Sales Manager", "System Manager"]
			},
			{
				"action_name": "draft_sales_order",
				"action_category": "DRAFT",
				"module": "Selling",
				"description": "Create a draft sales order",
				"enabled": 1,
				"requires_confirmation": 1,
				"risk_level": "Medium",
				"handler_function": "erpassist.erpassist.handlers.selling.create_sales_order_draft",
				"allowed_roles": ["Sales User", "Sales Manager", "System Manager"]
			},
			
			# Buying Actions
			{
				"action_name": "view_purchase_orders",
				"action_category": "QUERY",
				"module": "Buying",
				"description": "View purchase orders",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "erpassist.erpassist.handlers.buying.get_purchase_orders",
				"allowed_roles": ["Purchase User", "Purchase Manager", "System Manager"]
			},
			
			# Stock Actions
			{
				"action_name": "view_stock_summary",
				"action_category": "QUERY",
				"module": "Stock",
				"description": "View stock levels and summary",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "erpassist.erpassist.handlers.stock.get_stock_summary",
				"allowed_roles": ["Stock User", "Stock Manager", "System Manager"]
			},
			
			# Accounting Actions
			{
				"action_name": "view_account_balances",
				"action_category": "QUERY",
				"module": "Accounting",
				"description": "View account balances",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "erpassist.erpassist.handlers.accounting.get_account_balances",
				"allowed_roles": ["Accounts User", "Accounts Manager", "System Manager"]
			},
			{
				"action_name": "draft_journal_entry",
				"action_category": "DRAFT",
				"module": "Accounting",
				"description": "Create a draft journal entry",
				"enabled": 1,
				"requires_confirmation": 1,
				"risk_level": "High",
				"handler_function": "erpassist.erpassist.handlers.accounting.create_journal_entry_draft",
				"allowed_roles": ["Accounts User", "Accounts Manager", "System Manager"]
			},
			
			# HR Actions
			{
				"action_name": "view_employee_list",
				"action_category": "QUERY",
				"module": "HR",
				"description": "View employee list",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "erpassist.erpassist.handlers.hr.get_employee_list",
				"allowed_roles": ["HR User", "HR Manager", "System Manager"]
			},
			{
				"action_name": "approve_leave_application",
				"action_category": "APPROVE",
				"module": "HR",
				"description": "Approve a leave application",
				"enabled": 1,
				"requires_confirmation": 1,
				"risk_level": "Medium",
				"handler_function": "erpassist.erpassist.handlers.hr.approve_leave",
				"allowed_roles": ["HR Manager", "System Manager"]
			},
			
			# Payroll Actions
			{
				"action_name": "execute_payroll",
				"action_category": "EXECUTE_PAYROLL",
				"module": "Payroll",
				"description": "Execute payroll for a period",
				"enabled": 1,
				"requires_confirmation": 1,
				"risk_level": "Critical",
				"handler_function": "erpassist.erpassist.handlers.payroll.execute_payroll",
				"allowed_roles": ["HR Manager", "System Manager"]
			},
			
			# Projects Actions
			{
				"action_name": "view_projects_summary",
				"action_category": "QUERY",
				"module": "Projects",
				"description": "View projects summary",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "erpassist.erpassist.handlers.projects.get_projects_summary",
				"allowed_roles": ["Projects User", "Projects Manager", "System Manager"]
			},
			{
				"action_name": "view_tasks_summary",
				"action_category": "QUERY",
				"module": "Projects",
				"description": "View tasks summary",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "erpassist.erpassist.handlers.projects.get_tasks_summary",
				"allowed_roles": ["Projects User", "Projects Manager", "System Manager"]
			},
			
			# Manufacturing Actions
			{
				"action_name": "view_work_orders",
				"action_category": "QUERY",
				"module": "Manufacturing",
				"description": "View work orders",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "erpassist.erpassist.handlers.manufacturing.get_work_orders",
				"allowed_roles": ["Manufacturing User", "Manufacturing Manager", "System Manager"]
			},
			{
				"action_name": "view_bom_summary",
				"action_category": "QUERY",
				"module": "Manufacturing",
				"description": "View Bill of Materials summary",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "erpassist.erpassist.handlers.manufacturing.get_bom_summary",
				"allowed_roles": ["Manufacturing User", "Manufacturing Manager", "System Manager"]
			},
			
			# Support Actions
			{
				"action_name": "view_issues_summary",
				"action_category": "QUERY",
				"module": "Support",
				"description": "View support issues summary",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "erpassist.erpassist.handlers.support.get_issues_summary",
				"allowed_roles": ["Support Team", "System Manager"]
			},
			{
				"action_name": "view_service_level_summary",
				"action_category": "QUERY",
				"module": "Support",
				"description": "View SLA compliance summary",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "erpassist.erpassist.handlers.support.get_service_level_summary",
				"allowed_roles": ["Support Team", "System Manager"]
			},
			
			# Assets Actions
			{
				"action_name": "view_assets_summary",
				"action_category": "QUERY",
				"module": "Assets",
				"description": "View assets summary",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "erpassist.erpassist.handlers.assets.get_assets_summary",
				"allowed_roles": ["Stock User", "Accounts User", "System Manager"]
			},
			{
				"action_name": "view_asset_maintenance_schedule",
				"action_category": "QUERY",
				"module": "Assets",
				"description": "View asset maintenance schedule",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "erpassist.erpassist.handlers.assets.get_asset_maintenance_schedule",
				"allowed_roles": ["Stock User", "Accounts User", "System Manager"]
			},
			
			# Quality Actions
			{
				"action_name": "view_quality_inspections",
				"action_category": "QUERY",
				"module": "Quality",
				"description": "View quality inspections",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "erpassist.erpassist.handlers.quality.get_quality_inspections",
				"allowed_roles": ["Quality Manager", "Stock User", "System Manager"]
			},
			{
				"action_name": "view_quality_goals",
				"action_category": "QUERY",
				"module": "Quality",
				"description": "View quality goals",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "erpassist.erpassist.handlers.quality.get_quality_goals",
				"allowed_roles": ["Quality Manager", "System Manager"]
			},
			
			# Maintenance Actions
			{
				"action_name": "view_maintenance_schedule",
				"action_category": "QUERY",
				"module": "Maintenance",
				"description": "View maintenance schedule",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "erpassist.erpassist.handlers.maintenance.get_maintenance_schedule",
				"allowed_roles": ["Sales User", "System Manager"]
			},
			{
				"action_name": "view_maintenance_visits",
				"action_category": "QUERY",
				"module": "Maintenance",
				"description": "View maintenance visits",
				"enabled": 1,
				"requires_confirmation": 0,
				"risk_level": "Low",
				"handler_function": "erpassist.erpassist.handlers.maintenance.get_maintenance_visits",
				"allowed_roles": ["Sales User", "System Manager"]
			},
		]
		
		for action_data in default_actions:
			# Extract roles
			roles = action_data.pop("allowed_roles", [])
			
			# Check if action already exists
			if frappe.db.exists("ERPAssist Action Registry", action_data["action_name"]):
				continue
			
			# Create action
			action_doc = frappe.get_doc({
				"doctype": "ERPAssist Action Registry",
				**action_data
			})
			
			# Add roles
			for role in roles:
				action_doc.append("allowed_roles", {"role": role})
			
			action_doc.insert()
		
		frappe.db.commit()
