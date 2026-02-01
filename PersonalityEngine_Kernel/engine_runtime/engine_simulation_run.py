import json
import os
from PersonalityEngine_Kernel.engines.inference.inference_engine import run_inference

def load_simulation_template():
    template_path = os.path.join(
        os.path.dirname(__file__), 
        "..",
        "modules",
        "interpretation",
        "engine_simulation_run.json"
    )

    template_path = os.path.abspath(template_path)

    print("Loading simulation template from:", template_path)

    with open(template_path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_simulation():
    print("\n--- PERSONALITY ENGINE SIMULATION RUN ---\n")

    template = load_simulation_template()

    raw_input = template.get("raw_input", {})
    print("Raw Input:")
    print(json.dumps(raw_input, indent=4))
    print("\n----------------------------------------\n")

    expected_output = template.get("expected_output_skeleton", {})
    print("Expected Output Skeleton:")
    print(json.dumps(expected_output, indent=4))
    print("\n----------------------------------------\n")

    print("\nRunning Inference Engine...\n")
    result = run_inference(template.get("raw_input", {}))

    print("Inference Output:")
    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    run_simulation()
