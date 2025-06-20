import sys
from pathlib import Path


def main():
    """
    Remove hard-coded overrides that force the collection to 'Basophile'
    (and related variables) so that environment variables supplied at
    runtime take precedence.
    """
    cfg_path = Path("/opt/publish/src/configs/basic.py")
    if not cfg_path.exists():
        sys.stderr.write(
            "patch_basic_env_override.py: basic.py not found at expected path\n"
        )
        sys.exit(1)

    original_lines = cfg_path.read_text().splitlines(keepends=True)
    patched_lines = []
    skip_block = False

    for line in original_lines:
        stripped = line.strip()

        # Start of the override block we want to remove
        if stripped.startswith("# For jpl-labcas"):
            skip_block = True
            continue

        # If we're inside the override block, skip lines that set the variables
        if skip_block:
            if stripped == "" or stripped.startswith("#"):
                # End the skip when we hit a blank line or another comment
                skip_block = False
            # Always skip the variable assignment lines inside this block
            continue

        # Additionally guard against any stray hard-coded overrides
        if ("'Basophile'" in stripped and stripped.startswith("collection")) \
           or stripped.startswith("collection_subset = None") \
           or stripped.startswith("publish_id = None") \
           or stripped.startswith("steps = ["):
            continue

        patched_lines.append(line)

    cfg_path.write_text("".join(patched_lines))
    print("patch_basic_env_override.py: removed hard-coded Basophile overrides from basic.py")


if __name__ == "__main__":
    main()