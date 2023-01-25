
import os
if os.path.exists("/website/sql_handling/databases") is False:
    cwd = os.getcwd()
    print(cwd)

    goal_wd = "\\website\\sql_handling\\databases"
    full_path = f"{cwd}{goal_wd}"
    print(full_path)
    os.mkdir(full_path)
