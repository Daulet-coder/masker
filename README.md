# masker
The best chat with anonymizator

Privacy is a priority - a local anonymization tool for AI.

With the increasing use of AI, privacy protection is becoming critical. Many
companies use AI tools to work effectively, but they
cannot send confidential data to online AI tools, as the data
is sent to third-party servers. Therefore, to work with data, you need to anonymize it
so that the content does not contain private data. The task is to create a local tool for
automatic anonymization of text, images and files before sending them to AI, with
the ability of a chatbot to simplify the process.
The goal: The tool will ensure privacy, increase trust in AI, and help comply with laws
such as GDPR.

COMPONENT ARCHITECTURE — MASKER

Frontend (UI):
User-friendly drag-and-drop interface with an integrated chatbot.

Backend:
NLP module based on BERT and NER models
Document processing (PDF, DOCX — using pdf2image and python-docx)
Text detection in images (via OpenCV)

Local Deployment:
Desktop application (Python GUI)

Chatbot:
LLM-powered (GPT-4o)

Example: Меня зовут Айгуль Сатыбалдиева. Мой ИИН: 991122334455. Рабочий email: a.sat@mail.kz.
Родилась 01.01.1990 в городе Алматы. Телефон: +77015553322. Домашний: 87172223344.
Номер банковского счёта: KZ86125KZT5004100100. Альтернативный счет: 40817810099910004312.
Моя карта: 4400123412341234. IP-адрес устройства: 192.168.1.1.
Мой паспорт: N12345678. Иногда данные попадают в систему без шифрования.
Имя друга: Тимур Ергалиев. Он живёт в Астане. Email его — timur@gmail.com. Его IP: 10.0.0.1.

Output: Меня зовут  *** Мой ИИН: * Рабочий email: * Родилась 01.01.1990 в городе * Телефон: *** Домашний: * Номер банковского счёта: *** Альтернативный счет: *** Моя карта: ** IP-адрес устройства: * Мой паспорт: ** Иногда данные попадают в систему без шифрования. Имя друга:  ** Он живёт в * Email его — ** Его IP: ***

![image](https://github.com/user-attachments/assets/b85f4614-2147-48b7-84b0-786393b79bb1)
![image](https://github.com/user-attachments/assets/aa83dc39-ac47-4e0c-8d47-a014ddf9cf70)



