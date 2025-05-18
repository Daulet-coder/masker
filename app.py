from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename

from services.ner_service import NerService
from services.file_extraction import extract_text
from utils.text_masking import mask_entities_by_token
from services.chatgpt_service import ChatGPTService

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ner = NerService()
chatgpt = ChatGPTService()

@app.route('/', methods=['GET', 'POST'])
def index():
    text = ""
    masked_text = ""
    file_name_for_template = ""

    if request.method == 'POST':
        file = request.files.get('file')
        input_text = request.form.get('text', '')

        if file and file.filename:
            uploaded_file_name = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file_name)
            try:
                file.save(path)
                text = extract_text(path)
                if text:
                    file_name_for_template = uploaded_file_name
                else:
                    file_name_for_template = uploaded_file_name
            except Exception as e:
                print(f"Error processing file {uploaded_file_name}: {e}")
        elif input_text.strip():
            text = input_text.strip()

        if text:
            entities = ner.predict(text)
            masked_text = mask_entities_by_token(text, entities, entity_types_to_mask={
                'PERSON', 'LOCATION', 'CONTACT', 'CARDINAL', 'MISCELLANEOUS', 'GPE', 'ORGANIZATION', 'ID', 'DATE'
            })
        elif not text and file_name_for_template: # Файл был, но текст не извлекся
            pass
        else: # Нет ни файла, ни текста
            text = ""
            masked_text = ""

    return render_template("index.html",
                           original_text=text,
                           masked_text=masked_text,
                           submitted_file_name=file_name_for_template,
                           chatgpt_configured=chatgpt.is_configured)

@app.route('/ask_chatgpt', methods=['POST'])
def ask_chatgpt_route():
    if not chatgpt.is_configured:
        return jsonify({'error': 'Сервис ChatGPT не настроен. Проверьте API ключ.'}), 503

    data = request.get_json()
    masked_context = data.get('masked_text')
    user_question = data.get('question')

    try:
        answer = chatgpt.ask_question(masked_context, user_question)
        return jsonify({'answer': answer})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except ConnectionError as e:
         return jsonify({'error': str(e)}), 503
    except PermissionError as e:
        return jsonify({'error': str(e)}), 429
    except Exception as e:
        print(f"Неожиданная ошибка в маршруте /ask_chatgpt: {e}")
        return jsonify({'error': f'Произошла внутренняя ошибка сервера: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)