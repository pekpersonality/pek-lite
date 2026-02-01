import os
import json

# ================================
#  ENGINE LOADER v1.0
#  Loads Kernel → Resolves Modules → Prepares Runtime
# ================================

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
KERNEL_ROOT = os.path.join(BASE_PATH, "..")

# -------------------------
# Helper: Safe JSON Loader
# -------------------------
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# -------------------------
# Step 1: Load Kernel Files
# -------------------------
def load_kernel():
    kernel = {}
    kernel_files = [
        "kernel_access_layer.json",
        "kernel_linkage.json",
        "kernel_structural_v1.json",
        "runtime_harness.json",
        "test_input_engine.json"
    ]

    for file in kernel_files:
        full_path = os.path.join(KERNEL_ROOT, file)
        if os.path.exists(full_path):
            kernel[file.replace(".json", "")] = load_json(full_path)

    return kernel

# ---------------------------------------------
# Step 2: Recursively Load All Module JSON Files
# ---------------------------------------------
def load_modules():
    modules_path = os.path.join(KERNEL_ROOT, "modules")
    module_tree = {}

    for root, dirs, files in os.walk(modules_path):
        for file in files:
            if file.endswith(".json"):
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, modules_path)

                # Create nested dictionary structure based on folders
                pointer = module_tree
                parts = relative_path.split(os.sep)

                for part in parts[:-1]:
                    pointer = pointer.setdefault(part, {})

                pointer[parts[-1].replace(".json", "")] = load_json(full_path)

    return module_tree

# -------------------------------------
# Step 3: Attach Modules to Kernel Root
# -------------------------------------
def assemble_engine():
    print("Loading kernel...")
    kernel = load_kernel()

    print("Loading modules...")
    modules = load_modules()

    engine = {
        "kernel": kernel,
        "modules": modules
    }

    print("Engine structure assembled successfully.")
    return engine

# -------------------------------------
# Step 4: Runtime Entry Point
# -------------------------------------
def initialize_engine():
    engine = assemble_engine()
    print("\nPERSONALITY ENGINE INITIALIZED.")
    print("--------------------------------")

    # Show high-level structure count
    print("Kernel components loaded:", len(engine["kernel"]))
    print("Module categories loaded:", len(engine["modules"]))

    return engine


# -------------------------
# Standalone Run
# -------------------------
if __name__ == "__main__":
    engine = initialize_engine()
    print("\nReady for test input or live processing.")
