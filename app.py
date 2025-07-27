from flask import Flask, request, jsonify, render_template
from transformers import (
    MarianMTModel, MarianTokenizer,
    MBartForConditionalGeneration, MBart50TokenizerFast,
    M2M100ForConditionalGeneration, M2M100Tokenizer,
    AutoModelForSeq2SeqLM, AutoTokenizer
)
import torch

app = Flask(__name__, static_url_path='/static')

# Device config
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Global model and tokenizer
model = None
tokenizer = None
model_type = None

# Loadable models with corresponding tokenizer class and language code settings
MODEL_CONFIGS = {
    "helsinki": {
        "model_name": "Helsinki-NLP/opus-mt-en-fr",
        "class": (MarianMTModel, MarianTokenizer),
        "src_lang": "en",
        "tgt_langs": {
            "fr_XX": "Helsinki-NLP/opus-mt-en-fr",
            "hi_IN": "Helsinki-NLP/opus-mt-en-hi",
            "de_DE": "Helsinki-NLP/opus-mt-en-de",
            "ja_XX": "Helsinki-NLP/opus-mt-en-ja"
        }
    },
    "mbart": {
        "model_name": "facebook/mbart-large-50-many-to-many-mmt",
        "class": (MBartForConditionalGeneration, MBart50TokenizerFast),
        "src_lang": "en_XX",
        "lang_map": {
            "hi_IN": "hi_IN",
            "fr_XX": "fr_XX",
            "de_DE": "de_DE",
            "ja_XX": "ja_XX"
        }
    },
    "m2m100": {
        "model_name": "facebook/m2m100_418M",
        "class": (M2M100ForConditionalGeneration, M2M100Tokenizer),
        "src_lang": "en",
        "lang_map": {
            "hi_IN": "hi",
            "fr_XX": "fr",
            "de_DE": "de",
            "ja_XX": "ja"
        }
    },
    "nllb": {
        "model_name": "facebook/nllb-200-distilled-600M",
        "class": (AutoModelForSeq2SeqLM, AutoTokenizer),
        "src_lang": "eng_Latn",
        "lang_map": {
            "hi_IN": "hin_Deva",
            "fr_XX": "fra_Latn",
            "de_DE": "deu_Latn",
            "ja_XX": "jpn_Jpan"
        }
    }
}

@app.route("/")
def home():
    return render_template("form.html")

@app.route("/set_model", methods=["POST"])
def set_model():
    global model, tokenizer, model_type

    req = request.json
    model_type = req.get("model_type", "helsinki")
    target_lang = req.get("target_lang", "fr_XX")

    if model_type not in MODEL_CONFIGS:
        return jsonify({"error": "Invalid model type"}), 400

    config = MODEL_CONFIGS[model_type]
    ModelClass, TokenizerClass = config["class"]

    try:
        if model_type == "helsinki":
            model_name = config["tgt_langs"][target_lang]
        else:
            model_name = config["model_name"]

        tokenizer = TokenizerClass.from_pretrained(model_name)
        model = ModelClass.from_pretrained(model_name).to(device)

        return jsonify({"status": "Model loaded successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/translate", methods=["POST"])
def translate():
    global model, tokenizer, model_type

    data = request.json
    text = data.get("text", "")
    target_lang = data.get("target_lang", "fr_XX")

    if not model or not tokenizer:
        return jsonify({"translation": text})

    try:
        config = MODEL_CONFIGS[model_type]

        if model_type == "helsinki":
            input_tokens = tokenizer([text], return_tensors="pt", padding=True).to(device)
            translated = model.generate(**input_tokens)
            result = tokenizer.decode(translated[0], skip_special_tokens=True)

        elif model_type == "mbart":
            tokenizer.src_lang = config["src_lang"]
            input_tokens = tokenizer(text, return_tensors="pt").to(device)
            forced_bos = tokenizer.lang_code_to_id[config["lang_map"][target_lang]]
            translated = model.generate(**input_tokens, forced_bos_token_id=forced_bos)
            result = tokenizer.decode(translated[0], skip_special_tokens=True)

        elif model_type == "m2m100":
            tokenizer.src_lang = config["src_lang"]
            input_tokens = tokenizer(text, return_tensors="pt").to(device)
            translated = model.generate(**input_tokens, forced_bos_token_id=tokenizer.get_lang_id(config["lang_map"][target_lang]))
            result = tokenizer.decode(translated[0], skip_special_tokens=True)

        elif model_type == "nllb":
            tokenizer.src_lang = config["src_lang"]
            input_tokens = tokenizer(text, return_tensors="pt").to(device)
            translated = model.generate(**input_tokens, forced_bos_token_id=tokenizer.convert_tokens_to_ids(config["lang_map"][target_lang]))
            result = tokenizer.decode(translated[0], skip_special_tokens=True)

        else:
            result = text

        return jsonify({"translation": result})
    except Exception as e:
        return jsonify({"translation": text, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)