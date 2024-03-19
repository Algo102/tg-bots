# скрипт который переводит тхт в множество и сохраняет в файл rus_mat.py
# (запускается отдельно от всего бота, на входе список стоп-слов rus_mat.txt)
import os


def read_file_to_set(filename):
    mat_set = set()
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                mat_set.add(line.strip().lower())
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла '{filename}': {e}")
    return mat_set


def save_set_to_file(mat_set, output_filename):
    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write("rus_mat = {\n")
            for line in sorted(mat_set):
                file.write(f"    '{line}',\n")
            file.write("}\n")
        print(f"Отсортированное множество строк сохранено в файл '{output_filename}'")
    except Exception as e:
        print(f"Произошла ошибка при сохранении файла '{output_filename}': {e}")


filename = os.path.join(os.path.dirname(__file__), 'rus_mat.txt')
output_filename = os.path.join(os.path.dirname(__file__), 'rus_mat.py')

lines_set = read_file_to_set(filename)

save_set_to_file(lines_set, output_filename)
