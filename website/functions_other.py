import json


def read_py_and_return_part(path_filename_extension: str, function_name: str, json_mode: bool = False):
    """
    This function can read most files (used to read python source code in this use case. From the entire python file it
    slices the relevant python functions, given the function name. This requires the function to be ended with a comment:
    "# end function_name"
    :param json_mode: Deafult False. If this is set to true the function_name parameter does nothing, instead it reads the entier file
    :param path_filename_extension: Path to the file to be read, relative from the current working directory, with file extension
    :param function_name: the name of the function to be sliced
    :return:
    """


    if json_mode is False:
        with open(path_filename_extension, "r") as read_file:
            text_content = read_file.read()
        left_slice = text_content.find(function_name)
        right_slice = text_content.rfind(f"# end {function_name}")
        return text_content[left_slice:right_slice]

    # todo check for filenotfound error
    else:
        with open(path_filename_extension, "r", encoding="utf-8") as read_file:
            text_content = json.load(read_file)
            #todo result is not formatted nicely

            text_content = json.dumps(text_content, indent=4, ensure_ascii=False)
        return text_content


def directory_checker_and_creator(directorypath: str):
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


def json_to_list(input_dict):
    return_list = []
    for items in input_dict:
        return_list.append(str(input_dict[items]))
    return return_list


if __name__ == "__main__":
    mydict = {
          "Vorname": "Margot",
          "Nachname": "Meyer",
          "Name": "Margot Meyer"
        }
