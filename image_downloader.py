import os
import requests
import hashlib
from urllib.parse import urlparse
from pathlib import Path
from PIL import Image
import io

# Базовый путь для сохранения изображений
BASE_PATH = "F:\\data_base_images"

class ImageDownloader:
    """Класс для скачивания и сохранения изображений в формате AVIF"""
    
    def __init__(self, base_path=BASE_PATH):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        
        # Создаем папки для разных типов изображений
        (self.base_path / "films").mkdir(exist_ok=True)
        (self.base_path / "actors").mkdir(exist_ok=True)
        (self.base_path / "temp").mkdir(exist_ok=True)
        
        # Настройки оптимизации AVIF
        self.avif_quality = 80  # Качество AVIF (0-100)
    
    def _optimize_image_to_avif(self, image_data):
        try:
            # Открываем изображение
            image = Image.open(io.BytesIO(image_data))
            
            # Конвертируем в RGB если нужно
            if image.mode in ('RGBA', 'LA', 'P'):
                # Создаем белый фон для прозрачных изображений
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Конвертируем в AVIF
            avif_buffer = io.BytesIO()
            image.save(avif_buffer, format='AVIF', quality=self.avif_quality, method=6)
            
            return avif_buffer.getvalue()
            
        except Exception as e:
            print(f"❌ Ошибка оптимизации изображения: {e}")
            return None

    def download_image(self, url, image_type, filename=None):
        """
        Скачивает изображение, оптимизирует и сохраняет в формате AVIF
        
        Args:
            url (str): URL изображения
            image_type (str): Тип изображения ('films' или 'actors')
            filename (str, optional): Имя файла. Если не указано, генерируется автоматически
        
        Returns:
            str: Путь к сохраненному файлу или None при ошибке
        """
        if not url or url.startswith('https://yastatic.net'):
            # Пропускаем placeholder изображения
            return None
            
        try:
            # Нормализуем URL
            if url.startswith('//'):
                url = 'https:' + url
            elif not url.startswith('http'):
                url = 'https://' + url
            
            # Генерируем имя файла если не указано
            if not filename:
                # Генерируем уникальное имя на основе URL
                url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
                filename = f"{url_hash}.avif"
            
            # Определяем путь для сохранения
            save_path = self.base_path / image_type / filename
            
            # Скачиваем изображение
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Оптимизируем и конвертируем в AVIF
            avif_data = self._optimize_image_to_avif(response.content)
            if not avif_data:
                return None
            
            # Сохраняем оптимизированный файл
            with open(save_path, 'wb') as f:
                f.write(avif_data)
            
            # Возвращаем относительный путь
            return f"{BASE_PATH}/{image_type}/{filename}"
            
        except Exception as e:
            print(f"❌ Ошибка скачивания изображения {url}: {e}")
            return None
    
    def download_film_poster(self, url, film_id):
        """Скачивает постер фильма в формате AVIF"""
        if not url:
            return None
        
        # Генерируем имя файла на основе ID фильма
        filename = f"film_{film_id}.avif"
        return self.download_image(url, "films", filename)
    
    def download_actor_photo(self, url, actor_id):
        """Скачивает фото актера в формате AVIF"""
        if not url:
            return None
        
        # Генерируем имя файла на основе ID актера
        filename = f"actor_{actor_id}.avif"
        return self.download_image(url, "actors", filename)
    
    def cleanup_temp_files(self):
        """Очищает временные файлы"""
        temp_dir = self.base_path / "temp"
        if temp_dir.exists():
            for file in temp_dir.iterdir():
                if file.is_file():
                    file.unlink()
    
    def get_image_info(self, image_path):
        """Получает информацию о сохраненном изображении"""
        if not image_path or not os.path.exists(image_path):
            return None
        
        file_size = os.path.getsize(image_path)
        return {
            'path': image_path,
            'size_bytes': file_size,
            'size_mb': round(file_size / (1024 * 1024), 2),
            'format': 'AVIF',
            'exists': True
        }