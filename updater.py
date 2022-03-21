import json
import requests
import os

print("NOTICE: THE WHOLE PROCESS MAY TAKE LONG")

path = os.path.split(os.path.realpath(__file__))[0] # Path to the current directory
files_not_to_update = ("main/settings.json", "main/info.txt", "main/debug.txt", "main/data.json")

version = requests.get("https://raw.githubusercontent.com/Ayza69420/Pygame-editor/main/version.txt").text.strip() # Repo version

repo_files = requests.get("https://api.github.com/repos/Ayza69420/Pygame-editor/git/trees/main?recursive=1").json()

def update():
    for repo_file in repo_files["tree"]:
        if repo_file["mode"] == "100644" and os.path.splitext(path+"/"+repo_file["path"])[1] in (".py", ".txt", ".json"):
            file_path = path+"/"+repo_file["path"]
            content = requests.get(f"https://raw.githubusercontent.com/Ayza69420/Pygame-editor/main/{repo_file['path']}").text

            # Updating
            if os.path.exists(file_path) and repo_file["path"] not in files_not_to_update:
                with open(file_path, "r") as fr:
                    if [i for i in content if not i.isspace()] != [i for i in fr.read() if not i.isspace()]:
                        print(f"Updating {repo_file['path']}..")

                        with open(file_path, "w") as fw:
                            fw.write(content)

            # Adding
            elif not os.path.exists(file_path):
                print(f"Adding {repo_file['path']}..")
                with open(file_path, "x") as f:
                    with open(file_path, "w") as f:
                        f.write(content) 
            
            # Updating settings
            elif repo_file["path"] == "main/settings.json":
                with open(file_path, "r") as f:
                    user_settings = json.loads(f.read())

                    if len(user_settings) != len(json.loads(content)):
                       print("Updating main/settings.json..")

                       for i in json.loads(content):
                           if i not in user_settings:
                               user_settings[i] = json.loads(content)[i]

                       with open(file_path, "w") as fw:
                           fw.write(json.dumps(user_settings))

    with open(path+"version.txt", "w") as ver:
        ver.write(version)

        input("Finished updating.")

with open(path+"/version.txt", "r") as ver:
    if ver.read().strip() == version:
        input("No available updates.")
    else:
        print("An update was found.")

        while True:
            answer = input("Proceed on updating (y/n)? ").lower()
            
            if answer in ("y", "n"):
                if answer == "y":
                    update()
                    break
                quit() # no else statement required here, if the answer wasn't y (because it would break the while loop), then it's n
            else:
                print("Your answer (%s) is not valid. Please enter either (Y/y = Yes) or (N/n = No)" % answer)
                continue
