SANBAD - DJANGO STORE WITH AI FASHION ASSISTANT
================================================

This project contains the SANBAD boutique storefront, Django product database,
customer login/registration, and SANBAD STYLE AI chat endpoint.

AI ASSISTANT
- The chat sends messages to Django at /api/style-ai/.
- Django reads active, in-stock products from the Product database.
- The OpenAI API key is read only on the server from OPENAI_API_KEY.
- The key must NEVER be placed in HTML, JavaScript, or shared ZIP files.
- The assistant recommends only products present in the live catalogue.
- API usage may incur charges on the OpenAI Platform account.

SETUP (WINDOWS POWERSHELL)
1. Extract this ZIP and open the folder containing manage.py in VS Code.
2. Open Terminal > New Terminal.
3. Activate your existing virtual environment if you have one.
4. Install dependencies:
      pip install -r requirements.txt
5. Run database migrations:
      python manage.py migrate
6. (Optional) Add sample products:
      python manage.py seed_products
7. Set your API key in PowerShell (replace the placeholder with your own key):
      $env:OPENAI_API_KEY="your_api_key_here"
   This sets it for the current terminal window only. Do not share the key.
8. Start the website in the same terminal:
      python manage.py runserver
9. Open:
      http://127.0.0.1:8000/
10. Open the assistant button and send a test message.

To use the AI in a new terminal window, set OPENAI_API_KEY again before starting
Django. The default model is gpt-5.5. You can override it with OPENAI_MODEL.

PRODUCTS
Manage products at http://127.0.0.1:8000/admin/ . Add product name, category,
price, tag, public image URL, description, stock, and keep Is active checked.
The assistant can only recommend active products that have stock greater than zero.

IMPORTANT
- Your local db.sqlite3, virtual environment, and admin password are not included.
- The OpenAI API key is not included. You must create your own API key and keep it secret.
- AI responses require internet access and an active API account with available billing/credits.
- Checkout remains a WhatsApp demo. No payment gateway or order database is configured.
- Before public launch, configure production security, hosting, domain, and HTTPS.
