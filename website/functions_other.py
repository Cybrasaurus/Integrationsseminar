def read_py_and_return_part(path_filename_extension, function_name):
    with open(path_filename_extension, "r") as read_file:
        text_content = read_file.read()

    left_slice = text_content.find(function_name)
    right_slice = text_content.rfind(f"# end {function_name}")

    return text_content[left_slice:right_slice]


if __name__ == "__main__":
    print(read_py_and_return_part("chapter_1.py", "chapter_1_2_create_db()"))


