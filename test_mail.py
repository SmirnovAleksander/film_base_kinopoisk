#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест отправки почты для Film Base API
"""

import asyncio
from backend.utils.mailer import send_email


async def test_email():
    """Тестирует отправку почты"""
    print("🧪 Тестирование отправки почты...")
    
    # Тестовые данные
    subject = "Тест подтверждения почты - Film Base API"
    recipients = ["andrewdurev506@gmail.com"]  # Замени на свою почту для тестирования
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Подтверждение почты</title>
    </head>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px;">
            <h1 style="color: #333; text-align: center;">🎬 Film Base API</h1>
            <h2 style="color: #666;">Подтверждение почты</h2>
            <p>Здравствуйте!</p>
            <p>Это тестовое письмо для проверки настройки почты в Film Base API.</p>
            <p>Если вы получили это письмо, значит почта настроена правильно! ✅</p>
            
            <div style="background-color: #e9ecef; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3>Что дальше?</h3>
                <ul>
                    <li>Настройте реальную почту в <code>config.py</code></li>
                    <li>Протестируйте регистрацию пользователей</li>
                    <li>Проверьте подтверждение почты</li>
                </ul>
            </div>
            
            <p style="color: #666; font-size: 12px; text-align: center;">
                Это автоматическое письмо от Film Base API
            </p>
        </div>
    </body>
    </html>
    """
    
    try:
        result = await send_email(subject, recipients, html_content)
        if result:
            print("✅ Тест почты завершен успешно!")
            print(f"📧 Письмо отправлено на: {recipients}")
        else:
            print("❌ Ошибка при отправке почты")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


async def test_verification_email():
    """Тестирует письмо подтверждения регистрации"""
    print("\n🔐 Тестирование письма подтверждения регистрации...")
    
    subject = "Подтвердите регистрацию в Film Base API"
    recipients = ["newuser@example.com"]  # Замени на свою почту
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Подтверждение регистрации</title>
    </head>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px;">
            <h1 style="color: #333; text-align: center;">🎬 Film Base API</h1>
            <h2 style="color: #28a745;">Добро пожаловать!</h2>
            <p>Здравствуйте!</p>
            <p>Вы зарегистрировались в Film Base API. Для завершения регистрации подтвердите вашу почту.</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="http://localhost:3000/verify-email?token=VERIFICATION_TOKEN" 
                   style="background-color: #007bff; color: white; padding: 15px 30px; 
                          text-decoration: none; border-radius: 5px; display: inline-block;">
                    Подтвердить почту
                </a>
            </div>
            
            <p style="color: #666;">
                Если кнопка не работает, скопируйте эту ссылку в браузер:<br>
                <code>http://localhost:3000/verify-email?token=VERIFICATION_TOKEN</code>
            </p>
            
            <p style="color: #666; font-size: 12px;">
                Если вы не регистрировались в Film Base API, проигнорируйте это письмо.
            </p>
        </div>
    </body>
    </html>
    """
    
    try:
        result = await send_email(subject, recipients, html_content)
        if result:
            print("✅ Тест письма подтверждения завершен!")
        else:
            print("❌ Ошибка при отправке письма подтверждения")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


async def test_password_reset_email():
    """Тестирует письмо сброса пароля"""
    print("\n🔑 Тестирование письма сброса пароля...")
    
    subject = "Сброс пароля - Film Base API"
    recipients = ["user@example.com"]  # Замени на свою почту
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Сброс пароля</title>
    </head>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px;">
            <h1 style="color: #333; text-align: center;">🎬 Film Base API</h1>
            <h2 style="color: #dc3545;">Сброс пароля</h2>
            <p>Здравствуйте!</p>
            <p>Вы запросили сброс пароля для вашего аккаунта в Film Base API.</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="http://localhost:3000/reset-password?token=RESET_TOKEN" 
                   style="background-color: #dc3545; color: white; padding: 15px 30px; 
                          text-decoration: none; border-radius: 5px; display: inline-block;">
                    Сбросить пароль
                </a>
            </div>
            
            <p style="color: #666;">
                Если кнопка не работает, скопируйте эту ссылку в браузер:<br>
                <code>http://localhost:3000/reset-password?token=RESET_TOKEN</code>
            </p>
            
            <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p style="color: #856404; margin: 0;">
                    ⚠️ <strong>Важно:</strong> Эта ссылка действительна в течение 1 часа.
                </p>
            </div>
            
            <p style="color: #666; font-size: 12px;">
                Если вы не запрашивали сброс пароля, проигнорируйте это письмо.
            </p>
        </div>
    </body>
    </html>
    """
    
    try:
        result = await send_email(subject, recipients, html_content)
        if result:
            print("✅ Тест письма сброса пароля завершен!")
        else:
            print("❌ Ошибка при отправке письма сброса пароля")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


async def main():
    """Главная функция тестирования"""
    print("🚀 Запуск тестов почты для Film Base API")
    print("=" * 50)
    
    # Проверяем конфигурацию
    try:
        from config import MAIL_CONFIG
        print(f"📧 Настроенная почта: {MAIL_CONFIG['MAIL_USERNAME']}")
        print(f"🖥️ SMTP сервер: {MAIL_CONFIG['MAIL_SERVER']}:{MAIL_CONFIG['MAIL_PORT']}")
        
        if MAIL_CONFIG['MAIL_USERNAME'] == "your_email@gmail.com":
            print("⚠️ Внимание: Используются тестовые настройки почты!")
            print("📝 Обновите config.py с реальными данными для отправки писем")
    except ImportError:
        print("❌ Не удалось импортировать конфигурацию почты")
        return
    
    print("\n" + "=" * 50)
    
    # Запускаем тесты
    await test_email()
    await test_verification_email()
    await test_password_reset_email()
    
    print("\n" + "=" * 50)
    print("🎉 Тестирование завершено!")
    print("\n📋 Следующие шаги:")
    print("1. Обновите config.py с реальными данными почты")
    print("2. Протестируйте регистрацию через API")
    print("3. Проверьте получение писем")


if __name__ == "__main__":
    asyncio.run(main())
