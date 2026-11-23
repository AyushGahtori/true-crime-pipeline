"""Stdlib validator for Task 004 v4 golden packs. Does not import packages outside this worktree."""

from __future__ import annotations

import json
import math
import re
import struct
import sys
import wave
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "fixtures"
PACKS = (
    "ep_golden_01_20min",
    "ep_golden_02_2strike_fallback",
    "ep_golden_03_2k_grid_heavy",
)
DISCLAIMER = "ILLUSTRATIVE RECONSTRUCTION \u2014 NOT CRIME SCENE PHOTO"
BADGE = "TRANSCRIPT DRAMATIZATION"
VIDEO_MODES = {"TEXT_TO_VIDEO", "FIRST_FRAME", "FIRST_AND_LAST_FRAME"}
RETIRED = ("FRAMES_MOTION_ONLY", "VEO_3_1_LITE", "Veo 3.1 Lite", "CrimeScenePanZoom", "veo-3.1-lite")
FORBIDDEN_KEYS = {
    "monetizationDetails",
    "monetization_status",
    "estimatedRevenue",
    "estimated_revenue",
    "adsense_revenue",
    "yellow_icon",
    "yellowIcon",
}
CODE_FOIA = {"CODE_STICKMAN", "AUDIO_EVIDENCE_CARD", "FOIA_REAL_FOOTAGE"}
ENGINE_MOTIF = {
    "CODE_STICKMAN": {"StickmanStage", "RedactedDocReveal"},
    "AUDIO_EVIDENCE_CARD": {"AudioEvidenceCard"},
    "FOIA_REAL_FOOTAGE": {"FoiaFootageFrame"},
    "STILL_2K_PANZOOM": {"Illustrative2KPanZoom"},
    "FLOW_HERO_VIDEO": {"HeroVideoBridge"},
}
MVP = ("StickmanStage", "AudioEvidenceCard", "RedactedDocReveal", "FoiaFootageFrame")


def sha256_text(text: str) -> str:
    import hashlib

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_bytes(data: bytes) -> str:
    import hashlib

    return hashlib.sha256(data).hexdigest()


def asset_version(scene_id: str, narration_sha: str, engine: str, start: int, end: int, motif: str) -> str:
    return sha256_text(f"v4|{scene_id}|{narration_sha}|{engine}|{start}|{end}|{motif}")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def type_ok(value, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "null":
        return value is None
    return False


def validate_schema(instance, schema: dict, path: str, errors: list[str]) -> None:
    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path} const {schema['const']!r} != {instance!r}")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path} value {instance!r} not in enum")
    expected = schema.get("type")
    if isinstance(expected, list):
        if not any(type_ok(instance, item) for item in expected):
            errors.append(f"{path} type {type(instance).__name__} not in {expected}")
            return
    elif expected and not type_ok(instance, expected):
        errors.append(f"{path} type {type(instance).__name__} != {expected}")
        return
    if isinstance(instance, str) and "pattern" in schema and re.search(schema["pattern"], instance) is None:
        errors.append(f"{path} does not match {schema['pattern']}")
    if isinstance(instance, str) and "minLength" in schema and len(instance) < schema["minLength"]:
        errors.append(f"{path} shorter than {schema['minLength']}")
    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{path} < {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            errors.append(f"{path} > {schema['maximum']}")
    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path} minItems")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            errors.append(f"{path} maxItems")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(instance):
                validate_schema(item, item_schema, f"{path}[{index}]", errors)
    if isinstance(instance, dict):
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in instance:
                errors.append(f"{path} missing {key}")
        additional = schema.get("additionalProperties", True)
        for key, value in instance.items():
            if key in properties:
                validate_schema(value, properties[key], f"{path}.{key}", errors)
            elif additional is False:
                errors.append(f"{path} unexpected {key}")


def walk_keys(node, found: list[str]) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            if key in FORBIDDEN_KEYS:
                found.append(key)
            walk_keys(value, found)
    elif isinstance(node, list):
        for item in node:
            walk_keys(item, found)


def is_crimson(r: int, g: int, b: int) -> bool:
    if (r, g, b) == (0xC9, 0x2A, 0x2A):
        return True
    return r >= 170 and g <= 70 and b <= 70 and (r - g) >= 80 and (r - b) >= 80


def png_crimson_count(path: Path) -> tuple[int, int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise RuntimeError(f"bad png {path}")
    pos = 8
    ihdr = None
    idat = bytearray()
    while pos < len(data):
        length = struct.unpack(">I", data[pos : pos + 4])[0]
        tag = data[pos + 4 : pos + 8]
        payload = data[pos + 8 : pos + 8 + length]
        pos += 12 + length
        if tag == b"IHDR":
            ihdr = payload
        elif tag == b"IDAT":
            idat.extend(payload)
        elif tag == b"IEND":
            break
    width, height, bit, color, comp, filt, inter = struct.unpack(">IIBBBBB", ihdr)
    if (bit, color, inter) != (8, 2, 0):
        raise RuntimeError(f"png mode {path}")
    raw = zlib.decompress(bytes(idat))
    stride = width * 3
    count = 0
    index = 0
    for _ in range(height):
        if raw[index] != 0:
            raise RuntimeError(f"png filter {path}")
        index += 1
        row = raw[index : index + stride]
        index += stride
        for i in range(0, len(row), 3):
            if is_crimson(row[i], row[i + 1], row[i + 2]):
                count += 1
    return width, height, count


def iter_boxes(data: bytes, start: int, end: int):
    pos = start
    while pos + 8 <= end:
        size = struct.unpack(">I", data[pos : pos + 4])[0]
        typ = data[pos + 4 : pos + 8]
        if size < 8 or pos + size > end:
            break
        yield typ, pos + 8, pos + size
        pos += size


def find_box(data: bytes, start: int, end: int, target: bytes):
    for typ, payload_start, box_end in iter_boxes(data, start, end):
        if typ == target:
            return payload_start, box_end
        if typ in {b"moov", b"trak", b"mdia", b"minf", b"stbl"}:
            found = find_box(data, payload_start, box_end, target)
            if found:
                return found
    return None


def read_mp4_pcm(path: Path) -> tuple[int, list[int]]:
    data = path.read_bytes()
    if b"ftyp" not in data[:32]:
        raise RuntimeError("mp4 missing ftyp")
    stsd = find_box(data, 0, len(data), b"stsd")
    stsz = find_box(data, 0, len(data), b"stsz")
    stco = find_box(data, 0, len(data), b"stco")
    if not (stsd and stsz and stco):
        raise RuntimeError("mp4 missing sample tables")
    stsd_payload = data[stsd[0] : stsd[1]]
    entry_off = 8
    coding = stsd_payload[entry_off + 4 : entry_off + 8]
    if coding != b"sowt":
        raise RuntimeError(f"mp4 coding {coding!r} is not sowt PCM")
    sample_rate = struct.unpack(">I", stsd_payload[entry_off + 32 : entry_off + 36])[0] >> 16
    stsz_payload = data[stsz[0] : stsz[1]]
    sample_size, sample_count = struct.unpack(">II", stsz_payload[4:12])
    stco_payload = data[stco[0] : stco[1]]
    offset = struct.unpack(">I", stco_payload[8:12])[0]
    pcm = data[offset : offset + sample_size * sample_count]
    if len(pcm) != sample_size * sample_count:
        raise RuntimeError("mp4 pcm truncated")
    samples = list(struct.unpack("<" + "h" * sample_count, pcm))
    return sample_rate, samples


def goertzel_power(samples: list[int], freq: float, rate: int) -> float:
    count = len(samples)
    k = int(0.5 + (count * freq / rate))
    w = 2 * math.pi * k / count
    coeff = 2 * math.cos(w)
    s1 = 0.0
    s2 = 0.0
    for sample in samples:
        s0 = sample + coeff * s1 - s2
        s2 = s1
        s1 = s0
    return s1 * s1 + s2 * s2 - coeff * s1 * s2


def contiguous(rows: list[dict], start_key: str, end_key: str, total: int, label: str, errors: list[str]) -> None:
    cursor = 0
    for index, row in enumerate(rows):
        if row[start_key] != cursor:
            errors.append(f"{label}[{index}] starts at {row[start_key]} expected {cursor}")
        if row[end_key] <= row[start_key]:
            errors.append(f"{label}[{index}] empty interval")
        cursor = row[end_key]
    if cursor != total:
        errors.append(f"{label} ends at {cursor} expected {total}")


def check_pack(pack: dict, raw: str, errors: list[str]) -> None:
    pack_id = pack["pack_id"]
    if pack_id not in PACKS:
        errors.append(f"unexpected pack {pack_id}")
    if pack["contract_version"] != "4":
        errors.append(f"{pack_id} contract_version")
    for token in RETIRED:
        if token in raw:
            errors.append(f"{pack_id} contains retired identifier {token}")
    if "</data>" in raw or "IGNORE PREVIOUS INSTRUCTIONS" in raw:
        errors.append(f"{pack_id} propagated an injection delimiter into the pack")
    if "406-555-0142" in raw or "18 Fixture Lane" in raw or "Casey Quinn" in raw:
        errors.append(f"{pack_id} copied spoken PII into the episode pack")
    forbidden = []
    walk_keys(pack, forbidden)
    if forbidden:
        errors.append(f"{pack_id} forbidden monetization keys {forbidden}")

    split = pack["runtime_split"]
    if (split["code_foia_ms"], split["still_2k_panzoom_ms"], split["flow_hero_video_ms"]) != (780000, 340000, 80000):
        errors.append(f"{pack_id} runtime split ms")
    if (split["code_foia_min_label"], split["still_2k_panzoom_min_label"], split["flow_hero_video_min_label"]) != (13.0, 5.67, 1.33):
        errors.append(f"{pack_id} runtime split labels")
    episode = pack["episode"]
    if episode["max_hero_clips"] != 10 or episode["max_hero_duration_sec"] != 80:
        errors.append(f"{pack_id} hero caps")
    if episode["target_duration_ms"] != 1200000 or episode["total_master_ms"] != 1200000:
        errors.append(f"{pack_id} master duration")
    if episode["video_budget_cap_micro_usd"] != 10400000:
        errors.append(f"{pack_id} video cap")
    if episode["flow_backend_mode"] != "GEMINI_OMNI_INTERACTIONS":
        errors.append(f"{pack_id} backend")
    if episode["cold_open_archetype"] != "911_CALL_IN_MEDIA_RES":
        errors.append(f"{pack_id} cold open")
    if episode["altered_content_disclosure"] != 1:
        errors.append(f"{pack_id} disclosure")

    plans = pack["scene_plans"]
    scenes = pack["scenes"]
    contiguous(scenes, "start_ms", "end_ms", 1200000, f"{pack_id} scenes", errors)
    sums = {"code_foia": 0, "still": 0, "hero": 0}
    motifs = set()
    hero_modes = []
    run_engine = None
    run_ms = 0
    for index, scene in enumerate(scenes):
        plan = plans[index]
        engine = scene["visual_engine"]
        if plan["visual_engine"] != engine or plan["motif_component"] != scene["motif_component"]:
            errors.append(f"{pack_id} plan/scene mismatch {scene['scene_id']}")
        if plan["plan_status"] != "EDITED_APPROVED" or not plan["reviewed_by"] or not plan["reviewed_at"]:
            errors.append(f"{pack_id} plan not EDITED_APPROVED {scene['scene_id']}")
        if plan["asset_version_sha256"] != asset_version(
            plan["scene_id"],
            plan["narration_version_sha256"],
            engine,
            plan["timing_start_ms"],
            plan["timing_end_ms"],
            plan["motif_component"],
        ):
            errors.append(f"{pack_id} asset sha {scene['scene_id']}")
        if sha256_text(plan["approved_narration_text"]) != plan["narration_version_sha256"]:
            errors.append(f"{pack_id} narration sha {scene['scene_id']}")
        if not plan["cited_fact_ids_json"] or not plan["acceptance_criteria_json"]:
            errors.append(f"{pack_id} empty citations or acceptance {scene['scene_id']}")
        if plan["timing_start_ms"] != scene["start_ms"] or plan["timing_end_ms"] != scene["end_ms"]:
            errors.append(f"{pack_id} timing mismatch {scene['scene_id']}")
        motif = scene["motif_component"]
        if motif not in ENGINE_MOTIF[engine]:
            errors.append(f"{pack_id} motif {motif} not owned by {engine}")
        mode = plan["prompt_mode"]
        if engine == "FLOW_HERO_VIDEO":
            if mode not in VIDEO_MODES:
                errors.append(f"{pack_id} hero prompt_mode {mode}")
            hero_modes.append(mode)
            sums["hero"] += scene["end_ms"] - scene["start_ms"]
            duration = scene["end_ms"] - scene["start_ms"]
            if duration < 3000 or duration > 15000:
                errors.append(f"{pack_id} hero duration {duration}")
            if mode == "FIRST_AND_LAST_FRAME" and duration > 10000:
                errors.append(f"{pack_id} FIRST_AND_LAST_FRAME over 10s")
        else:
            if mode != "NONE":
                errors.append(f"{pack_id} non-hero prompt_mode {mode}")
            if engine in CODE_FOIA:
                sums["code_foia"] += scene["end_ms"] - scene["start_ms"]
                motifs.add(motif)
            elif engine == "STILL_2K_PANZOOM":
                sums["still"] += scene["end_ms"] - scene["start_ms"]
        if engine == run_engine:
            run_ms += scene["end_ms"] - scene["start_ms"]
        else:
            if run_ms > 50000:
                errors.append(f"{pack_id} engine streak {run_engine} {run_ms}ms")
            run_engine = engine
            run_ms = scene["end_ms"] - scene["start_ms"]
        if index:
            prev = scenes[index - 1]
            nxt = scene
            if prev["visual_engine"] == "FLOW_HERO_VIDEO" or nxt["visual_engine"] == "FLOW_HERO_VIDEO":
                hero = prev if prev["visual_engine"] == "FLOW_HERO_VIDEO" else nxt
                other = nxt if hero is prev else prev
                fallback = hero["fallback_spec_json"]
                if not fallback or fallback["engine"] == other["visual_engine"] or fallback["engine"] == "FLOW_HERO_VIDEO":
                    errors.append(f"{pack_id} neighbor fallback {hero['scene_id']}")
    if run_ms > 50000:
        errors.append(f"{pack_id} engine streak {run_engine} {run_ms}ms")
    if sums != {"code_foia": 780000, "still": 340000, "hero": 80000}:
        errors.append(f"{pack_id} measured split {sums}")
    if set(MVP) - motifs:
        errors.append(f"{pack_id} missing mvp motifs {set(MVP) - motifs}")
    if hero_modes != ["TEXT_TO_VIDEO"] * 4 + ["FIRST_FRAME"] * 3 + ["FIRST_AND_LAST_FRAME"] * 3:
        errors.append(f"{pack_id} hero mode mix {hero_modes}")
    if scenes[0]["visual_engine"] != "FOIA_REAL_FOOTAGE" or "?" not in plans[0]["approved_narration_text"]:
        errors.append(f"{pack_id} cold open question")
    act2_peaks = [s for s in scenes if s["act_number"] == 2 and s["emotional_peak_score"] >= 0.8]
    if len(act2_peaks) < 2:
        errors.append(f"{pack_id} act 2 peaks")

    facts = {fact["fact_id"]: fact for fact in pack["temporal_fact_ledger"]}
    docs = {doc["doc_id"] for doc in pack["primary_documents"]}
    for fact in facts.values():
        if fact["source_doc_id"] not in docs:
            errors.append(f"{pack_id} fact doc missing {fact['fact_id']}")
        if fact["source_type"] == "news_report" and fact["hedging_required"] != 1:
            errors.append(f"{pack_id} news fact missing hedge")
        if fact["source_type"] != "news_report" and fact["hedging_required"] != 0:
            errors.append(f"{pack_id} primary fact hedged")
    for plan in plans:
        for fact_id in plan["cited_fact_ids_json"]:
            fact = facts.get(fact_id)
            if fact is None:
                errors.append(f"{pack_id} unknown fact {fact_id}")
            elif fact["source_type"] == "news_report" and "reported" not in plan["approved_narration_text"].lower():
                errors.append(f"{pack_id} news citation not hedged in narration")
        if plan["motif_component"] == "AudioEvidenceCard" and BADGE not in plan["visual_concept"]:
            errors.append(f"{pack_id} missing transcript badge")
        if plan["motif_component"] == "Illustrative2KPanZoom" and DISCLAIMER not in plan["visual_concept"]:
            errors.append(f"{pack_id} missing illustrative label in concept")
        if plan["motif_component"] == "HeroVideoBridge" and "#C92A2A" in plan["visual_prompt"]:
            errors.append(f"{pack_id} crimson hex in hero prompt")

    case = pack["compliance_cleared_case"]["case"]
    if case["disposition_status"] != "AFFIRMED" or case["conviction_confirmed"] != 1:
        errors.append(f"{pack_id} disposition")
    if case["anonymization_status"] != "APPROVED":
        errors.append(f"{pack_id} anonymization")
    if case["anonymization_artifact_sha256"] != sha256_text(f"anonymized-fixture-v4:{case['case_id']}"):
        errors.append(f"{pack_id} anonymization sha")
    audit = pack["compliance_cleared_case"]["compliance_audit"]
    for flag in (
        "provenance_whitelist_ok",
        "that_vs_how_passed",
        "anti_legal_persona_passed",
        "first_30s_adsense_safe",
        "spoken_pii_audit_passed",
        "altered_content_disclosure",
    ):
        if audit[flag] != 1:
            errors.append(f"{pack_id} audit {flag}")

    stills = {still["still_2k_id"]: still for still in pack["still_assets"]}
    for still in stills.values():
        if still["is_illustrative_reconstruction"] != 1 or still["disclaimer_label_text"] != DISCLAIMER:
            errors.append(f"{pack_id} still disclaimer {still['still_2k_id']}")
        plate = ROOT / still["asset_path"]
        width, height, crimson = png_crimson_count(plate)
        if (width, height) != (still["width_px"], still["height_px"]) or width < 1920 or height < 1080:
            errors.append(f"{pack_id} plate size {still['asset_path']}")
        if crimson:
            errors.append(f"{pack_id} plate crimson {crimson}")
        if sha256_bytes(plate.read_bytes()) != still["asset_sha256"]:
            errors.append(f"{pack_id} plate sha")

    cells = []
    for anchor in pack["spatial_anchors"]:
        if anchor["lock_status"] != "LOCKED" or not anchor["locked_by"] or not anchor["locked_at"]:
            errors.append(f"{pack_id} anchor not locked {anchor['anchor_id']}")
        still = stills[anchor["still_2k_id"]]
        if anchor["still_asset_sha256"] != still["asset_sha256"]:
            errors.append(f"{pack_id} anchor sha {anchor['anchor_id']}")
        if not re.fullmatch(r"[A-J](?:[1-9]|10)", anchor["grid_cell"]):
            errors.append(f"{pack_id} grid cell {anchor['grid_cell']}")
        col = ord(anchor["grid_cell"][0]) - ord("A")
        row = int(anchor["grid_cell"][1:]) - 1
        if anchor["x_px"] != col * (still["width_px"] // 10) or anchor["y_px"] != row * (still["height_px"] // 10):
            errors.append(f"{pack_id} anchor pixel {anchor['anchor_id']}")
        if not (0 < anchor["span_cols"] <= 10 and 0 < anchor["span_rows"] <= 10):
            errors.append(f"{pack_id} span {anchor['anchor_id']}")
        if not (1.0 <= anchor["target_zoom"] <= 3.8):
            errors.append(f"{pack_id} zoom {anchor['anchor_id']}")
        cells.append(anchor["grid_cell"])
    if pack_id == "ep_golden_03_2k_grid_heavy":
        expected = {f"{col}{row}" for col in "ABCDEFGHIJ" for row in range(1, 11)}
        if set(cells) != expected:
            errors.append(f"{pack_id} grid coverage {len(set(cells))}")
    elif len(pack["spatial_anchors"]) < 14:
        errors.append(f"{pack_id} expected at least 14 anchors")

    assets = {asset["asset_id"]: asset for asset in pack["foia_media_assets"]}
    pii_ids = {asset["asset_id"] for asset in assets.values() if asset["spoken_pii_bleeped"] == 0}
    body_ids = {asset["asset_id"] for asset in assets.values() if asset["raw_path"].endswith("bodycam_440hz_music_042profanity.mp4")}
    call_ids = {asset["asset_id"] for asset in assets.values() if asset["raw_path"].endswith("911_8khz_distorted.wav")}
    for asset in assets.values():
        blob = (ROOT / asset["raw_path"]).read_bytes()
        if sha256_bytes(blob) != asset["sha256"]:
            errors.append(f"{pack_id} foia sha {asset['asset_id']}")
        if asset["rights_review_status"] == "APPROVED" and not (asset["rights_reviewed_by"] and asset["rights_reviewed_at"]):
            errors.append(f"{pack_id} rights reviewer")
        if asset["raw_path"].endswith("911_8khz_distorted.wav"):
            if asset["music_detected"] != 0 or asset["demucs_applied"] != 0:
                errors.append(f"{pack_id} 911 should bypass demucs")
        if asset["raw_path"].endswith("bodycam_440hz_music_042profanity.mp4"):
            if asset["music_detected"] != 1:
                errors.append(f"{pack_id} bodycam music flag")
            intervals = asset["profanity_intervals_json"]
            if not intervals or intervals[0]["start_ms"] != 42000 or intervals[0]["severity"] != "severe":
                errors.append(f"{pack_id} profanity map")

    for scene in scenes:
        if scene["start_ms"] < 30000:
            plan = next(p for p in plans if p["scene_id"] == scene["scene_id"])
            if scene["visual_engine"] == "FOIA_REAL_FOOTAGE":
                voice = next(v for v in pack["voice_track_manifest"]["segments"] if v["start_ms"] == scene["start_ms"])
                if voice["foia_asset_id"] in body_ids:
                    errors.append(f"{pack_id} bodycam inside first 30s")
            if "#C92A2A" in plan["visual_prompt"]:
                errors.append(f"{pack_id} crimson in opening prompt")

    voice = pack["voice_track_manifest"]["segments"]
    contiguous(voice, "start_ms", "end_ms", 1200000, f"{pack_id} voice", errors)
    twists = [seg for seg in voice if seg["segment_kind"] == "TWIST_PAD"]
    if len(twists) != 3 or any(not (450 <= seg["end_ms"] - seg["start_ms"] <= 750) for seg in twists):
        errors.append(f"{pack_id} twist pads")
    for seg in voice:
        if seg["segment_kind"] == "NARRATION":
            if not seg["audio_path"] or seg["foia_asset_id"] is not None:
                errors.append(f"{pack_id} narration slot {seg['segment_id']}")
            owner = next(scene for scene in scenes if scene["start_ms"] == seg["start_ms"])
            plan = next(p for p in plans if p["scene_id"] == owner["scene_id"])
            if seg["narration_version_sha256"] != plan["narration_version_sha256"]:
                errors.append(f"{pack_id} voice hash {seg['segment_id']}")
        elif seg["segment_kind"] == "FOIA_AUDIO_SLOT":
            if seg["foia_asset_id"] not in assets or seg["audio_path"] is not None:
                errors.append(f"{pack_id} foia slot {seg['segment_id']}")
            if seg["foia_asset_id"] in pii_ids:
                errors.append(f"{pack_id} unbleeped PII is on the timeline")
        elif seg["segment_kind"] == "TWIST_PAD":
            if seg["audio_path"] is not None or seg["foia_asset_id"] is not None:
                errors.append(f"{pack_id} twist slot fields")
        for stamp in seg["word_timestamps"]:
            if not (seg["start_ms"] <= stamp["start_ms"] < stamp["end_ms"] <= seg["end_ms"]):
                errors.append(f"{pack_id} word outside segment {seg['segment_id']}")
    if not any(seg["foia_asset_id"] in call_ids for seg in voice):
        errors.append(f"{pack_id} 911 call missing from voice")

    canonical = json.dumps(
        [
            {
                "scene_id": scene["scene_id"],
                "start_ms": scene["start_ms"],
                "end_ms": scene["end_ms"],
                "visual_engine": scene["visual_engine"],
            }
            for scene in scenes
        ],
        separators=(",", ":"),
        ensure_ascii=False,
    )
    if episode["timeline_validated_sha256"] != sha256_text(canonical):
        errors.append(f"{pack_id} timeline sha")

    spec = pack["timeline_spec"]
    if spec["fps"] != 30 or spec["frame_count"] != 36000:
        errors.append(f"{pack_id} timeline fps")
    if sum(row["duration_frames"] for row in spec["scenes"]) != 36000:
        errors.append(f"{pack_id} frame sum")
    manifest = pack["production_manifest"]
    if manifest["motif_registry_version"] != "MOTIF_REGISTRY_V1" or manifest["fps"] != 30:
        errors.append(f"{pack_id} manifest")
    if manifest["primary_video_model"] != "gemini-omni-1.2-flash":
        errors.append(f"{pack_id} video model")
    if manifest["offline_test_spend_cap_micro_usd"] != 0:
        errors.append(f"{pack_id} offline cap")
    registry = {row["motif_component"]: row for row in pack["motif_registry_v1"]}
    for name in MVP:
        if registry[name]["is_mvp_4"] != 1 or registry[name]["owner_package"] != "render_catalog":
            errors.append(f"{pack_id} registry {name}")
    if registry["Illustrative2KPanZoom"]["owner_package"] != "crime_scene_2k":
        errors.append(f"{pack_id} 2k owner")
    if registry["HeroVideoBridge"]["owner_package"] != "flow_adapter":
        errors.append(f"{pack_id} hero owner")

    jobs = pack["flow_job_cards"]
    if len(jobs) != 10:
        errors.append(f"{pack_id} hero job count {len(jobs)}")
    if sum(job["estimated_micro_usd"] for job in jobs) != 8000000:
        errors.append(f"{pack_id} hero estimate")
    attempts_by_job = {}
    for attempt in pack["flow_job_attempts"]:
        attempts_by_job.setdefault(attempt["flow_job_id"], []).append(attempt)
        if attempt["cost_micro_usd"] != 0:
            errors.append(f"{pack_id} attempt cost")
    states = []
    for job in jobs:
        states.append(job["state"])
        if job["prompt_mode"] not in VIDEO_MODES:
            errors.append(f"{pack_id} job mode")
        if job["duration_bucket_sec"] != 8 or job["estimated_micro_usd"] != 800000:
            errors.append(f"{pack_id} job bucket")
        if job["engine_model"] != "gemini-omni-1.2-flash":
            errors.append(f"{pack_id} job model")
        if job["attempts_used"] > 2:
            errors.append(f"{pack_id} attempts_used")
        rows = attempts_by_job[job["flow_job_id"]]
        if len(rows) != job["attempts_used"]:
            errors.append(f"{pack_id} attempt rows")
        mode = job["prompt_mode"]
        if mode == "TEXT_TO_VIDEO" and (job["start_frame_png"] or job["end_frame_png"]):
            errors.append(f"{pack_id} text-to-video frames")
        if mode == "FIRST_FRAME" and not (job["start_frame_png"] and job["end_frame_png"] is None):
            errors.append(f"{pack_id} first-frame frames")
        if mode == "FIRST_AND_LAST_FRAME" and not (job["start_frame_png"] and job["end_frame_png"]):
            errors.append(f"{pack_id} bookend frames")
        if job["fallback_spec_json"]["engine"] != "STILL_2K_PANZOOM":
            errors.append(f"{pack_id} fallback engine")
        for frame_path in (job["start_frame_png"], job["end_frame_png"]):
            if not frame_path:
                continue
            frame = ROOT / frame_path
            _w, _h, crimson = png_crimson_count(frame)
            if crimson:
                errors.append(f"{pack_id} keyframe crimson {frame_path}")
            if "Monochrome" not in json.dumps(next(p for p in plans if p["scene_id"] == job["scene_id"])["keyframe_refs_json"]):
                errors.append(f"{pack_id} keyframe description")
    if pack_id == "ep_golden_02_2strike_fallback":
        if states.count("SWITCHED_TO_FALLBACK") != 1 or states.count("STRIKE_1_RETRY_SAFE") != 1 or states.count("ACCEPTED") != 8:
            errors.append(f"{pack_id} strike states {states}")
        switched = next(job for job in jobs if job["state"] == "SWITCHED_TO_FALLBACK")
        if switched["attempts_used"] != 2:
            errors.append(f"{pack_id} strike 2 attempts")
        verdicts = [row["qa_verdict"] for row in attempts_by_job[switched["flow_job_id"]]]
        if verdicts != ["FAIL_MORPH", "FAIL_DURATION_RES"]:
            errors.append(f"{pack_id} strike verdicts {verdicts}")
    elif states != ["ACCEPTED"] * 10:
        errors.append(f"{pack_id} expected accepted jobs")

    for reservation in pack["provider_spend_reservations"]:
        if reservation["purpose"] != "OFFLINE_TEST" or reservation["estimated_micro_usd"] != 0:
            errors.append(f"{pack_id} offline reservation spend")
        if reservation["status"] != "RELEASED":
            errors.append(f"{pack_id} reservation status")

    analytics = pack["episode_analytics"]
    if analytics["adsense_status"] != "UNKNOWN" or analytics["adsense_source"] != "UNAVAILABLE":
        errors.append(f"{pack_id} adsense status")
    if analytics["rpm_micro_usd"] is not None or analytics["ctr_pct"] is not None:
        errors.append(f"{pack_id} fabricated analytics metric")
    if analytics["watch_hours_total"] != 0.0:
        errors.append(f"{pack_id} watch hours")
    ready = pack["ready_to_upload_pack"]
    if ready["status"] != "NOT_READY":
        errors.append(f"{pack_id} ready status")
    gates = [gate["gate_name"] for gate in ready["gates"]]
    if gates != [
        "FACTUAL_ACCURACY",
        "PRIVACY_PII",
        "SOURCE_RIGHTS",
        "SYNTHETIC_DISCLOSURE",
        "ILLUSTRATIVE_LABELING",
    ]:
        errors.append(f"{pack_id} gates")
    if any(gate["status"] != "PENDING" for gate in ready["gates"]):
        errors.append(f"{pack_id} gate fabricated approval")

    seed_keys = set(pack["seed_packet"])
    if seed_keys != {
        "suspect_names",
        "victim_names",
        "incident_date_or_year",
        "county_state",
        "docket_ids",
        "unanswered_comment_questions",
    }:
        errors.append(f"{pack_id} seed packet keys")


def check_recorded(errors: list[str]) -> None:
    recorded = FIX / "recorded_apis"
    files = {
        "youtube_videos_list.json": "youtube_videos_list",
        "courtlistener_search.json": "courtlistener_search",
        "muckrock_foia_requests.json": "muckrock_foia_requests",
        "adversarial_prompt_injection.json": "adversarial_prompt_injection",
    }
    for name, kind in files.items():
        path = recorded / name
        payload = load_json(path)
        raw = path.read_text(encoding="utf-8")
        if payload.get("fixture_kind") != kind:
            errors.append(f"{name} fixture_kind")
        controls = payload.get("fixture_controls") or {}
        if controls.get("live_http") is not False or controls.get("authorization_header_present") is not False:
            errors.append(f"{name} live controls")
        if controls.get("api_key_material_present") is not False:
            errors.append(f"{name} api key flag")
        if re.search(r"AIza[0-9A-Za-z_\-]{20,}|Bearer |sk-", raw):
            errors.append(f"{name} secret-like material")
        forbidden = []
        walk_keys(payload, forbidden)
        if forbidden:
            errors.append(f"{name} forbidden keys {forbidden}")
    youtube = load_json(recorded / "youtube_videos_list.json")
    if "monetizationDetails" in json.dumps(youtube):
        errors.append("youtube mock includes monetizationDetails")
    if youtube["fixture_controls"].get("captions_download_called") is not False:
        errors.append("youtube captions.download was recorded as called")
    if not youtube["items"][0]["statistics"].get("viewCount"):
        errors.append("youtube statistics")
    court = load_json(recorded / "courtlistener_search.json")
    if court["count"] != 1 or court["results"][0]["docket_number"] != "2019-CR-1042":
        errors.append("courtlistener mock")
    if court["fixture_controls"].get("daily_limit") != 125:
        errors.append("courtlistener quota")
    muck = load_json(recorded / "muckrock_foia_requests.json")
    if muck["count"] != 1 or muck["results"][0]["status"] != "done":
        errors.append("muckrock mock")
    attack = load_json(recorded / "adversarial_prompt_injection.json")
    blob = json.dumps(attack)
    if blob.count("</data>") < 2 or "IGNORE PREVIOUS INSTRUCTIONS" not in blob:
        errors.append("adversarial breakout strings missing")
    if attack["expected_regression"]["unauthorized_instructions_in_fact_ledger"] != 0:
        errors.append("adversarial expected propagation")


def check_media(errors: list[str]) -> list[str]:
    notes = []
    media = FIX / "synthetic_media"
    specs = {
        "911_8khz_distorted.wav": 8000,
        "911_spoken_pii.wav": 16000,
    }
    for name, rate in specs.items():
        path = media / name
        size = path.stat().st_size
        with wave.open(str(path), "rb") as handle:
            channels = handle.getnchannels()
            width = handle.getsampwidth()
            actual = handle.getframerate()
            frames = handle.getnframes()
        duration = frames / actual
        if channels != 1 or width != 2 or actual != rate:
            errors.append(f"{name} wav format {channels} {width} {actual}")
        if not (2 <= duration <= 10) or size >= 500 * 1024:
            errors.append(f"{name} size/duration {size} {duration}")
        notes.append(f"PASS media {name} bytes={size} duration_s={duration:.3f} rate={actual}")
        if name.startswith("911_8khz"):
            handle_samples = wave.open(str(path), "rb").readframes(frames)
            samples = struct.unpack("<" + "h" * frames, handle_samples)
            clipped = sum(1 for sample in samples if abs(sample) >= 32767)
            if clipped < frames * 0.01:
                errors.append(f"{name} not distorted/clipped")
    body = media / "bodycam_440hz_music_042profanity.mp4"
    size = body.stat().st_size
    rate, samples = read_mp4_pcm(body)
    duration = len(samples) / rate
    if rate != 8000 or not (2 <= duration <= 10) or size >= 500 * 1024:
        errors.append(f"bodycam mp4 size/duration {size} {duration} {rate}")
    power_440 = goertzel_power(samples, 440, rate)
    power_180 = goertzel_power(samples, 180, rate)
    if power_440 < power_180 * 10:
        errors.append("bodycam mp4 missing 440 Hz music bed")
    notes.append(f"PASS media bodycam_440hz_music_042profanity.mp4 bytes={size} duration_s={duration:.3f} rate={rate} coding=sowt")
    transcript = load_json(media / "911_spoken_pii.transcript.json")
    if "406-555-0142" not in transcript["transcript"] or "18 Fixture Lane" not in transcript["transcript"]:
        errors.append("spoken pii transcript")
    note = load_json(media / "media_notes.json")
    if "sowt" not in note["mp4_tooling"] or "ffmpeg" not in note["mp4_tooling"]:
        errors.append("mp4 tooling note")
    if note["profanity_source_timeline_ms"]["start_ms"] != 42000:
        errors.append("profanity note")
    if note["no_live_download"] is not True:
        errors.append("download note")
    return notes


def main() -> int:
    errors: list[str] = []
    schema_path = FIX / "golden_pack.schema.json"
    schema = load_json(schema_path)
    lines = [f"schema: {schema_path.relative_to(ROOT).as_posix()}"]
    for pack_id in PACKS:
        path = FIX / "golden_manifests" / pack_id / "pack.json"
        raw = path.read_text(encoding="utf-8")
        pack = json.loads(raw)
        before = len(errors)
        validate_schema(pack, schema, pack_id, errors)
        check_pack(pack, raw, errors)
        if len(errors) == before:
            heroes = sum(1 for scene in pack["scenes"] if scene["visual_engine"] == "FLOW_HERO_VIDEO")
            lines.append(
                f"PASS {pack_id} scenes={len(pack['scenes'])} anchors={len(pack['spatial_anchors'])} "
                f"heroes={heroes} runtime_ms=780000/340000/80000"
            )
        else:
            lines.append(f"FAIL {pack_id}")
    before = len(errors)
    check_recorded(errors)
    if len(errors) == before:
        lines.append("PASS recorded_apis youtube_videos_list.json courtlistener_search.json muckrock_foia_requests.json adversarial_prompt_injection.json")
    else:
        lines.append("FAIL recorded_apis")
    before = len(errors)
    try:
        lines.extend(check_media(errors))
    except Exception as exc:
        errors.append(f"media exception: {exc}")
    if len(errors) != before:
        lines.append("FAIL synthetic_media")
    else:
        lines.append("PASS keyframes_and_plates crimson_pixels=0")
    print("GOLDEN FIXTURE VALIDATOR v4")
    for line in lines:
        print(line)
    if errors:
        print(f"RESULT fail={len(errors)}")
        for error in errors:
            print(f"ERROR {error}")
        return 1
    print("RESULT pass=3 packs + recorded_apis + synthetic_media fail=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
