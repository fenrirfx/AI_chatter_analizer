# AI Chatter Assistant for Odoo 19

**Version:** 1.0  
**Author:** FenrirFX Gaming  
**Price:** €100  
**Supported Odoo Version:** 19  
**License:** OPL-1  

---

## Overview

**AI Chatter Assistant** enhances Odoo chatter and discuss threads by providing AI-powered insights.  

With this module, you can:

- **Summarize** chatter messages automatically.
- **Classify urgency** of conversations: LOW, MEDIUM, HIGH.
- **Generate a recommended course of action** for your next steps.

The module integrates directly into **Chat Windows** and **Discuss views**, making it easy to analyze conversations with a single click.

---

## Requirements

- **Odoo 19** (Community or Enterprise edition)  
- **Hugging Face API Token** — required to access the AI models used for summarization, classification, and recommendation.  

> ⚠️ **Note:** Hugging Face models are used under their terms. Users must provide their own API key.

---

## Features

- Button added in chat windows/discuss threads to quickly analyze messages.
- AI generates:
  - **Summary**
  - **Urgency** (LOW, MEDIUM, HIGH)
  - **Recommended course of action**
- **Customizable**: Change models for summarization, classification, or recommendations via Odoo `ir.config_parameter`.
- Easy integration with existing chatter, non-intrusive design.

---

## Installation

1. Copy the `ai_chatter_assistant` folder into your Odoo `addons` directory.  
2. Update the Apps list in Odoo and install **AI Chatter Assistant**.  
3. Add your Hugging Face API key via **Settings → Technical → Parameters → System Parameters**:  
   - `ai_chatter.hf_token` → Your Hugging Face API token  
   - `ai_chatter.summary_model` → e.g., `facebook/bart-large-cnn`  
   - `ai_chatter.classification_model` → e.g., `cardiffnlp/twitter-roberta-base-sentiment`  
   - `ai_chatter.recommendation_model` → e.g., `meta-llama/Llama-3.1-8B-Instruct`  

---

## Usage

1. Open any chatter or discuss thread.  
2. Click the **Analyze AI** button.  
3. The AI modal will display:  
   - **Summary of messages**  
   - **Recommended course of action**  
   - **Urgency level**, which is also displayed as a colored indicator.  

---

## Customization

You can easily update the models by changing the system parameters in Odoo:

- Summarization model
- Urgency classification model
- Recommendation model  

This allows your AI setup to improve over time without touching the module code.

---

## Support

- **Supported Odoo Version:** 19  
- **Support:** Included with purchase for installation, bug fixes, and guidance.  
- Contact: [your email or website]

---

## Credits

- **Hugging Face** — AI models used in this module.  
- **FenrirFX Gaming** — Module development, packaging, and support.

---

## License

This module is distributed under **OPL-1 (Odoo Proprietary License v1.0)**.
