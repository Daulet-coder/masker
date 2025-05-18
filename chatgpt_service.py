import openai
from config.settings import OPENAI_API_KEY, OPENAI_CHAT_MODEL
import os # Добавим os для альтернативной загрузки ключа из окружения, если в settings.py пусто

class ChatGPTService:
    def __init__(self):
        # Приоритет: settings.py, затем переменная окружения
        api_key_to_use = OPENAI_API_KEY
        if not api_key_to_use or api_key_to_use == "sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx": # Проверка на плейсхолдер
            api_key_to_use = os.getenv("OPENAI_API_KEY")

        if not api_key_to_use:
            print("ПРЕДУПРЕЖДЕНИЕ: OpenAI API ключ не найден ни в settings.py, ни в переменных окружения.")
            self.client = None
            self.is_configured = False
        else:
            try:
                self.client = openai.OpenAI(api_key=api_key_to_use)
                self.is_configured = True
                print("OpenAI клиент успешно инициализирован.")
            except Exception as e:
                print(f"Ошибка инициализации OpenAI клиента: {e}")
                self.client = None
                self.is_configured = False

    def ask_question(self, masked_context: str, user_question: str) -> str:
        if not self.is_configured or not self.client:
            raise ConnectionError("OpenAI клиент не настроен или не инициализирован.")

        if not masked_context or not user_question:
            raise ValueError("Masked text и вопрос не должны быть пустыми")

        system_prompt = """Ты ассистент, который отвечает на вопросы ИСКЛЮЧИТЕЛЬНО на основе предоставленного текста.
Предоставленный текст — это "Masked Text".
Если ответ на вопрос скрыт символами "*" ты ОБЯЗАН ответить: "В данном тексте эта информация скрыта"
Не используй никакие внешние знания или информацию, не содержащуюся в "Masked Text".
Отвечай на том языке, на котором был задан вопрос
Отвечай кратко и по существу, основываясь только на предоставленном контексте."""

        user_message_content = f"""Контекст (Masked Text):
---
{masked_context}
---

Вопрос: {user_question}"""

        try:
            completion = self.client.chat.completions.create(
                model=OPENAI_CHAT_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message_content}
                ],
                temperature=0.2
            )
            answer = completion.choices[0].message.content
            return answer
        except openai.APIConnectionError as e:
            print(f"Ошибка соединения с OpenAI: {e}")
            raise ConnectionError(f"Не удалось подключиться к OpenAI: {e}")
        except openai.RateLimitError as e:
            print(f"Превышен лимит запросов OpenAI: {e}")
            raise PermissionError(f"Превышен лимит запросов к OpenAI: {e}") # Используем PermissionError для лимитов
        except openai.APIStatusError as e:
            print(f"Ошибка API OpenAI (статус {e.status_code}): {e.response}")
            raise Exception(f"Ошибка API OpenAI (статус {e.status_code}): {e.message}")
        except Exception as e:
            print(f"Неожиданная ошибка при обращении к OpenAI API: {e}")
            raise Exception(f"Неожиданная ошибка при обращении к OpenAI: {str(e)}")