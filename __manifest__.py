{
    'name': 'AI Chatter Assistant',
    'version': '1.0',
    'summary': 'Summarize chatter and suggest replies using AI',
    'depends': ['mail', 'web'],
    'data': [
    ],
    'assets': {
        'web.assets_backend': [
            'ai_chatter_assistant/static/css/style.css',
            'ai_chatter_assistant/static/src/js/ai_chatter_button.js',
            # 'ai_chatter_assistant/static/src/xml/ai_chatter_templates.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}