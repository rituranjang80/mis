"""Build animal_story_1min.json — segments x 48 frames, merged to one MP4."""

import argparse
import json
from pathlib import Path

OUT = Path(__file__).parent / "user" / "default" / "workflows" / "animal_story_1min.json"

STYLE_PREFIX = (
    "masterpiece, best quality, cinematic children's fable, detailed fur feathers and scales, "
    "peaceful storybook animation, soft magical lighting, consistent character design, "
)
STYLE_SUFFIX = ", vibrant african savanna, joyful mood, seamless animation, no text, no watermark"

ALL_CHAPTERS = [
    "Scene 1 - Dawn: a majestic lion and gentle elephant meet at a sparkling savanna watering hole, warm morning mist, wide cinematic shot",
    "Scene 2 - Friendship: lion and curious zebra talk under a giant acacia tree, afternoon golden light, friendly gestures",
    "Scene 3 - Playful: a cheerful monkey swings from branches toward lion and friends, dynamic motion, lush trees",
    "Scene 4 - Colorful: a bright parrot lands beside the group, spreading wings, tropical savanna edge",
    "Scene 5 - Tall Guest: a kind giraffe bends down to join the circle, all animals look up smiling, blue sky",
    "Scene 6 - Wisdom: a wise owl on a high branch speaks to listening animals below, soft dappled forest light",
    "Scene 7 - Patience: a slow turtle walks into the clearing, animals make space warmly, peaceful meadow",
    "Scene 8 - Storyteller: a friendly fox sits among lion elephant zebra monkey, animated storytelling pose",
    "Scene 9 - Gathering: all animals form a circle in a sunlit clearing, lion elephant zebra monkey parrot owl turtle fox giraffe together",
    "Scene 10 - Finale: epic sunset panorama, all animal friends celebrating together, golden hour, cinematic wide shot, heartwarming ending",
]

NEGATIVE = (
    "worst quality, low quality, bad anatomy, blurry, watermark, text, logo, ugly, deformed, "
    "violence, scary, aggressive animals, fighting, blood, nsfw, inconsistent style, flicker"
)

FRAMES = 48
FPS = 8
BASE_SEED = 420069001


class W:
    def __init__(self):
        self.nodes = []
        self.links = []
        self.link_id = 1
        self.nid = 1
        self.out_links = {}

    def node(self, **kw) -> int:
        kw["id"] = self.nid
        kw.setdefault("flags", {})
        kw.setdefault("mode", 0)
        self.nodes.append(kw)
        cur = self.nid
        self.nid += 1
        return cur

    def connect(self, src_id: int, src_slot: int, dst_id: int, dst_slot: int, typ: str):
        lid = self.link_id
        self.links.append([lid, src_id, src_slot, dst_id, dst_slot, typ])
        self.out_links.setdefault((src_id, src_slot), []).append(lid)
        dst = self.nodes[dst_id - 1]
        dst["inputs"][dst_slot]["link"] = lid
        self.link_id += 1

    def finalize_outputs(self):
        for n in self.nodes:
            for i, o in enumerate(n.get("outputs", [])):
                o["links"] = self.out_links.get((n["id"], i), []) or None
                if o["links"] == []:
                    o["links"] = None


def build(quick: bool) -> None:
    chapters = ALL_CHAPTERS[:2] if quick else ALL_CHAPTERS
    steps = 8 if quick else 12
    seg_total = len(chapters)
    total_frames = FRAMES * seg_total
    duration = total_frames / FPS
    out_prefix = "animal_story_quick_test" if quick else "animal_story_1min_final"
    group_title = (
        f"QUICK TEST: {seg_total} segments ({duration:.0f} sec) — CPU preview"
        if quick
        else "1-Min Animal Story: 10 segments auto-stitched → one perfect MP4"
    )

    w = W()

    ckpt = w.node(
        type="CheckpointLoaderSimple", pos=[-1100, 400], size=[315, 128], order=0,
        outputs=[
            {"name": "MODEL", "type": "MODEL"},
            {"name": "CLIP", "type": "CLIP"},
            {"name": "VAE", "type": "VAE"},
        ],
        properties={"Node name for S&R": "CheckpointLoaderSimple", "cnr_id": "comfy-core", "ver": "0.24.0"},
        widgets_values=["v1-5-pruned-emaonly.safetensors"],
    )

    ctx = w.node(
        type="ADE_LoopedUniformContextOptions", pos=[-760, 120], size=[315, 194], order=1,
        outputs=[{"name": "CONTEXT_OPTS", "type": "CONTEXT_OPTIONS"}],
        title="Context 16 frames per segment",
        properties={"Node name for S&R": "ADE_LoopedUniformContextOptions", "cnr_id": "comfyui-animatediff-evolved", "ver": "1.5.7"},
        widgets_values=[16, 1, 4, True],
    )

    ade = w.node(
        type="ADE_AnimateDiffLoaderGen1", pos=[-760, 360], size=[315, 328], order=2,
        inputs=[
            {"name": "model", "type": "MODEL", "link": None},
            {"name": "context_options", "type": "CONTEXT_OPTIONS", "link": None},
        ],
        outputs=[{"name": "MODEL", "type": "MODEL"}],
        properties={"Node name for S&R": "ADE_AnimateDiffLoaderGen1", "cnr_id": "comfyui-animatediff-evolved", "ver": "1.5.7"},
        widgets_values=["mm_sd_v15_v2.ckpt", "autoselect"],
    )

    neg = w.node(
        type="CLIPTextEncode", pos=[-760, 720], size=[420, 130], order=3,
        inputs=[{"name": "clip", "type": "CLIP", "link": None}],
        outputs=[{"name": "CONDITIONING", "type": "CONDITIONING"}],
        title="Negative (shared)",
        properties={"Node name for S&R": "CLIPTextEncode", "cnr_id": "comfy-core", "ver": "0.24.0"},
        widgets_values=[NEGATIVE],
    )

    w.connect(ckpt, 0, ade, 0, "MODEL")
    w.connect(ctx, 0, ade, 1, "CONTEXT_OPTIONS")
    w.connect(ckpt, 1, neg, 0, "CLIP")

    segment_out = []

    for i, chapter in enumerate(chapters):
        y = 40 + i * 200
        x = -360

        latent = w.node(
            type="EmptyLatentImage", pos=[x, y], size=[280, 110], order=4 + i,
            outputs=[{"name": "LATENT", "type": "LATENT"}],
            title=f"Segment {i + 1} — {FRAMES} frames",
            properties={"Node name for S&R": "EmptyLatentImage", "cnr_id": "comfy-core", "ver": "0.24.0"},
            widgets_values=[512, 512, FRAMES],
        )

        pos = w.node(
            type="CLIPTextEncode", pos=[x + 300, y], size=[420, 160], order=14 + i,
            inputs=[{"name": "clip", "type": "CLIP", "link": None}],
            outputs=[{"name": "CONDITIONING", "type": "CONDITIONING"}],
            title=f"Chapter {i + 1} prompt",
            properties={"Node name for S&R": "CLIPTextEncode", "cnr_id": "comfy-core", "ver": "0.24.0"},
            widgets_values=[STYLE_PREFIX + chapter + STYLE_SUFFIX],
            color="#232", bgcolor="#353",
        )

        ks = w.node(
            type="KSampler", pos=[x + 760, y], size=[300, 280], order=24 + i,
            inputs=[
                {"name": "model", "type": "MODEL", "link": None},
                {"name": "positive", "type": "CONDITIONING", "link": None},
                {"name": "negative", "type": "CONDITIONING", "link": None},
                {"name": "latent_image", "type": "LATENT", "link": None},
            ],
            outputs=[{"name": "LATENT", "type": "LATENT"}],
            title=f"KSampler {i + 1}/{seg_total}",
            properties={"Node name for S&R": "KSampler", "cnr_id": "comfy-core", "ver": "0.24.0"},
            widgets_values=[BASE_SEED + i, "fixed", steps, 7.5, "euler", "normal", 1],
        )

        dec = w.node(
            type="VAEDecode", pos=[x + 1100, y], size=[210, 60], order=34 + i,
            inputs=[
                {"name": "samples", "type": "LATENT", "link": None},
                {"name": "vae", "type": "VAE", "link": None},
            ],
            outputs=[{"name": "IMAGE", "type": "IMAGE"}],
            properties={"Node name for S&R": "VAEDecode", "cnr_id": "comfy-core", "ver": "0.24.0"},
        )

        w.connect(ckpt, 1, pos, 0, "CLIP")
        w.connect(ade, 0, ks, 0, "MODEL")
        w.connect(pos, 0, ks, 1, "CONDITIONING")
        w.connect(neg, 0, ks, 2, "CONDITIONING")
        w.connect(latent, 0, ks, 3, "LATENT")
        w.connect(ks, 0, dec, 0, "LATENT")
        w.connect(ckpt, 2, dec, 1, "VAE")
        segment_out.append(dec)

    prev = segment_out[0]
    for j in range(1, len(segment_out)):
        m = w.node(
            type="VHS_MergeImages", pos=[1600, 80 + j * 85], size=[315, 146], order=44 + j,
            inputs=[
                {"name": "images_A", "type": "IMAGE", "link": None},
                {"name": "images_B", "type": "IMAGE", "link": None},
            ],
            outputs=[
                {"name": "IMAGE", "type": "IMAGE"},
                {"name": "count", "type": "INT"},
            ],
            title=f"Stitch 1-{j + 1}",
            properties={"Node name for S&R": "VHS_MergeImages", "cnr_id": "comfyui-videohelpersuite", "ver": "1.7.7"},
            widgets_values=["match A", "bicubic", "disabled"],
        )
        w.connect(prev, 0, m, 0, "IMAGE")
        w.connect(segment_out[j], 0, m, 1, "IMAGE")
        prev = m

    combine = w.node(
        type="VHS_VideoCombine", pos=[2000, 200], size=[315, 620], order=90,
        inputs=[{"name": "images", "type": "IMAGE", "link": None}],
        outputs=[{"name": "Filenames", "type": "VHS_FILENAMES"}],
        title=f"FINAL {duration:.0f} sec MP4",
        properties={"Node name for S&R": "VHS_VideoCombine", "cnr_id": "comfyui-videohelpersuite", "ver": "1.7.9"},
        widgets_values={
            "frame_rate": FPS,
            "loop_count": 0,
            "filename_prefix": out_prefix,
            "format": "video/h264-mp4",
            "pix_fmt": "yuv420p",
            "crf": 18,
            "save_metadata": True,
            "trim_to_audio": False,
            "pingpong": False,
            "save_output": True,
        },
    )

    preview = w.node(
        type="PreviewImage", pos=[2000, 860], size=[315, 250], order=91,
        inputs=[{"name": "images", "type": "IMAGE", "link": None}],
        title=f"Preview all {total_frames} frames",
        properties={"Node name for S&R": "PreviewImage", "cnr_id": "comfy-core", "ver": "0.24.0"},
    )

    w.connect(prev, 0, combine, 0, "IMAGE")
    w.connect(prev, 0, preview, 0, "IMAGE")
    w.finalize_outputs()

    workflow = {
        "id": "animal-story-quick-test" if quick else "animal-story-10seg-stitch-1min",
        "revision": 3 if quick else 2,
        "last_node_id": w.nid - 1,
        "last_link_id": w.link_id - 1,
        "nodes": w.nodes,
        "links": w.links,
        "groups": [{
            "id": 1,
            "title": group_title,
            "bounding": [-1140, 0, 3500, max(600, 200 + len(chapters) * 200)],
            "color": "#8A8",
            "flags": {},
        }],
        "config": {},
        "extra": {"frontendVersion": "1.45.15", "ds": {"scale": 0.42, "offset": [1180, 30]}},
        "version": 0.4,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(workflow, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} ({len(w.nodes)} nodes, {len(w.links)} links)")
    print(f"  Mode: {'QUICK TEST' if quick else 'FULL'} — {seg_total} segments, {total_frames} frames, ~{duration:.0f}s @ {FPS} fps")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build animal story ComfyUI workflow JSON")
    parser.add_argument("--quick", action="store_true", help="2 segments, ~12 sec, 8 steps (CPU test)")
    parser.add_argument("--full", action="store_true", help="10 segments, 60 sec (default)")
    args = parser.parse_args()
    build(quick=args.quick and not args.full)
