# 🌐 Быстрый старт: Публичный доступ к нейросети

Это краткое руководство покажет, как за несколько минут сделать вашу нейросеть доступной с любого устройства.

## 🚀 Метод 1: Gradio Share (Самый быстрый)

### Linux/Mac

```bash
./launch_public.sh
```

### Windows

Дважды кликните на файл `launch_public.bat` или в командной строке:

```cmd
launch_public.bat
```

### Что произойдет?

1. Скрипт запустит веб-интерфейс с включенной публичной ссылкой
2. Через несколько секунд в консоли появится ссылка вида: `https://xxxxx.gradio.live`
3. Эта ссылка будет действительна **72 часа**
4. Поделитесь ссылкой с кем угодно - они смогут использовать нейросеть!

### Пример вывода:

```
🔥 Starting Fire Detection with Public Sharing
==============================================

⚠️  Public URL will be valid for 72 hours
🌐 A shareable link will be generated...

Running on local URL:  http://127.0.0.1:7860
Running on public URL: https://abc123def.gradio.live  ← Поделитесь этой ссылкой!

This share link expires in 72 hours.
```

## 🔒 С паролем (опционально)

### Linux/Mac

```bash
export GRADIO_AUTH=username:password
./launch_public.sh
```

### Windows

```cmd
set GRADIO_AUTH=username:password
launch_public.bat
```

Теперь для доступа потребуется ввести логин и пароль!

## 📝 Ручной запуск

Если скрипты не работают, запустите напрямую:

```bash
# Включить публичный доступ
export GRADIO_SHARE=True  # Linux/Mac
set GRADIO_SHARE=True     # Windows

# С паролем (опционально)
export GRADIO_AUTH=admin:secretpassword

# Запустить
python launch_ui.py
```

## ⏰ Постоянный хостинг

Если нужен постоянный доступ (не 72 часа), смотрите:

📖 **[DEPLOYMENT.md](DEPLOYMENT.md)** - Полное руководство по развертыванию на:
- Hugging Face Spaces (бесплатно, постоянно)
- Railway.app
- Render.com
- Docker
- AWS / Google Cloud

## ❓ FAQ

**Q: Ссылка не работает через 72 часа**
A: Запустите скрипт заново, получите новую ссылку. Для постоянного доступа используйте хостинг из DEPLOYMENT.md

**Q: Медленная работа**
A: Gradio Share использует удаленные серверы. Для лучшей производительности разверните на хостинге с GPU.

**Q: Безопасно ли это?**
A: Ссылка публичная, но случайная. Для дополнительной защиты используйте `GRADIO_AUTH`.

**Q: Можно ли использовать для production?**
A: Gradio Share - для тестирования. Для production используйте постоянный хостинг.

## 🎉 Готово!

Теперь ваша нейросеть доступна из любой точки мира! 🌍
