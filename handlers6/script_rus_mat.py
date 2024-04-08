# скрипт, который переводит тхт в множество и сохраняет в файл restricted_words.py
# Дублирует слова с подменными английскими буквами
# (запускается отдельно от всего бота, на входе список стоп-слов rus_mat.txt)
import os


def read_file_to_set(filename):
    mat_set = set()
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                word = line.strip().lower()
                mat_set.add(word)
                if 'а' in word:
                    mat_set.add(word.replace('а', 'a'))
                if 'у' in word:
                    mat_set.add(word.replace('у', 'y'))
                if 'к' in word:
                    mat_set.add(word.replace('к', 'k'))
                if 'з' in word:
                    mat_set.add(word.replace('з', '3'))
                if 'х' in word:
                    mat_set.add(word.replace('х', 'x'))
                if 'р' in word:
                    mat_set.add(word.replace('р', 'p'))
                if 'о' in word:
                    mat_set.add(word.replace('о', 'o'))
                if 'с' in word:
                    mat_set.add(word.replace('с', 'c'))
                if 'а' in word:
                    mat_set.add(word.replace('а', 'a'))
                if 'у' in word:
                    mat_set.add(word.replace('у', 'y'))
                if 'к' in word:
                    mat_set.add(word.replace('к', 'k'))
                if 'з' in word:
                    mat_set.add(word.replace('з', '3'))
                if 'х' in word:
                    mat_set.add(word.replace('х', 'x'))
                if 'р' in word:
                    mat_set.add(word.replace('р', 'p'))
                if 'о' in word:
                    mat_set.add(word.replace('о', 'o'))
                if 'о' in word:
                    mat_set.add(word.replace('о', '0'))
                if 'е' in word:
                    mat_set.add(word.replace('е', 'e'))
                if 'а' in word:
                    mat_set.add(word.replace('а', 'a'))
                if 'у' in word:
                    mat_set.add(word.replace('у', 'y'))
                if 'к' in word:
                    mat_set.add(word.replace('к', 'k'))
                if 'з' in word:
                    mat_set.add(word.replace('з', '3'))
                if 'ч' in word:
                    mat_set.add(word.replace('ч', '4'))
                if 'х' in word:
                    mat_set.add(word.replace('х', 'x'))
                if 'р' in word:
                    mat_set.add(word.replace('р', 'p'))
                if 'о' in word:
                    mat_set.add(word.replace('о', 'o'))
                if 'ё' in word:
                    mat_set.add(word.replace('ё', 'е'))
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
output_filename = os.path.join(os.path.dirname(__file__), 'restricted_words.py')

lines_set = read_file_to_set(filename)

save_set_to_file(lines_set, output_filename)
