import json
import os 
# Path to the launch.json file

os.chdir(os.path.dirname(os.getcwd()))
launch_json_path = "D:\j_Documents\cliimbing\climbtracker\.vscode\launch.json"
# rel_path =os.path.join(os.getcwd(), "climbtracker", ".vscode")
rel_path =os.path.join("climbtracker", ".vscode", "launch.json")

# launch_json_path = rel_path
# Read the launch.json file

print(launch_json_path)
with open(launch_json_path, "r") as file:
    launch_json = json.load(file)

# Extract the value of ${workspaceFolder}
workspace_folder = launch_json["configurations"][0]["cwd"]

# Print the value of ${workspaceFolder}
print(workspace_folder)

    # JSON comments
    # // Use IntelliSense to learn about possible attributes.
    # // Hover to view descriptions of existing attributes.
    # // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    # // NOTE: need to remove comments if you want to load json file with json.load
    # //https://stackoverflow.com/questions/53653083/how-to-correctly-set-pythonpath-for-visual-studio-code
    # // https://stackoverflow.com/questions/63654651/how-to-set-the-import-path-for-the-the-python-interactive-window-in-vs-code
    # // trailing commas not allowed in json!
    # // https://jsonlint.com/ godsend