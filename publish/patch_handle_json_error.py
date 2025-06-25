import os
import copy
import json

def patch_handle_json_error():
    import pathlib
    import sys

    pipeline_path = "/opt/publish/publishing_pipeline.py"
    try:
        with open(pipeline_path, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"File {pipeline_path} not found.")
        sys.exit(1)

    target_line = None
    for i, line in enumerate(lines):
        if "compare_with_solr(os.path.join(metadata_dir, collection), publish_id, collection, copy.deepcopy(metadata_walker))" in line:
            target_line = i
            break

    if target_line is None:
        print("Could not find compare_with_solr call in publishing_pipeline.py")
        sys.exit(1)

    indent = lines[target_line][:len(lines[target_line]) - len(lines[target_line].lstrip())]

    # Insert import json at the top if not present
    import_line = "import json\n"
    if import_line not in lines:
        # Find the last import statement line
        last_import_index = 0
        for idx, line in enumerate(lines):
            if line.startswith("import ") or line.startswith("from "):
                last_import_index = idx
        lines.insert(last_import_index + 1, import_line)

    # Wrap the call in try-except block
    new_lines = []
    new_lines.append(f"{indent}try:\n")
    new_lines.append(f"{indent}    {lines[target_line].strip()}\n")
    new_lines.append(f"{indent}except json.JSONDecodeError as e:\n")
    new_lines.append(f"{indent}    print(f\"JSONDecodeError caught: {{e}}. Continuing without exiting.\")\n")

    lines = lines[:target_line] + new_lines + lines[target_line+1:]

    with open(pipeline_path, "w") as f:
        f.writelines(lines)

if __name__ == "__main__":
    patch_handle_json_error()