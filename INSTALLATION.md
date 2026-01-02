# ERPAssist Installation Guide

## Prerequisites

- Frappe/ERPNext installed (Version 14 or 15 recommended)
- Python 3.8+
- OpenAI API account with API key

## Installation Steps

### 1. Get the App

Navigate to your Frappe bench directory and install the app:

```bash
# Navigate to your bench directory
cd ~/frappe-bench

# Get the app from the directory containing erpassist
bench get-app /path/to/erpassist

# Install the app on your site
bench --site your-site.local install-app erpassist
```

### 2. Configure OpenAI API Key

After installation:

1. Login to your ERPNext site
2. Go to **ERPAssist Settings** (Search in awesome bar)
3. Enter your OpenAI API Key
4. Select your preferred AI Model (default: gpt-4o)
5. Configure other settings as needed
6. Save

### 3. Set Permissions

The default actions are configured with common role permissions. You can customize these:

1. Go to **ERPAssist Action Registry**
2. View or edit existing actions
3. Add/remove roles as needed for each action

### 4. Test the Installation

1. Click the **ERPAssist** button in the navbar (message circle icon)
2. Try asking questions like:
   - "Show me recent sales orders"
   - "What's our current stock of item ABC?"
   - "List all open leads"

## Troubleshooting

### Chat button not appearing
- Clear browser cache: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
- Run: `bench clear-cache`
- Check browser console for JavaScript errors

### Actions not working
- Verify OpenAI API key is correctly configured
- Check ERPAssist Audit Log for error details
- Verify user has required roles for the action

### Permission errors
- Check ERPAssist Action Registry for role requirements
- Ensure user has necessary ERPNext permissions for underlying doctypes

## Configuration

### Enabled Modules

In ERPAssist Settings, you can enable/disable modules:
- CRM
- Selling
- Buying
- Stock
- Accounting
- HR
- Payroll
- Projects
- Support
- Manufacturing
- Assets
- Quality
- Maintenance

### Action Registry

You can add custom actions in ERPAssist Action Registry:

1. Create new ERPAssist Action Registry document
2. Define:
   - Action Name
   - Category (QUERY, DRAFT, APPROVE, POST, EXECUTE_PAYROLL)
   - Module
   - Allowed Roles
   - Handler Function
   - Parameters (JSON format)

## Development

### Creating Custom Handlers

Create handler functions in `erpassist/erpassist/handlers/`:

```python
def my_custom_action(parameters, user):
    """
    Custom action handler
    """
    try:
        # Your logic here
        return {
            "success": True,
            "message": "Action completed",
            "data": {...},
            "type": "table",  # or "text", "draft", etc.
            "category": "QUERY"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "error": str(e)
        }
```

Then register it in ERPAssist Action Registry with handler function path:
`erpassist.erpassist.handlers.module_name.my_custom_action`

## Support

For issues and questions:
- Check ERPAssist Audit Log for detailed error information
- Review browser console for frontend errors
- Check ERPNext error logs: `bench --site your-site.local logs`

## Uninstallation

To uninstall ERPAssist:

```bash
bench --site your-site.local uninstall-app erpassist
```

Note: This will remove all ERPAssist data including chat sessions and audit logs.
