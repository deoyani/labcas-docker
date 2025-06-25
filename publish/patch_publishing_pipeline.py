import os
import copy

def patch_publishing_pipeline():
    import pathlib
    import sys

    # Read the original publishing_pipeline.py
    pipeline_path = "/opt/publish/publishing_pipeline.py"
    with open(pipeline_path, "r") as f:
        lines = f.readlines()

    # Find the line with compare_with_solr call
    target_line = None
    for i, line in enumerate(lines):
        if "compare_with_solr(os.path.join(metadata_dir, collection), publish_id, collection, copy.deepcopy(metadata_walker))" in line:
            target_line = i
            break

    if target_line is None:
        print("Could not find compare_with_solr call in publishing_pipeline.py")
        sys.exit(1)

    # Insert debug print statements before the target line with correct indentation
    debug_lines = [
        '        print(f"DEBUG: metadata_dir={metadata_dir}")\n',
        '        print(f"DEBUG: collection={collection}")\n',
        '        print(f"DEBUG: publish_id={publish_id}")\n',
    ]

    lines = lines[:target_line] + debug_lines + lines[target_line:]

    # Write back the modified file
    with open(pipeline_path, "w") as f:
        f.writelines(lines)

if __name__ == "__main__":
    patch_publishing_pipeline()