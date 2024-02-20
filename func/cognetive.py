import radon.complexity as radon_complexity
import os


# Функция для подсчета когнитивной сложности проекта
def calculate_cognitive_complexity(project_path):
    total_complexity = 0
    lines_code = 0
    current_file = os.path.basename(__file__)

    # Рекурсивно обходит все файлы и директории в проекте
    for root, dirs, files in os.walk(project_path):
        for file in files:
            # if 'venv' in dirs:
            #     dirs.remove('venv')
            if 'main.py' in files:
                files.remove('main.py')
            if current_file in files:
                files.remove(current_file)
            if file.endswith(".py"):  # Проверка на расширение .py
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines_code += len(content.split('\n'))
                result = radon_complexity.cc_visit(
                    content)  # Получение когнитивной сложности файла
                for item in result:
                    total_complexity += item.complexity

    return total_complexity, lines_code


# Пример использования: подсчет когнитивной сложности проекта
project_path = "."  # Укажите путь к корневой директории вашего проекта
complexity, lines_code = calculate_cognitive_complexity(project_path)
print(
    f"Когнитивная сложность проекта: {complexity}\nКол-во строчек кода: {lines_code}")
