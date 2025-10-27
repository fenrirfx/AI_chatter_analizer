from odoo import models, api
import requests
import json


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.model
    def ai_analyze_chatter(self, messages_text):
        summary_text = ''
        urgency = ''
        suggestions = ''
        """Summarize chat messages, classify urgency, and generate suggested responses"""
        if not messages_text:
            return {
                'summary': '',
                'urgency': 'unknown',
                'suggestions': [],
            }
        
        headers = {
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json"
        }

        # --- 1️⃣ Summarization ---
        summary_model = "facebook/bart-large-cnn"
        try:
            summary_resp = requests.post(
                f"https://router.huggingface.co/hf-inference/models/{summary_model}",
                headers=headers,
                json={"inputs": messages_text},
                timeout=30
            )
            summary_json = summary_resp.json()
            summary_text = summary_json[0]["summary_text"] if isinstance(summary_json, list) else str(summary_json)
        except Exception as e:
            summary_text = f"Error generating summary: {str(e)}"

        # --- 2️⃣ Classification (Urgency) ---
        # We'll map POSITIVE / NEGATIVE or other labels to LOW / MEDIUM / HIGH
        classification_model = "cardiffnlp/twitter-roberta-base-sentiment"
        urgency = "unknown"
        try:
            class_resp = requests.post(
                f"https://router.huggingface.co/hf-inference/models/{classification_model}",
                headers=headers,
                json={"inputs": summary_text},
                timeout=30
            )
            class_json = class_resp.json()
            if isinstance(class_json, list) and len(class_json) > 0:
                label = class_json[0][0]
                # Map label to urgency (custom mapping)
                if label in ["NEGATIVE", "LABEL_0"]:
                    urgency = "high"
                elif label in ["POSITIVE", "LABEL_1"]:
                    urgency = "low"
                else:
                    urgency = "medium"
        except Exception as e:
            urgency = "unknown"

        # --- 3️⃣ Text generation / Suggested Responses ---
        model = "meta-llama/Llama-3.1-8B-Instruct"
        url = "https://router.huggingface.co/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"Generate 3 polite and professional response suggestions "
                        f"to this summarized chat:\n\n{summary_text}\n\n"
                        f"Each response should be on a new line."
                    )
                }
            ],
            "max_tokens": 200,
            "temperature": 0.7,
        }

        response = requests.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            text = data["choices"][0]["message"]["content"].strip()
            suggestions = [s.strip("-• ") for s in text.split("\n") if s.strip()]

        return {
            "summary": summary_text,
            "urgency": urgency,
            "suggestions": suggestions,
        }
