"""Queue animal_story_1min.json via ComfyUI API (optional helper)."""

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

HOST = "127.0.0.1:8188"
WORKFLOW = Path(__file__).parent / "user" / "default" / "workflows" / "animal_story_1min.json"


def workflow_to_prompt(wf: dict) -> dict:
    prompt = {}
    for node in wf["nodes"]:
        inputs = {}
        for inp in node.get("inputs", []):
            if inp.get("link") is not None:
                for link in wf["links"]:
                    if link[0] == inp["link"]:
                        inputs[inp["name"]] = [str(link[1]), link[2]]
                        break
        if "widgets_values" in node:
            wv = node["widgets_values"]
            if node["type"] == "CheckpointLoaderSimple":
                inputs["ckpt_name"] = wv[0]
            elif node["type"] == "EmptyLatentImage":
                inputs["width"], inputs["height"], inputs["batch_size"] = wv[0], wv[1], wv[2]
            elif node["type"] == "CLIPTextEncode":
                inputs["text"] = wv[0]
            elif node["type"] == "KSampler":
                inputs.update({
                    "seed": wv[0], "control_after_generate": wv[1], "steps": wv[2],
                    "cfg": wv[3], "sampler_name": wv[4], "scheduler": wv[5], "denoise": wv[6],
                })
            elif node["type"] == "ADE_AnimateDiffLoaderGen1":
                inputs["model_name"] = wv[0]
                inputs["beta_schedule"] = wv[1]
            elif node["type"] == "ADE_LoopedUniformContextOptions":
                inputs["context_length"] = wv[0]
                inputs["context_stride"] = wv[1]
                inputs["context_overlap"] = wv[2]
                inputs["closed_loop"] = wv[3]
            elif node["type"] == "VHS_MergeImages":
                inputs["merge_strategy"] = wv[0]
                inputs["scale_method"] = wv[1]
                inputs["crop"] = wv[2]
            elif node["type"] == "VHS_VideoCombine" and isinstance(wv, dict):
                inputs.update(wv)
        prompt[str(node["id"])] = {"class_type": node["type"], "inputs": inputs}
    return prompt


def main() -> int:
    if not WORKFLOW.exists():
        print(f"Missing {WORKFLOW}")
        return 1
    wf = json.loads(WORKFLOW.read_text(encoding="utf-8"))
    prompt = workflow_to_prompt(wf)
    body = json.dumps({"prompt": prompt}).encode("utf-8")
    req = urllib.request.Request(
        f"http://{HOST}/prompt",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        print(f"Queued job: {data.get('prompt_id', data)}")
        return 0
    except urllib.error.URLError as e:
        print(f"ComfyUI not reachable at http://{HOST} — start run_comfyui.bat first.")
        print(e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
