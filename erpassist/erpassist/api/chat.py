# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
import json
from frappe import _
from erpassist.erpassist.core.orchestrator import AIOrchestrator
from erpassist.erpassist.core.audit_logger import AuditLogger

@frappe.whitelist()
def send_message(message, session_id=None):
	"""
	Send a message to the AI assistant
	"""
	try:
		user = frappe.session.user
		
		# Create or get session
		if not session_id:
			session = frappe.get_doc({
				"doctype": "ERPAssist Chat Session",
				"user": user,
				"session_title": message[:50] + "..." if len(message) > 50 else message,
				"status": "Active"
			})
			session.insert()
			session_id = session.name
		else:
			session = frappe.get_doc("ERPAssist Chat Session", session_id)
		
		# Add user message to session
		session.append("messages", {
			"role": "user",
			"message": message,
			"timestamp": frappe.utils.now()
		})
		session.save()
		
		# Process with AI Orchestrator
		orchestrator = AIOrchestrator()
		response = orchestrator.process_message(message, session_id, user)
		
		# Add assistant response to session
		session.append("messages", {
			"role": "assistant",
			"message": response.get("message", ""),
			"timestamp": frappe.utils.now(),
			"action_taken": response.get("action_taken"),
			"action_result": json.dumps(response.get("action_result"))
		})
		session.save()
		
		return {
			"success": True,
			"session_id": session_id,
			"response": response
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "ERPAssist Chat Error")
		return {
			"success": False,
			"error": str(e)
		}

@frappe.whitelist()
def get_sessions():
	"""
	Get all chat sessions for the current user
	"""
	try:
		user = frappe.session.user
		sessions = frappe.get_all(
			"ERPAssist Chat Session",
			filters={"user": user},
			fields=["name", "session_title", "status", "created_at", "last_message_at"],
			order_by="last_message_at desc"
		)
		return {
			"success": True,
			"sessions": sessions
		}
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "ERPAssist Get Sessions Error")
		return {
			"success": False,
			"error": str(e)
		}

@frappe.whitelist()
def get_session_messages(session_id):
	"""
	Get all messages from a chat session
	"""
	try:
		session = frappe.get_doc("ERPAssist Chat Session", session_id)
		
		# Check if user has access to this session
		if session.user != frappe.session.user and not frappe.has_permission("ERPAssist Chat Session", "read", session):
			frappe.throw(_("You don't have permission to view this session"))
		
		return {
			"success": True,
			"messages": [msg.as_dict() for msg in session.messages]
		}
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "ERPAssist Get Messages Error")
		return {
			"success": False,
			"error": str(e)
		}

@frappe.whitelist()
def confirm_action(session_id, action_name, parameters):
	"""
	Confirm and execute a pending action
	"""
	try:
		user = frappe.session.user
		orchestrator = AIOrchestrator()
		
		# Parse parameters if it's a string
		if isinstance(parameters, str):
			parameters = json.loads(parameters)
		
		result = orchestrator.execute_action(action_name, parameters, user)
		
		# Log the action
		AuditLogger.log_action(
			user=user,
			action_name=action_name,
			action_category=result.get("category"),
			status="Success" if result.get("success") else "Failed",
			query=json.dumps(parameters),
			result=json.dumps(result.get("data")),
			error_message=result.get("error"),
			session_id=session_id
		)
		
		return result
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "ERPAssist Confirm Action Error")
		return {
			"success": False,
			"error": str(e)
		}
