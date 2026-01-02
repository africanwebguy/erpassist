# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
import json
from openai import OpenAI
from erpassist.erpassist.core.action_registry import ActionRegistry
from erpassist.erpassist.core.permission_guard import PermissionGuard
from erpassist.erpassist.core.executor import ActionExecutor
from erpassist.erpassist.core.audit_logger import AuditLogger

class AIOrchestrator:
	"""
	Main orchestrator that processes user messages and coordinates
	all components of the ERPAssist system
	"""
	
	def __init__(self):
		self.settings = frappe.get_single("ERPAssist Settings")
		self.action_registry = ActionRegistry()
		self.permission_guard = PermissionGuard()
		self.executor = ActionExecutor()
		
		# Initialize OpenAI client
		api_key = self.settings.get_password("openai_api_key")
		if not api_key:
			frappe.throw("OpenAI API Key not configured in ERPAssist Settings")
		
		self.client = OpenAI(api_key=api_key)
		self.model = self.settings.ai_model or "gpt-4o"
	
	def process_message(self, message, session_id, user):
		"""
		Process a user message and generate a response
		"""
		try:
			# Get user roles
			user_roles = frappe.get_roles(user)
			
			# Get available actions for this user
			available_actions = self.action_registry.get_available_actions(user_roles)
			
			# Build context for AI
			system_prompt = self._build_system_prompt(user_roles, available_actions)
			
			# Get session history for context
			session_history = self._get_session_history(session_id)
			
			# Call OpenAI API
			messages = [
				{"role": "system", "content": system_prompt},
				*session_history,
				{"role": "user", "content": message}
			]
			
			response = self.client.chat.completions.create(
				model=self.model,
				messages=messages,
				max_tokens=self.settings.max_tokens or 4000,
				temperature=0.7,
				functions=self._get_function_definitions(available_actions),
				function_call="auto"
			)
			
			# Process response
			choice = response.choices[0]
			
			# Check if AI wants to call a function
			if choice.message.function_call:
				return self._handle_function_call(
					choice.message.function_call,
					user,
					session_id
				)
			else:
				return {
					"message": choice.message.content,
					"type": "text",
					"action_taken": None
				}
				
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "AI Orchestrator Error")
			return {
				"message": f"I encountered an error while processing your request: {str(e)}",
				"type": "error",
				"error": str(e)
			}
	
	def _build_system_prompt(self, user_roles, available_actions):
		"""
		Build the system prompt for the AI with context about ERPNext and available actions
		"""
		actions_desc = "\n".join([
			f"- {action['name']}: {action.get('description', '')} (Category: {action['category']}, Module: {action['module']})"
			for action in available_actions
		])
		
		return f"""You are ERPAssist, an AI assistant for ERPNext. You help users with their ERP tasks.

Current User Roles: {', '.join(user_roles)}

IMPORTANT RULES:
1. NEVER guess or hallucinate data. Only use data from ERPNext via the available functions.
2. Always respect user permissions. You can only perform actions the user has permission for.
3. For financial actions (POST) and payroll (EXECUTE_PAYROLL), always ask for explicit confirmation.
4. Be concise and professional in your responses.
5. When showing data, format it clearly with tables when appropriate.

AVAILABLE ACTIONS:
{actions_desc}

When a user asks about data, use the appropriate query function. When they want to create or modify something, use the appropriate action function. Always explain what you're going to do before calling a function that requires confirmation."""
	
	def _get_session_history(self, session_id):
		"""
		Get the conversation history from the session
		"""
		try:
			session = frappe.get_doc("ERPAssist Chat Session", session_id)
			history = []
			
			# Only include last 10 messages to avoid token limits
			for msg in session.messages[-10:]:
				history.append({
					"role": msg.role,
					"content": msg.message
				})
			
			return history
		except:
			return []
	
	def _get_function_definitions(self, available_actions):
		"""
		Convert available actions to OpenAI function definitions
		"""
		functions = []
		
		for action in available_actions:
			# Parse parameters if they exist
			parameters = {"type": "object", "properties": {}, "required": []}
			
			if action.get("parameters"):
				try:
					param_def = json.loads(action["parameters"])
					parameters = param_def
				except:
					pass
			
			functions.append({
				"name": action["name"],
				"description": action.get("description", ""),
				"parameters": parameters
			})
		
		return functions if functions else None
	
	def _handle_function_call(self, function_call, user, session_id):
		"""
		Handle when AI wants to call a function
		"""
		function_name = function_call.name
		
		try:
			arguments = json.loads(function_call.arguments)
		except:
			arguments = {}
		
		# Get action details
		action = self.action_registry.get_action(function_name)
		
		if not action:
			return {
				"message": f"Action '{function_name}' is not available.",
				"type": "error"
			}
		
		# Check if action requires confirmation
		if action.get("requires_confirmation") or action.get("action_category") in ["POST", "EXECUTE_PAYROLL"]:
			return {
				"message": f"I need your confirmation to proceed with: {action.get('description', function_name)}",
				"type": "confirmation_required",
				"action_name": function_name,
				"action_details": action,
				"parameters": arguments
			}
		
		# Execute action directly
		return self.execute_action(function_name, arguments, user, session_id)
	
	def execute_action(self, action_name, parameters, user, session_id=None):
		"""
		Execute an action with permission checks
		"""
		try:
			# Get action
			action = self.action_registry.get_action(action_name)
			
			if not action:
				return {
					"success": False,
					"message": "Action not found",
					"error": "Action not found"
				}
			
			# Check permissions
			if not self.permission_guard.check_permission(user, action):
				return {
					"success": False,
					"message": "You don't have permission to perform this action",
					"error": "Permission denied"
				}
			
			# Execute action
			result = self.executor.execute(action, parameters, user)
			
			# Log action
			if self.settings.enable_audit_log:
				AuditLogger.log_action(
					user=user,
					action_name=action_name,
					action_category=action.get("action_category"),
					status="Success" if result.get("success") else "Failed",
					query=json.dumps(parameters),
					result=json.dumps(result.get("data")),
					error_message=result.get("error"),
					session_id=session_id
				)
			
			return result
			
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), f"Execute Action Error: {action_name}")
			return {
				"success": False,
				"message": f"Error executing action: {str(e)}",
				"error": str(e)
			}
