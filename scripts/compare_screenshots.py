#!/usr/bin/env python3
"""
Compare two screenshots and generate basic visual-diff artifacts.

Usage:
    python compare_screenshots.py reference.png candidate.png --out-dir diff-output
    python compare_screenshots.py reference.png candidate.png --out-dir diff-output --fit

Best results come from comparing images already captured at the same dimensions.
Use --fit only as a fallback diagnostic when the candidate screenshot size is slightly off.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

try:
    from PIL import Image, ImageChops, ImageOps, ImageStat
except Exception as exc:  # pragma: no cover - environment dependent
    raise SystemExit(
        "This script requires Pillow. Install it with `pip install pillow` "
        "or compare screenshots manually."
    ) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare two screenshots and save diff artifacts.")
    parser.add_argument("reference", type=Path, help="Path to the reference screenshot.")
    parser.add_argument("candidate", type=Path, help="Path to the candidate/implementation screenshot.")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("screenshot-diff-output"),
        help="Directory where diff artifacts will be written.",
    )
    parser.add_argument(
        "--fit",
        action="store_true",
        help="Resize the candidate image to the reference size before comparing. "
             "Use only as a fallback when exact-size capture is not available.",
    )
    parser.add_argument(
        "--enhance-factor",
        type=float,
        default=4.0,
        help="Contrast boost for the enhanced diff image. Default: 4.0",
    )
    return parser.parse_args()


def ensure_exists(path: Path, label: str) -> None:
    if not path.exists():
        raise SystemExit(f"{label} does not exist: {path}")
    if not path.is_file():
        raise SystemExit(f"{label} is not a file: {path}")


def load_image(path: Path) -> Image.Image:
    with Image.open(path) as img:
        return img.convert("RGBA")


def resize_if_needed(reference: Image.Image, candidate: Image.Image, fit: bool) -> tuple[Image.Image, bool]:
    if candidate.size == reference.size:
        return candidate, False
    if not fit:
        raise SystemExit(
            "Images are different sizes. Capture the candidate screenshot at the same size as the "
            f"reference ({reference.size[0]}x{reference.size[1]}) or rerun with --fit for a fallback comparison."
        )
    resized = candidate.resize(reference.size, Image.LANCZOS)
    return resized, True


def compute_metrics(diff_rgb: Image.Image) -> dict:
    stat = ImageStat.Stat(diff_rgb)
    mean_per_channel = stat.mean
    rms_per_channel = stat.rms

    mean_abs = sum(mean_per_channel) / len(mean_per_channel)
    rms_avg = sum(rms_per_channel) / len(rms_per_channel)

    normalized_mean_abs_pct = (mean_abs / 255.0) * 100.0
    normalized_rms_pct = (rms_avg / 255.0) * 100.0

    # Approximate count of pixels with any visible difference.
    grayscale = diff_rgb.convert("L")
    hist = grayscale.histogram()
    total_pixels = diff_rgb.width * diff_rgb.height
    identical_pixels = hist[0]
    changed_pixels = total_pixels - identical_pixels
    changed_pct = (changed_pixels / total_pixels) * 100.0

    return {
        "mean_abs_diff_per_channel": [round(x, 4) for x in mean_per_channel],
        "rms_diff_per_channel": [round(x, 4) for x in rms_per_channel],
        "mean_abs_diff": round(mean_abs, 4),
        "rms_diff": round(rms_avg, 4),
        "normalized_mean_abs_diff_pct": round(normalized_mean_abs_pct, 4),
        "normalized_rms_diff_pct": round(normalized_rms_pct, 4),
        "changed_pixels": changed_pixels,
        "total_pixels": total_pixels,
        "changed_pixel_pct": round(changed_pct, 4),
    }


def boost_diff(diff_rgb: Image.Image, factor: float) -> Image.Image:
    # Auto-contrast first, then boost intensity for easier inspection.
    auto = ImageOps.autocontrast(diff_rgb)
    return auto.point(lambda v: max(0, min(255, int(v * factor))))


def write_report(path: Path, report: dict) -> None:
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")


def write_text_summary(path: Path, report: dict) -> None:
    lines = [
        f"reference_path: {report['reference_path']}",
        f"candidate_path: {report['candidate_path']}",
        f"reference_size: {report['reference_size']}",
        f"candidate_original_size: {report['candidate_original_size']}",
        f"compared_size: {report['compared_size']}",
        f"candidate_resized: {report['candidate_resized']}",
        "",
        f"mean_abs_diff: {report['metrics']['mean_abs_diff']}",
        f"normalized_mean_abs_diff_pct: {report['metrics']['normalized_mean_abs_diff_pct']}%",
        f"rms_diff: {report['metrics']['rms_diff']}",
        f"normalized_rms_diff_pct: {report['metrics']['normalized_rms_diff_pct']}%",
        f"changed_pixel_pct: {report['metrics']['changed_pixel_pct']}%",
        "",
        "Artifacts:",
        f"- overlay.png",
        f"- diff_raw.png",
        f"- diff_enhanced.png",
        "",
        "Interpretation:",
        "- Lower diff values are generally better, but visual judgment still matters more than the metric.",
        "- Review the enhanced diff image to find concentrated mismatch regions.",
        "- A low global diff can still hide an important missing icon or typography mismatch.",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    ensure_exists(args.reference, "Reference image")
    ensure_exists(args.candidate, "Candidate image")
    args.out_dir.mkdir(parents=True, exist_ok=True)

    reference = load_image(args.reference)
    candidate_original = load_image(args.candidate)
    candidate, resized = resize_if_needed(reference, candidate_original, args.fit)

    diff_rgba = ImageChops.difference(reference, candidate)
    diff_rgb = diff_rgba.convert("RGB")
    enhanced = boost_diff(diff_rgb, args.enhance_factor)
    overlay = Image.blend(reference.convert("RGB"), candidate.convert("RGB"), 0.5)

    metrics = compute_metrics(diff_rgb)

    report = {
        "reference_path": str(args.reference),
        "candidate_path": str(args.candidate),
        "reference_size": list(reference.size),
        "candidate_original_size": list(candidate_original.size),
        "compared_size": list(candidate.size),
        "candidate_resized": resized,
        "metrics": metrics,
    }

    overlay.save(args.out_dir / "overlay.png")
    diff_rgb.save(args.out_dir / "diff_raw.png")
    enhanced.save(args.out_dir / "diff_enhanced.png")

    write_report(args.out_dir / "report.json", report)
    write_text_summary(args.out_dir / "report.txt", report)

    print(f"Saved artifacts to: {args.out_dir}")
    print(f"Compared size: {candidate.size[0]}x{candidate.size[1]}")
    print(f"Candidate resized: {resized}")
    print(f"Mean absolute diff: {metrics['mean_abs_diff']} ({metrics['normalized_mean_abs_diff_pct']}%)")
    print(f"RMS diff: {metrics['rms_diff']} ({metrics['normalized_rms_diff_pct']}%)")
    print(f"Changed pixels: {metrics['changed_pixels']} / {metrics['total_pixels']} ({metrics['changed_pixel_pct']}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
