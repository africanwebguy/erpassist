from . import __version__ as app_version

app_name = "erpassist"
app_title = "ERPAssist"
app_publisher = "Your Company"
app_description = "AI-powered assistant for ERPNext"
app_email = "support@yourcompany.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/erpassist/css/erpassist.css"
app_include_js = "/assets/erpassist/js/erpassist.bundle.js"


# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "erpassist.utils.jinja_methods",
#	"filters": "erpassist.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "erpassist.install.before_install"
after_install = "erpassist.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "erpassist.uninstall.before_uninstall"
# after_uninstall = "erpassist.uninstall.after_uninstall"

# Desk Notifications
# -------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "erpassist.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"erpassist.tasks.all"
#	],
#	"daily": [
#		"erpassist.tasks.daily"
#	],
#	"hourly": [
#		"erpassist.tasks.hourly"
#	],
#	"weekly": [
#		"erpassist.tasks.weekly"
#	],
#	"monthly": [
#		"erpassist.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "erpassist.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "erpassist.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "erpassist.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]


# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"erpassist.auth.validate"
# ]
