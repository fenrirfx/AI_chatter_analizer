from odoo import http
from odoo.http import request
import json

class AIChatterController(http.Controller):

    @http.route('/ai_chatter/scan', type='json', auth='user', methods=['POST'])
    def scan(self):
        # Try parsing JSON manually from request body
        try:
            data = json.loads(request.httprequest.data.decode('utf-8'))
        except Exception:
            data = {}

        messages_text = data.get('messages', '')
        if not messages_text:
            return {
                'summary': '',
                'urgency': 'unknown',
                'suggestions': [],
            }

        result = request.env['mail.thread'].sudo().ai_analyze_chatter(messages_text)
        return result