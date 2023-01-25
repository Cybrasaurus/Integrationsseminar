def read_py_and_return_part(path_filename_extension: str, function_name: str):
    """
    This function can read most files (used to read python source code in this use case. From the entire python file it
    slices the relevant python functions, given the function name. This requires the function to be ended with a comment:
    "# end function_name"
    :param path_filename_extension: Path to the file to be read, relative from the current working directory, with file extension
    :param function_name: the name of the function to be sliced
    :return:
    """
    with open(path_filename_extension, "r") as read_file:
        text_content = read_file.read()

    left_slice = text_content.find(function_name)
    right_slice = text_content.rfind(f"# end {function_name}")

    # todo check for filenotfound error
    return text_content[left_slice:right_slice]


def directory_checker_and_creator(directorypath:str):
    """
    This function checks whether a given directory exists within the project, if not it creates said directory and
    returns false. If it already exists it returns true
    :param directorypath: the path to the directory, relative from the current working directory
    :return: True or False: If Directory exists -> True, else False
    """
    import os
    cwd = os.getcwd()
    goal_wd = directorypath
    full_path = f"{cwd}{goal_wd}"

    if os.path.exists(full_path) is False:
        os.mkdir(full_path)
        return False
    else:
        return True

if __name__ == "__main__":
    print(read_py_and_return_part("chapter_1.py", "chapter_1_2_create_db()"))


