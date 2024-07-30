import os
import subprocess
from datetime import datetime

from config import DB_HOST, DB_PORT, DB_USER, DB_NAME, BACKUP_DIR, DB_PASS


def backup_database():
    # Убедитесь, что каталог для резервных копий существует
    os.makedirs(BACKUP_DIR, exist_ok=True)

    # Создание имени файла для резервной копии
    backup_file = os.path.join(BACKUP_DIR, f'backup_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}.sql')

    # Команда для создания резервной копии
    dump_cmd = [
        'pg_dump',
        '-h', DB_HOST,
        '-p', DB_PORT,
        '-U', DB_USER,
        '-d', DB_NAME,
        '-F', 'c',
        '-b',
        '-v',
        '-f', backup_file
    ]

    # Установка пароля для PostgreSQL
    env = os.environ.copy()
    env['PGPASSWORD'] = DB_PASS

    # Выполнение команды
    result = subprocess.run(dump_cmd, env=env, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Ошибка при создании резервной копии: {result.stderr}")
    else:
        print(f"Резервная копия успешно создана: {backup_file}")