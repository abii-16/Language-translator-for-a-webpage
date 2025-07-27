# 🌐 Language Translator for a Webpage

A web-based translation tool that dynamically translates form content using cutting-edge online models from Hugging Face — including **Helsinki-NLP**, **mBART**, **M2M100**, and **NLLB**.

## 🚀 Project Overview

This project is a multilingual web form translator built with **Flask (Python backend)** and **HTML/CSS/JavaScript (frontend)**. It allows users to interactively select translation models and target languages, translating the page content in real time.

## 📁 Project Structure

all_lang_models_online/
├── app.py # Flask backend server
├── templates/
│ └── form.html # Web form UI
├── static/
│ └── translate.js # Client-side translation logic


## 🧠 Key Features

- 🔄 **Real-time Translation** of web form content (labels, placeholders, headings, etc.)
- 🌍 **Multi-language Support**: English, Hindi, French, German, and Japanese
- 🔧 **Model Switching**: Dynamically select between different models
- 🧪 **Online Models Used**:
  - MarianMT (Helsinki-NLP)
  - mBART
  - M2M100
  - NLLB (No Language Left Behind)

## ⚙️ API Endpoints

- `POST /set_model`: Loads the selected translation model
- `POST /translate`: Translates given text into the selected language

## 📚 Tech Stack

- **Backend**: Python, Flask, PyTorch
- **Frontend**: HTML, CSS, JavaScript
- **Libraries**:
  - `transformers` (Hugging Face)
  - `torch` (for model execution)

## 🔗 Online Model Access

All models are loaded directly from Hugging Face using `from_pretrained()` at runtime — no prior download required.

## 🖼 UI Features

- 📝 Form inputs for Name, Age, Address, and Country
- 🌐 Floating panel to select language and translation model
- 🔄 Spinner animation during translation activity

## 📝 Notes

- Ensure an active internet connection for model loading.
- Ideal for projects requiring dynamic, client-driven multilingual support without preloading heavy models.



