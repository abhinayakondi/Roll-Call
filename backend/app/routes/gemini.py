from ..services.gemini_service.word_gen import WordGen
from ..services.gemini_service.quote_gen import QuoteGen
from flask import jsonify 
import traceback

from . import gem

@gem.route("/generate_word", methods=['GET'])
def get_word():
    try:
        word_gen = WordGen()
        word = word_gen.get_word()
        print(f"Generated word: {word}")
        return jsonify(word)
    except Exception as e:
        print(f"Error generating word: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@gem.route("/generate_quote", methods=['GET'])
def get_quote():
    try:
        quote_gen = QuoteGen()
        quote = quote_gen.get_quote()
        print(f"Generated quote: {quote}")
        return jsonify(quote)
    except Exception as e:
        print(f"Error generating quote: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500
