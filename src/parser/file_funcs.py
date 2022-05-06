def file_reader(filename: str):
    with open(filename, 'r') as file:
        line = file.readline()
        while line:
            yield line
            line = file.readline()


def list_writer(list_to_write: list, filename: str):
    with open(filename, 'w', encoding='utf8') as file:
        for key, value in list_to_write:
            file.write(f'{key} {value}\n')


def word_counter(words_list: list, word: str) -> int:
    result = 0
    for line in words_list:
        if not line:
            continue
        curr_word = line.split()[0]
        if curr_word == word:
            result += 1
    return result


def files_merge(*filenames: str, result_path: str):
    """
    sad
    :param filenames:
    :param result_path:
    :return:
    """
    with open(result_path, 'w') as result_file:
        file_readers = [file_reader(filename) for filename in filenames]
        lines = [next(reader, None) for reader in file_readers]
        while any(lines):
            non_none_words = [word for word in lines if word]
            min_word_line = min(non_none_words, key=lambda line: line.split()[0])
            min_word = min_word_line.split()[0]
            # if word is met multiple times
            if word_counter(lines, min_word) > 1:
                next_indexes = []
                result_word_count = 0
                for line_index in range(len(lines)):
                    read_line = lines[line_index]
                    if not read_line:
                        continue
                    word, num = read_line.split()
                    if word == min_word:
                        result_word_count += int(num)
                        next_indexes.append(line_index)
                result_file.write(f'{min_word} {str(result_word_count)}\n')
                for next_index in next_indexes:
                    lines[next_index] = next(file_readers[next_index], None)
            # if word is met only once
            else:
                result_file.write(f'{min_word_line}')
                next_index = lines.index(min_word_line)
                lines[next_index] = next(file_readers[next_index], None)


if __name__ == "__main__":
    pass
