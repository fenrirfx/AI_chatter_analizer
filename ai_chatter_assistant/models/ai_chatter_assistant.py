from odoo import models, api
import requests


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.model
    def ai_analyze_chatter(self, messages_text):
        """
        Analyze chatter messages: summarize, assess urgency, and recommend a course of action.
        Uses Hugging Face token and models stored in ir.config_parameter.
        """
        if not messages_text:
            return {
                "summary": "",
                "urgency": "unknown",
                "recommendation": "No messages found to analyze.",
            }

        # Get token and models from ir.config_parameter
        param_obj = self.env['ir.config_parameter'].sudo()
        hf_token = param_obj.get_param('ai_chatter.hf_token', default='')
        summary_model = param_obj.get_param('ai_chatter.summary_model', default='facebook/bart-large-cnn')
        classification_model = param_obj.get_param('ai_chatter.classification_model', default='cardiffnlp/twitter-roberta-base-sentiment')
        recommendation_model = param_obj.get_param('ai_chatter.recommendation_model', default='meta-llama/Llama-3.1-8B-Instruct')

        headers = {
            "Authorization": f"Bearer {hf_token}",
            "Content-Type": "application/json"
        }

        # --- 1️⃣ Summarization ---
        summary_text = ""
        try:
            summary_resp = requests.post(
                f"https://router.huggingface.co/hf-inference/models/{summary_model}",
                headers=headers,
                json={"inputs": messages_text},
                timeout=30
            )
            summary_json = summary_resp.json()
            summary_text = summary_json[0].get("summary_text") if isinstance(summary_json, list) else str(summary_json)
        except Exception as e:
            summary_text = f"Error generating summary: {str(e)}"

        # --- 2️⃣ Urgency Classification ---
        urgency = "unknown"
        try:
            class_resp = requests.post(
                f"https://router.huggingface.co/hf-inference/models/{classification_model}",
                headers=headers,
                json={"inputs": summary_text},
                timeout=30
            )
            class_json = class_resp.json()
            if isinstance(class_json, list) and class_json and isinstance(class_json[0], list):
                label = class_json[0][0]
                if label in ["NEGATIVE", "LABEL_0"]:
                    urgency = "high"
                elif label in ["POSITIVE", "LABEL_1"]:
                    urgency = "low"
                else:
                    urgency = "medium"
        except Exception:
            urgency = "unknown"

        # --- 3️⃣ Recommended Course of Action ---
        recommendation = "Unable to generate recommendation."
        try:
            payload = {
                "model": recommendation_model,
                "messages": [
                    {
                        "role": "user",
                        "content": (
                            f"Based on this summarized chat:\n\n{summary_text}\n\n"
                            f"Provide a concise recommendation for the next best course of action. "
                            f"The recommendation should be clear, practical, and professional."
                        ),
                    }
                ],
                "max_tokens": 200,
                "temperature": 0.6,
            }
            response = requests.post(
                "https://router.huggingface.co/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                recommendation = (
                    data["choices"][0]["message"]["content"].strip()
                    if data.get("choices") else "No recommendation returned."
                )
            else:
                recommendation = f"Model error: {response.status_code}"
        except Exception as e:
            recommendation = f"Error generating recommendation: {str(e)}"

        return {
            "summary": summary_text,
            "urgency": urgency.upper(),
            "recommendation": recommendation,
        }
