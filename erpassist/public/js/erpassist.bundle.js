/**
 * ERPAssist - AI Chat Interface
 * Main JavaScript file for chat functionality
 */

frappe.provide('erpassist');

erpassist.ChatPanel = class ChatPanel {
	constructor() {
		this.session_id = null;
		this.messages = [];
		this.is_open = false;
		this.init();
	}

	init() {
		// Add chat button to navbar
		this.add_chat_button();
		
		// Create chat panel
		this.create_panel();
		
		// Bind events
		this.bind_events();
	}

	add_chat_button() {
		const navbar = $('header.navbar');
		const chat_button = $(`
			<li class="nav-item">
				<a class="nav-link" id="erpassist-chat-btn" title="${__('ERPAssist AI Chat')}">
					<svg class="icon icon-md">
						<use href="#icon-message-circle"></use>
					</svg>
				</a>
			</li>
		`);
		
		navbar.find('.navbar-nav').append(chat_button);
	}

	create_panel() {
		const panel_html = `
			<div id="erpassist-chat-panel" class="erpassist-chat-panel" style="display: none;">
				<div class="chat-header">
					<h5>${__('ERPAssist AI')}</h5>
					<button class="btn btn-sm btn-close" id="erpassist-close-btn">&times;</button>
				</div>
				<div class="chat-messages" id="erpassist-messages"></div>
				<div class="chat-input-area">
					<div class="input-group">
						<input type="text" class="form-control" id="erpassist-input" 
							placeholder="${__('Ask me anything...')}" />
						<button class="btn btn-primary" id="erpassist-send-btn">
							${__('Send')}
						</button>
					</div>
				</div>
			</div>
		`;
		
		$('body').append(panel_html);
		this.$panel = $('#erpassist-chat-panel');
		this.$messages = $('#erpassist-messages');
		this.$input = $('#erpassist-input');
	}

	bind_events() {
		// Toggle panel
		$(document).on('click', '#erpassist-chat-btn', () => {
			this.toggle_panel();
		});

		// Close panel
		$(document).on('click', '#erpassist-close-btn', () => {
			this.close_panel();
		});

		// Send message
		$(document).on('click', '#erpassist-send-btn', () => {
			this.send_message();
		});

		// Send on Enter key
		this.$input.on('keypress', (e) => {
			if (e.which === 13) {
				this.send_message();
			}
		});
	}

	toggle_panel() {
		if (this.is_open) {
			this.close_panel();
		} else {
			this.open_panel();
		}
	}

	open_panel() {
		this.$panel.show();
		this.is_open = true;
		this.$input.focus();
	}

	close_panel() {
		this.$panel.hide();
		this.is_open = false;
	}

	send_message() {
		const message = this.$input.val().trim();
		
		if (!message) {
			return;
		}

		// Clear input
		this.$input.val('');

		// Add user message to UI
		this.add_message('user', message);

		// Show typing indicator
		this.show_typing();

		// Send to server
		frappe.call({
			method: 'erpassist.erpassist.api.chat.send_message',
			args: {
				message: message,
				session_id: this.session_id
			},
			callback: (r) => {
				this.hide_typing();
				
				if (r.message && r.message.success) {
					this.session_id = r.message.session_id;
					const response = r.message.response;
					
					// Add assistant response
					this.add_message('assistant', response.message);
					
					// Handle special response types
					if (response.type === 'confirmation_required') {
						this.show_confirmation(response);
					} else if (response.type === 'table') {
						this.show_table(response.data);
					}
				} else {
					this.add_message('assistant', 'Sorry, I encountered an error. Please try again.');
				}
			},
			error: () => {
				this.hide_typing();
				this.add_message('assistant', 'Sorry, I encountered an error. Please try again.');
			}
		});
	}

	add_message(role, content) {
		const message_class = role === 'user' ? 'user-message' : 'assistant-message';
		const message_html = `
			<div class="chat-message ${message_class}">
				<div class="message-content">${frappe.utils.escape_html(content)}</div>
			</div>
		`;
		
		this.$messages.append(message_html);
		this.scroll_to_bottom();
	}

	show_typing() {
		const typing_html = `
			<div class="chat-message assistant-message typing-indicator" id="typing-indicator">
				<div class="message-content">
					<span class="dot"></span>
					<span class="dot"></span>
					<span class="dot"></span>
				</div>
			</div>
		`;
		
		this.$messages.append(typing_html);
		this.scroll_to_bottom();
	}

	hide_typing() {
		$('#typing-indicator').remove();
	}

	show_confirmation(response) {
		const confirm_html = `
			<div class="confirmation-box">
				<p><strong>${__('Action:')} </strong>${response.action_details.description}</p>
				<div class="btn-group">
					<button class="btn btn-sm btn-success confirm-action-btn" 
						data-action="${response.action_name}"
						data-params='${JSON.stringify(response.parameters)}'>
						${__('Confirm')}
					</button>
					<button class="btn btn-sm btn-secondary cancel-action-btn">
						${__('Cancel')}
					</button>
				</div>
			</div>
		`;
		
		this.$messages.append(confirm_html);
		this.scroll_to_bottom();

		// Bind confirmation buttons
		$(document).on('click', '.confirm-action-btn', (e) => {
			const $btn = $(e.currentTarget);
			const action_name = $btn.data('action');
			const parameters = $btn.data('params');
			
			this.confirm_action(action_name, parameters);
			$btn.closest('.confirmation-box').remove();
		});

		$(document).on('click', '.cancel-action-btn', (e) => {
			$(e.currentTarget).closest('.confirmation-box').remove();
			this.add_message('assistant', 'Action cancelled.');
		});
	}

	confirm_action(action_name, parameters) {
		this.show_typing();
		
		frappe.call({
			method: 'erpassist.erpassist.api.chat.confirm_action',
			args: {
				session_id: this.session_id,
				action_name: action_name,
				parameters: parameters
			},
			callback: (r) => {
				this.hide_typing();
				
				if (r.message && r.message.success) {
					this.add_message('assistant', r.message.message);
				} else {
					this.add_message('assistant', 'Action failed: ' + (r.message.error || 'Unknown error'));
				}
			}
		});
	}

	show_table(data) {
		// Simple table rendering - can be enhanced
		if (data.leads || data.sales_orders || data.purchase_orders || data.stock_balances || data.accounts || data.employees) {
			const items = data.leads || data.sales_orders || data.purchase_orders || data.stock_balances || data.accounts || data.employees;
			
			if (items && items.length > 0) {
				const keys = Object.keys(items[0]);
				let table_html = '<table class="table table-sm table-bordered"><thead><tr>';
				
				keys.forEach(key => {
					table_html += `<th>${key}</th>`;
				});
				
				table_html += '</tr></thead><tbody>';
				
				items.slice(0, 10).forEach(item => {
					table_html += '<tr>';
					keys.forEach(key => {
						table_html += `<td>${item[key] || ''}</td>`;
					});
					table_html += '</tr>';
				});
				
				table_html += '</tbody></table>';
				
				if (items.length > 10) {
					table_html += `<p class="text-muted">${__('Showing 10 of')} ${items.length} ${__('records')}</p>`;
				}
				
				this.$messages.append(table_html);
				this.scroll_to_bottom();
			}
		}
	}

	scroll_to_bottom() {
		this.$messages.scrollTop(this.$messages[0].scrollHeight);
	}
};

// Initialize on page load
frappe.ready(() => {
	if (frappe.session.user !== 'Guest') {
		window.erpassist_chat = new erpassist.ChatPanel();
	}
});
