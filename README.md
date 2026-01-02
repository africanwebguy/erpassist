# ERPAssist - AI-Powered Assistant for ERPNext

ERPAssist is a role-aware AI chatbot that integrates seamlessly with ERPNext to help users query data, generate visualizations, prepare drafts, execute approved actions, and export data while respecting permissions and workflows.

## Features

- **Role-Aware**: Respects ERPNext user roles and permissions
- **Never Hallucinates**: Only provides accurate data from your ERPNext system
- **Action Registry**: Whitelisted actions ensure safe operations
- **Audit Trail**: Complete logging of all AI actions
- **Visualizations**: Generate charts and export to Excel, PDF, and images
- **Multi-Module Support**: CRM, Selling, Buying, Stock, Accounting, HR, Payroll, Projects, Manufacturing, Support, Assets, Quality, and Maintenance

## Installation

### Method 1: From Directory (Recommended)

1. Extract the zip file:
```bash
unzip erpassist.zip
```

2. Get the app from your bench directory:
```bash
cd ~/frappe-bench
bench get-app /path/to/erpassist
```

3. Install the app on your site:
```bash
bench --site your-site.local install-app erpassist
```

4. Clear cache and restart:
```bash
bench --site your-site.local clear-cache
bench restart
```

### Method 2: Development Install

For development or testing:
```bash
cd ~/frappe-bench/apps
unzip /path/to/erpassist.zip
cd erpassist
pip install -e .
bench --site your-site.local install-app erpassist
```

### Post-Installation

5. Configure your OpenAI API key in ERPNext:
   - Go to **ERPAssist Settings**
   - Enter your OpenAI API key
   - Save

6. Hard refresh your browser:
   - Windows/Linux: `Ctrl + Shift + R`
   - Mac: `Cmd + Shift + R`

## Troubleshooting Installation

### Issue: "App not found in apps.txt"
**Solution:**
```bash
cd ~/frappe-bench
bench get-app /absolute/path/to/erpassist
```
Make sure to use absolute path, not relative path.

### Issue: "No module named 'erpassist'"
**Solution:**
```bash
cd ~/frappe-bench/apps/erpassist
pip install -e . --break-system-packages
bench restart
```

### Issue: "DocType not found"
**Solution:**
```bash
bench --site your-site.local migrate
bench --site your-site.local clear-cache
bench restart
```

### Issue: Chat button not appearing
**Solution:**
```bash
bench --site your-site.local clear-cache
bench build --app erpassist
bench restart
```
Then hard refresh browser.

### Issue: Permission errors during installation
**Solution:**
```bash
# Fix file permissions
cd ~/frappe-bench/apps/erpassist
chmod -R 755 .
bench --site your-site.local install-app erpassist
```

### Issue: "ImportError: cannot import name..."
**Solution:**
```bash
# Reinstall dependencies
cd ~/frappe-bench/apps/erpassist
pip install -r requirements.txt --upgrade --break-system-packages
bench restart
```

## Usage

1. Click the **ERPAssist** button in the ERPNext navbar (message circle icon)
2. Type your question or request in natural language
3. The AI will respond with data, visualizations, or ask for confirmation for actions
4. Confirm any actions that require approval

## Supported Actions (23 Total)

### CRM (2 actions)
- View leads summary
- View opportunities

### Selling (2 actions)
- View sales orders
- Create draft sales order

### Buying (1 action)
- View purchase orders

### Stock (1 action)
- View stock summary

### Accounting (2 actions)
- View account balances
- Create draft journal entry

### HR (2 actions)
- View employee list
- Approve leave application

### Payroll (1 action)
- Execute payroll

### Projects (2 actions)
- View projects summary
- View tasks summary

### Manufacturing (2 actions)
- View work orders
- View BOM summary

### Support (2 actions)
- View issues summary
- View SLA compliance

### Assets (2 actions)
- View assets summary
- View asset maintenance schedule

### Quality (2 actions)
- View quality inspections
- View quality goals

### Maintenance (2 actions)
- View maintenance schedule
- View maintenance visits

## Security

- All actions respect ERPNext permissions
- Action Registry ensures only whitelisted operations
- Complete audit logging in ERPAssist Audit Log
- Confirmation required for financial and payroll actions

## Configuration

Configure ERPAssist through **ERPAssist Settings** doctype:
- OpenAI API Key
- AI Model selection (gpt-4o, gpt-4o-mini, gpt-4-turbo)
- Enable/disable specific modules
- Configure action permissions
- Enable/disable audit logging

## Development

### File Structure
```
erpassist/
├── erpassist/
│   ├── erpassist/
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Core business logic
│   │   ├── doctype/          # ERPNext doctypes
│   │   └── handlers/         # Module-specific handlers
│   ├── public/
│   │   ├── css/              # Stylesheets
│   │   └── js/               # JavaScript
│   ├── hooks.py              # App hooks
│   └── install.py            # Installation script
├── README.md
├── INSTALLATION.md
├── setup.py
└── requirements.txt
```

### Adding Custom Handlers

See INSTALLATION.md for detailed instructions on creating custom actions.

## Requirements

- Frappe/ERPNext Version 14 or 15
- Python 3.8+
- OpenAI API account with API key

## Support

For detailed installation and customization instructions, see:
- **INSTALLATION.md** - Complete installation guide
- **SETUP_GUIDE.md** - Comprehensive setup and usage guide

For issues:
- Check ERPAssist Audit Log for error details
- Review browser console for frontend errors
- Check ERPNext error logs: `bench --site your-site.local logs`

## License

MIT

## Credits

Built with ❤️ for the ERPNext community

