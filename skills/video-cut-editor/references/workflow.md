# Video Cut Editor Workflow

Use this when editing lecture or screen-recording footage with retake markers.

## Core Model

Timeline boundaries come from audio evidence, not STT.

- Marker detection finds the intentional edit point.
- VAD/silence analysis finds speech starts, speech ends, and safe padding.
- STT is semantic evidence for deciding which side of the marker to remove.
- Join maps are the source of truth for post-render waveform QA.
- A marker is not a command to delete the whole previous VAD speech segment.
- Mixed marker+silence work is marker-first, silence-second, render-once.
- Rendering happens once from the original source timeline.

## Workflow

1. Analyze the original media.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/video_cut_workflow.py analyze INPUT.mp4
```

2. Read the generated `review.md`.

3. Classify each marker and fill `remove_intervals` in `cut-plan.json`.

4. Audit the plan.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/audit_cut_plan.py cut-plan.json
```

5. Dry-run render once.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/video_cut_workflow.py render cut-plan.json --dry-run
```

6. Render the reviewed plan. The final media stays at `OUTPUT.mp4`; generated evidence goes under `OUTPUT.video-cut-artifacts/` by default.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/video_cut_workflow.py render cut-plan.json --output OUTPUT.mp4
```

7. Audit rendered waveform continuity at actual joins only.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/audit_waveform_joins.py OUTPUT.mp4 OUTPUT.video-cut-artifacts/OUTPUT.join-map.json
```

8. For multi-file deliverables, spot-check marker-risk joins before merge.

9. Merge only the edited files that passed spot-check and decode verification. The final media stays at `MERGED.mp4`; merge evidence goes under `MERGED.video-cut-artifacts/` by default.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/merge_reviewed_outputs.py --output MERGED.mp4 --spot-check-summary spot-check-summary.json PART1.edited.mp4 PART2.edited.mp4
```

10. Audit the merged waveform joins against the merged join map.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/audit_waveform_joins.py MERGED.mp4 MERGED.video-cut-artifacts/MERGED.join-map.json
```

11. After delivery is accepted, dry-run cleanup before deleting generated evidence/log artifacts.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/cleanup_artifacts.py WORKDIR
```

## Request Modes

- Marker only: review markers, fill marker intervals, audit, render once.
- Silence only: run silence dry-run/sample, confirm padding, render once.
- Marker + silence: review markers first in `marker-cut-plan.reviewed.json`, audit that marker plan, run `scripts/build_mixed_cut_plan.py --marker-plan marker-cut-plan.reviewed.json`, audit the generated `cut-plan.json`, render once.

## Marker Decisions

Use these labels in the plan reason text.

- `full_retake`: failed clause or sentence before marker is repeated after marker.
- `local_correction`: only the failed word or short phrase before marker should be removed.
- `cut_before_marker`: alias for `full_retake`; use it only when the retake repeats the whole clause or sentence.
- `cut_after_marker`: marker is followed by filler before the real retake.
- `skip`: marker is accidental or no retake exists.
- `needs_manual`: evidence is ambiguous; do not auto-render.

## Marker Review Rules

- Compare the transcript before and after the marker before choosing a cut type.
- If the post-marker transcript repeats only a word or short phrase, use `local_correction` and cut only that failed phrase.
- If the post-marker transcript repeats the whole clause or sentence, use `full_retake` and cut from the semantic start of the failed take.
- Do not use the start of the previous VAD speech segment as the cut start unless the whole segment is a failed retake.
- If the marker is near the end and no valid retake follows, use `skip` instead of cutting to EOF.
- For every non-silence marker interval, inspect a join preview around the kept-left and kept-right boundary before final render.
- When silence removal is also required, decide marker intervals first; then add silence intervals that remain after those marker cuts.
- Store the final mixed plan in original-source seconds even when silence was judged after subtracting marker intervals.

## Render Monitoring

- `video_cut_workflow.py render` creates `<output-stem>.video-cut-artifacts/<output-stem>.render.log` unless `--log-file` is set.
- The default render join map is `<output-stem>.video-cut-artifacts/<output-stem>.join-map.json` unless `--join-map` is set.
- For long renders, check the render log, `pgrep`/`ps`, and output file size before deciding the job is stuck.
- If ffmpeg fails, report the log path with the error; the log is the source for the failing command and tail output.

## Post-Render Spot Check

- `verify: ok` confirms structure and decode, not semantic cut quality.
- Waveform QA must read `*.join-map.json` and check only actual edit/merge joins.
- Do not use whole-file waveform discontinuity scans to find edit problems; natural speech dynamics create false positives.
- For files with marker cuts, spot-check at least one risky join with STT or playback before reporting done.
- Prioritize joins with `local_correction`, `intentional_long_cut`, tail markers, or earlier failed cuts.
- Sample at least one previous failure area when this run was triggered by a bad cut.
- Prefer the longest `full_retake` intervals when marker count is high.
- Include the last marker interval when tail markers exist.
- Store checked joins in `spot-check-summary.json` when multiple files are being merged.

## Final QA and Merge

- Merge is a final delivery step, not a substitute for per-file review.
- Do not merge files with marker cuts until representative risky joins pass STT or playback spot-check.
- Use `scripts/merge_reviewed_outputs.py` for multi-file deliverables; it prints input preflight, writes a merge log, writes a QA report, and verifies the merged output.
- The default merge log, join map, and QA report are written under `<merged-stem>.video-cut-artifacts/` unless explicit paths are provided.
- Keep the merged `*.join-map.json`; it is required for waveform QA after merge.
- Prefer concat stream copy when stream shapes match.
- Use re-encode fallback only when the helper reports compatible stream geometry and audio layout.
- After merge, confirm decode verification and duration close to the sum of reviewed inputs.
- Spot-check the first and last 10 seconds of the merged output before reporting final delivery.
- Include `--merged-spot-check` when the head/tail spot-check has a JSON result.
- Read the merge warning summary; timestamp warnings can be acceptable only when duration and decode verification pass.

## QA Report

- Use the helper-generated `*.qa-report.md` in the artifact folder as the standard final QA report.
- The report should include input durations, stream preflight, marker-risk spot-check count, merged head/tail spot-check count, merge warnings, expected duration, actual duration, and decode result.
- If a spot-check JSON is not available, mark that report item as `not provided` instead of inventing a result.

## Cleanup

- Cleanup is a post-delivery step after the edited or merged media is confirmed.
- New render/merge 부산물은 `<output-stem>.video-cut-artifacts/`에 모은다.
- Dry-run cleanup first.
- Delete generated evidence/log/workspace artifacts only after reviewing the candidate list.
- Preserve source media, `*.edited.mp4`, and `*.merged.mp4` by default.
- Use `scripts/cleanup_artifacts.py WORKDIR --delete` only after the dry-run candidate list is correct.

## Safety Rules

- Do not render a marker-based edit from an empty or unreviewed plan.
- Do not chain edits through intermediate renders.
- Do not merge before marker-risk spot-checks pass.
- Do not cleanup before final media exists and passes decode verification.
- Do not report waveform QA from a final MP4 alone unless the checked target list came from a join map.
- Do not use STT timestamps as final cut boundaries.
- Do not let broad marker intervals pass audit unless the reason says `full_retake` or `intentional_long_cut` and the review evidence supports it.
- Keep old outputs in an archive folder instead of overwriting them.
- Report when the render is re-encoded; exact trim/concat is not bitstream lossless.
