# Функция для выполнения тестов задач на курсе https://stepik.org/course/82541/ - "Поколение Python": курс для профессионалов
# Предварительно необходимо получить личный токен на github для подключения к репозиторию Beegeek
# Для получение токена нужно иметь учетную запись Github, переходим в Settings,
# слева последняя строка Developer settings -> Personal access tokens -> Fine-grained tokens
# Подробнее - https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
# Функции на вход подается 3 параметра ваш токен, номер модуля и номер задачи, 

from github import Github
import re
import sys
import io
import contextlib

# параметры на вход
github_token = "твой токен"
# пример для второго модуля, задача 13 - https://stepik.org/lesson/569748/step/13
module = 2
task = 13

def check_bg(github_token, module, task):
  
  # Подключение к GitHub с использованием токена
  g = Github(github_token)

  # Получение репозитория
  repo = g.get_repo("python-generation/Professional")

  # Путь в репозитории к файлам
  path = f'Module_{int(module)}/Module_{module}/Module_{module}.{task}/'

  # Чтение файла input
  file_path_input = f'{path}input.txt'
  input_contents = repo.get_contents(file_path_input).decoded_content.decode('utf-8')

  # Чтение файла output
  file_path_output = f'{path}output.txt'
  output_contents = repo.get_contents(file_path_output).decoded_content.decode('utf-8')

  # Парсинг кода между блоками TEST_N:
  pattern = r'# TEST_\d+:(.*?)\n(?=# TEST_|$|\Z)'
  input_matches = re.findall(pattern, input_contents, re.DOTALL)
  output_matches = re.findall(pattern, output_contents, re.DOTALL)

  # Список для хранения флагов успешности выполнения тестов
  test_results = []

  for i, (input_match, output_match) in enumerate(zip(input_matches, output_matches), 1):
      print(f"Результат теста {i}:")
      try:
          # Перенаправляем стандартный вывод в объект StringIO
          output = io.StringIO()

          # Исполнение строки как кода и сохранение вывода в переменную
          with contextlib.redirect_stdout(output):
            exec(input_match)

          # Получение содержимого объекта StringIO в виде строки
          output_string = output.getvalue().strip()
          print("Ожидаемый результат:  ", output_match.strip())
          print("Фактический результат:", output_string, end='\n\n')

          # Сравниваем результаты
          test_results.append(output_string == output_match.strip())
      except Exception as e:
          print("Ошибка при выполнении теста:", e)
          test_results.append(False)

  print("Результаты тестов:", ['Не успешно', 'Успешно'][all(test_results)])


# Пример запуска
# 1. Сначала решаем поставленную задачу, создаем и записываем функцию. 
# ВНИМАНИЕ! Код будет исполняться корректно, только если все условия по наименованию функции будет исполняться
def spell(*args):
    result = {}
    for word in args:
        if result.get(word[0].lower(), 0) < len(word):
            result[word[0].lower()] = len(word)
    return result
# 2. Вызываем функцию для проверки решения. 
check_bg(github_token, module, task)
# Можем далее использовать конструкцию вида ниже, остается создать функцию из задания 14 строкой выше
check_bg(github_token, module, task=14)
