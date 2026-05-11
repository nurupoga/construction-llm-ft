#!/usr/bin/env python3
"""Plot Baseline vs Fine-tuned accuracy comparison for 宅建士 PoC.

Reads two evaluation JSON files (baseline & fine-tuned) and produces:
  1. results/score_comparison.png   -- bar chart (PNG)
  2. results/score_comparison.json  -- structured summary with flipped IDs

Both input JSON files share the schema (excerpt):
    {
      "run_id": "...",
      "model": "Qwen/Qwen2.5-7B-Instruct",
      "adapter": null | "checkpoints/...",
      "eval_set": "takken_2025",
      "num_total": 50,
      "num_correct": 28,
      "accuracy": 0.56,
      "score": "28/50",
      "per_question": [
        {"id": "takken_2025_q001", "correct": true | false, ...}
      ],
      "config": {...}
    }

Usage:
    python3 scripts/plot_score_comparison.py
    python3 scripts/plot_score_comparison.py --baseline path/to/b.json --ft path/to/f.json --output-dir results/

Constraints:
    - matplotlib only (numpy/json are stdlib-adjacent)
    - Falls back to default font if Hiragino Sans is unavailable
"""

from __future__ import annotations

import argparse
import json
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")  # headless-safe
import matplotlib.font_manager as fm  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402


# ---------------------------------------------------------------------------
# Font setup (macOS Hiragino Sans preferred; fallback to default with warning)
# ---------------------------------------------------------------------------
def setup_japanese_font() -> bool:
    """Try to register a Japanese font. Return True if a CJK font is in use."""
    preferred = [
        "Hiragino Sans",
        "Hiragino Maru Gothic Pro",
        "Hiragino Kaku Gothic Pro",
        "Yu Gothic",
        "Noto Sans CJK JP",
        "IPAexGothic",
        "TakaoPGothic",
    ]
    available = {f.name for f in fm.fontManager.ttflist}
    for name in preferred:
        if name in available:
            plt.rcParams["font.family"] = name
            plt.rcParams["axes.unicode_minus"] = False
            return True
    warnings.warn(
        "Japanese font not found (tried: %s). Falling back to default font; "
        "Japanese characters may render as tofu." % ", ".join(preferred)
    )
    return False


# ---------------------------------------------------------------------------
# IO helpers
# ---------------------------------------------------------------------------
def load_eval(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_subtitle(ft_config: dict[str, Any] | None) -> str:
    """Render a subtitle line from the FT run config (best-effort)."""
    base_model = "Qwen2.5-7B-Instruct"
    if not ft_config:
        return base_model
    method = ft_config.get("method", "QLoRA")
    train_n = ft_config.get("train_size") or ft_config.get("num_train") or ft_config.get("train_examples")
    epoch = ft_config.get("epoch") or ft_config.get("num_epochs") or ft_config.get("epochs")
    lr = ft_config.get("lr") or ft_config.get("learning_rate")

    bits: list[str] = [base_model, method]
    if train_n is not None:
        bits.append(f"train={train_n}")
    if epoch is not None:
        bits.append(f"epoch={epoch}")
    if lr is not None:
        bits.append(f"lr={lr}")
    return ", ".join(bits)


# ---------------------------------------------------------------------------
# Core analysis
# ---------------------------------------------------------------------------
def diff_per_question(
    baseline: dict[str, Any], ft: dict[str, Any]
) -> tuple[list[str], list[str]]:
    """Return (flipped_correct, flipped_wrong) id lists by matching on `id`.

    flipped_correct: baseline wrong -> FT correct
    flipped_wrong  : baseline correct -> FT wrong (regression)
    """
    b_by_id = {q["id"]: bool(q.get("correct")) for q in baseline.get("per_question", []) if "id" in q}
    f_by_id = {q["id"]: bool(q.get("correct")) for q in ft.get("per_question", []) if "id" in q}
    common = sorted(set(b_by_id.keys()) & set(f_by_id.keys()))

    flipped_correct = [qid for qid in common if (not b_by_id[qid]) and f_by_id[qid]]
    flipped_wrong = [qid for qid in common if b_by_id[qid] and (not f_by_id[qid])]
    return flipped_correct, flipped_wrong


def compute_summary(baseline: dict[str, Any], ft: dict[str, Any]) -> dict[str, Any]:
    b_acc = float(baseline["accuracy"])
    f_acc = float(ft["accuracy"])
    flipped_c, flipped_w = diff_per_question(baseline, ft)

    abs_gain_pp = (f_acc - b_acc) * 100.0
    rel_gain_pct = ((f_acc - b_acc) / b_acc * 100.0) if b_acc > 0 else None

    return {
        "baseline_accuracy": b_acc,
        "ft_accuracy": f_acc,
        "absolute_gain_pp": round(abs_gain_pp, 2),
        "relative_gain_pct": round(rel_gain_pct, 2) if rel_gain_pct is not None else None,
        "num_correct_baseline": int(baseline["num_correct"]),
        "num_correct_ft": int(ft["num_correct"]),
        "num_total": int(baseline.get("num_total", ft.get("num_total", 0))),
        "questions_flipped_correct": flipped_c,
        "questions_flipped_wrong": flipped_w,
        "baseline_run_id": baseline.get("run_id"),
        "ft_run_id": ft.get("run_id"),
        "eval_set": ft.get("eval_set", baseline.get("eval_set")),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------
def plot_comparison(
    baseline: dict[str, Any],
    ft: dict[str, Any],
    summary: dict[str, Any],
    output_png: Path,
    has_jp_font: bool,
) -> None:
    if has_jp_font:
        labels = ["Baseline (FT前)", "Fine-tuned (FT後)"]
        title = "宅建士試験 2025年度 (eval=50問) 正答率比較"
    else:
        labels = ["Baseline (pre-FT)", "Fine-tuned (post-FT)"]
        title = "Takken (Real Estate License) 2025 — Accuracy (eval=50)"

    subtitle = build_subtitle(ft.get("config"))

    b_acc = summary["baseline_accuracy"]
    f_acc = summary["ft_accuracy"]
    b_n = summary["num_correct_baseline"]
    f_n = summary["num_correct_ft"]
    total = summary["num_total"]

    fig, ax = plt.subplots(figsize=(8.0, 6.0), dpi=150)
    bar_colors = ["#7f7f7f", "#1f4e8c"]  # gray, dark blue (color-blind safe pair)
    xs = [0, 1]
    bars = ax.bar(xs, [b_acc, f_acc], color=bar_colors, width=0.55, edgecolor="black", linewidth=0.6)

    # Bar labels: "N/total (XX.X%)"
    for x, acc, ncorrect in zip(xs, [b_acc, f_acc], [b_n, f_n]):
        ax.text(
            x,
            acc + 0.02,
            f"{ncorrect}/{total}\n({acc * 100:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
        )

    # Improvement annotation (arrow between bar tops)
    abs_pp = summary["absolute_gain_pp"]
    rel = summary["relative_gain_pct"]
    diff_n = f_n - b_n
    sign = "+" if diff_n >= 0 else ""
    if has_jp_font:
        gain_label = f"{sign}{diff_n}問 / {sign}{abs_pp:.1f}%pt"
        if rel is not None:
            gain_label += f"  (相対 {sign}{rel:.1f}%)"
    else:
        gain_label = f"{sign}{diff_n} questions / {sign}{abs_pp:.1f}%pt"
        if rel is not None:
            gain_label += f"  (relative {sign}{rel:.1f}%)"

    arrow_color = "#1f4e8c" if diff_n >= 0 else "#a83232"
    y_arrow = max(b_acc, f_acc) + 0.12
    ax.annotate(
        "",
        xy=(1, f_acc + 0.005),
        xytext=(0, b_acc + 0.005),
        arrowprops=dict(arrowstyle="->", color=arrow_color, lw=2.0),
    )
    ax.text(
        0.5,
        y_arrow,
        gain_label,
        ha="center",
        va="bottom",
        fontsize=12,
        color=arrow_color,
        fontweight="bold",
    )

    # Axes
    ax.set_ylim(0.0, 1.0)
    ax.set_ylabel("Accuracy" if not has_jp_font else "正答率")
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=11)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.1f}"))
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)

    # Title + subtitle
    fig.suptitle(title, fontsize=14, fontweight="bold", y=0.98)
    ax.set_title(subtitle, fontsize=10, color="#444444", pad=12)

    fig.tight_layout(rect=[0, 0, 1, 0.94])
    output_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_png, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parent.parent
    default_results = repo_root / "results"

    p = argparse.ArgumentParser(
        description="Plot Baseline vs Fine-tuned accuracy comparison.",
    )
    p.add_argument(
        "--baseline",
        type=Path,
        default=default_results / "baseline_eval.json",
        help="Path to baseline eval JSON (default: results/baseline_eval.json)",
    )
    p.add_argument(
        "--ft",
        type=Path,
        default=default_results / "ft_eval.json",
        help="Path to fine-tuned eval JSON (default: results/ft_eval.json)",
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=default_results,
        help="Directory to write score_comparison.{png,json} (default: results/)",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    missing = [str(p) for p in (args.baseline, args.ft) if not p.is_file()]
    if missing:
        sys.stderr.write(
            "baseline_eval.json または ft_eval.json が見つかりません。"
            "Colab実行を待ってください\n"
            "  missing: " + ", ".join(missing) + "\n"
        )
        return 1

    baseline = load_eval(args.baseline)
    ft = load_eval(args.ft)

    summary = compute_summary(baseline, ft)
    has_jp = setup_japanese_font()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out_png = args.output_dir / "score_comparison.png"
    out_json = args.output_dir / "score_comparison.json"

    plot_comparison(baseline, ft, summary, out_png, has_jp_font=has_jp)

    with out_json.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"[ok] wrote {out_png}")
    print(f"[ok] wrote {out_json}")
    print(
        f"     baseline={summary['num_correct_baseline']}/{summary['num_total']} "
        f"({summary['baseline_accuracy'] * 100:.1f}%)  "
        f"ft={summary['num_correct_ft']}/{summary['num_total']} "
        f"({summary['ft_accuracy'] * 100:.1f}%)  "
        f"delta={summary['absolute_gain_pp']:+.1f}pp"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
