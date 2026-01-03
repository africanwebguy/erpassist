import frappe

def get_context(context):
	"""
	Context for ERPAssist Chat page
	"""
	context.no_cache = 1
	context.show_sidebar = False
	
	# Check if user is logged in
	if frappe.session.user == 'Guest':
		frappe.throw('Please login to use ERPAssist', frappe.PermissionError)
	
	# Get ERPAssist Settings
	settings = frappe.get_single('ERPAssist Settings')
	
	context.api_key_configured = bool(settings.openai_api_key)
	context.ai_model = settings.ai_model or 'gpt-4o'
	
	return context
