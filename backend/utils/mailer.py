import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi_mail.errors import ConnectionErrors
from config import MAIL_CONFIG

# Используем настройки из config.py
conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_CONFIG["MAIL_USERNAME"],
    MAIL_PASSWORD=MAIL_CONFIG["MAIL_PASSWORD"],
    MAIL_FROM=MAIL_CONFIG["MAIL_FROM"],
    MAIL_PORT=MAIL_CONFIG["MAIL_PORT"],
    MAIL_SERVER=MAIL_CONFIG["MAIL_SERVER"],
    MAIL_STARTTLS=MAIL_CONFIG["MAIL_STARTTLS"],
    MAIL_SSL_TLS=MAIL_CONFIG["MAIL_SSL_TLS"],
    USE_CREDENTIALS=MAIL_CONFIG["USE_CREDENTIALS"],
    VALIDATE_CERTS=MAIL_CONFIG["VALIDATE_CERTS"],
)


def create_verification_email_html(token: str, username: str = None) -> str:
    """Создает HTML для письма подтверждения регистрации"""
    frontend_url = MAIL_CONFIG.get("FRONTEND_URL", "http://localhost:3000")
    verify_url = f"{frontend_url}/verify-email?token={token}"
    
    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Подтверждение регистрации - Film Base API</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                background-color: white;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .logo {{
                font-size: 32px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 10px;
            }}
            .subtitle {{
                color: #7f8c8d;
                font-size: 16px;
            }}
            .content {{
                margin-bottom: 30px;
            }}
            .button {{
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
                text-align: center;
                margin: 20px 0;
                transition: transform 0.2s;
            }}
            .button:hover {{
                transform: translateY(-2px);
            }}
            .footer {{
                border-top: 1px solid #ecf0f1;
                padding-top: 20px;
                margin-top: 30px;
                font-size: 12px;
                color: #7f8c8d;
                text-align: center;
            }}
            .warning {{
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 5px;
                padding: 15px;
                margin: 20px 0;
                color: #856404;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🎬 Film Base API</div>
                <div class="subtitle">Ваша база данных фильмов</div>
            </div>
            
            <div class="content">
                <h2 style="color: #2c3e50;">Добро пожаловать{f', {username}' if username else ''}!</h2>
                
                <p>Спасибо за регистрацию в Film Base API! Мы рады приветствовать вас в нашем сообществе любителей кино.</p>
                
                <p>Для завершения регистрации и активации вашего аккаунта, пожалуйста, подтвердите вашу электронную почту:</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{verify_url}" class="button">✅ Подтвердить почту</a>
                </div>
                
                <div class="warning">
                    <strong>⚠️ Важно:</strong> Если кнопка не работает, скопируйте эту ссылку в браузер:<br>
                    <code style="word-break: break-all;">{verify_url}</code>
                </div>
                
                <p>После подтверждения вы сможете:</p>
                <ul>
                    <li>🔍 Просматривать каталог фильмов</li>
                    <li>⭐ Оставлять комментарии</li>
                    <li>📚 Добавлять фильмы в закладки</li>
                    <li>👤 Управлять профилем</li>
                </ul>
            </div>
            
            <div class="footer">
                <p>Если вы не регистрировались в Film Base API, проигнорируйте это письмо.</p>
                <p>Это автоматическое письмо, не отвечайте на него.</p>
                <p>© 2024 Film Base API. Все права защищены.</p>
            </div>
        </div>
    </body>
    </html>
    """


def create_password_reset_email_html(token: str, username: str = None) -> str:
    """Создает HTML для письма сброса пароля"""
    frontend_url = MAIL_CONFIG.get("FRONTEND_URL", "http://localhost:3000")
    reset_url = f"{frontend_url}/reset-password?token={token}"
    
    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Сброс пароля - Film Base API</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                background-color: white;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .logo {{
                font-size: 32px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 10px;
            }}
            .subtitle {{
                color: #7f8c8d;
                font-size: 16px;
            }}
            .content {{
                margin-bottom: 30px;
            }}
            .button {{
                display: inline-block;
                background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
                text-align: center;
                margin: 20px 0;
                transition: transform 0.2s;
            }}
            .button:hover {{
                transform: translateY(-2px);
            }}
            .footer {{
                border-top: 1px solid #ecf0f1;
                padding-top: 20px;
                margin-top: 30px;
                font-size: 12px;
                color: #7f8c8d;
                text-align: center;
            }}
            .warning {{
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
                border-radius: 5px;
                padding: 15px;
                margin: 20px 0;
                color: #721c24;
            }}
            .info {{
                background-color: #d1ecf1;
                border: 1px solid #bee5eb;
                border-radius: 5px;
                padding: 15px;
                margin: 20px 0;
                color: #0c5460;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🎬 Film Base API</div>
                <div class="subtitle">Ваша база данных фильмов</div>
            </div>
            
            <div class="content">
                <h2 style="color: #e74c3c;">Сброс пароля</h2>
                
                <p>Здравствуйте{f', {username}' if username else ''}!</p>
                
                <p>Мы получили запрос на сброс пароля для вашего аккаунта в Film Base API.</p>
                
                <p>Если это были вы, нажмите кнопку ниже для создания нового пароля:</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_url}" class="button">🔑 Сбросить пароль</a>
                </div>
                
                <div class="warning">
                    <strong>⚠️ Важно:</strong> Если кнопка не работает, скопируйте эту ссылку в браузер:<br>
                    <code style="word-break: break-all;">{reset_url}</code>
                </div>
                
                <div class="info">
                    <strong>ℹ️ Информация:</strong>
                    <ul style="margin: 10px 0;">
                        <li>Эта ссылка действительна в течение <strong>1 часа</strong></li>
                        <li>После сброса пароля все активные сессии будут завершены</li>
                        <li>Рекомендуем использовать надежный пароль</li>
                    </ul>
                </div>
                
                <p><strong>Если вы не запрашивали сброс пароля:</strong></p>
                <ul>
                    <li>Проигнорируйте это письмо</li>
                    <li>Ваш пароль останется без изменений</li>
                    <li>Рекомендуем проверить безопасность аккаунта</li>
                </ul>
            </div>
            
            <div class="footer">
                <p>Если у вас есть вопросы, обратитесь в службу поддержки.</p>
                <p>Это автоматическое письмо, не отвечайте на него.</p>
                <p>© 2024 Film Base API. Все права защищены.</p>
            </div>
        </div>
    </body>
    </html>
    """


async def send_verification_email(email: str, token: str, username: str = None) -> bool:
    """Отправляет письмо подтверждения регистрации"""
    subject = "🎬 Подтвердите регистрацию в Film Base API"
    html_content = create_verification_email_html(token, username)
    
    return await send_email(subject, [email], html_content)


async def send_password_reset_email(email: str, token: str, username: str = None) -> bool:
    """Отправляет письмо сброса пароля"""
    subject = "🔑 Сброс пароля - Film Base API"
    html_content = create_password_reset_email_html(token, username)
    
    return await send_email(subject, [email], html_content)


async def send_email(subject: str, recipients: list[str], html: str) -> bool:
    # Fallback: если не настроены креды, выводим письмо в консоль и не падаем
    if not conf.MAIL_USERNAME or not conf.MAIL_PASSWORD or conf.MAIL_USERNAME == "your_email@gmail.com":
        print(f"[MAIL:FALLBACK] Отправка письма в консоль:")
        print(f"[MAIL:FALLBACK] Тема: {subject}")
        print(f"[MAIL:FALLBACK] Получатели: {recipients}")
        print(f"[MAIL:FALLBACK] Содержимое: {html}")
        return True

    message = MessageSchema(subject=subject, recipients=recipients, body=html, subtype="html")
    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        print(f"[MAIL:SUCCESS] Письмо отправлено на {recipients}")
        return True
    except ConnectionErrors as e:
        print(f"[MAIL:ERROR] Ошибка подключения SMTP: {e}")
        print(f"[MAIL:FALLBACK] Письмо выведено в консоль:")
        print(f"[MAIL:FALLBACK] Тема: {subject}")
        print(f"[MAIL:FALLBACK] Получатели: {recipients}")
        print(f"[MAIL:FALLBACK] Содержимое: {html}")
        return False
    except Exception as e:
        print(f"[MAIL:ERROR] Неожиданная ошибка: {e}")
        print(f"[MAIL:FALLBACK] Письмо выведено в консоль:")
        print(f"[MAIL:FALLBACK] Тема: {subject}")
        print(f"[MAIL:FALLBACK] Получатели: {recipients}")
        print(f"[MAIL:FALLBACK] Содержимое: {html}")
        return False


