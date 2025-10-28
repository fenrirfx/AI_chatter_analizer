{
    'name': 'AI Chatter Assistant',
    'version': '1.0',
    'summary': 'Enhance chatter with AI: summary, urgency, and recommended actions',
    'description': """
AI Chatter Assistant allows you to quickly analyze Odoo chatter threads or discuss messages.
Features include:
- Summarizing chatter messages.
- Classifying the urgency of a conversation (LOW, MEDIUM, HIGH).
- Providing a professional recommendation for next steps.

Key points:
- Integrates directly into chat windows and discuss views.
- Fully customizable: future updates can allow switching to alternative AI models.
- Requires a Hugging Face API token for AI model access.
- Credit to Hugging Face for the AI models used.
""",
    'author': 'Filipe Guilherme Vieira',
    'website': 'https://yourwebsite.com',
    'category': 'Tools',
    'license': 'OPL-1',
    'depends': ['mail', 'web'],
    'data': [
        'data/ir_config_parameter.xml',  # stores API key and model names
    ],
    'assets': {
        'web.assets_backend': [
            'ai_chatter_assistant/static/css/style.css',
            'ai_chatter_assistant/static/src/js/ai_chatter_button.js',
        ],
    },
    'icon': 'static/description/icon.png',
    'images': [
        'static/description/cover.png',      # main banner (optional)
        'static/description/screenshot_01.png',
        'static/description/screenshot_02.png',
        'static/description/screenshot_03.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 100.0,
    'currency': 'EUR',
}
