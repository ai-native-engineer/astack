# Video Cut Editor Workflow

Use this when editing lecture or screen-recording footage with retake markers.

## 목차

- Core Model
- Workflow
- Request Modes
- Marker Decisions
- Marker Review Rules
- Existing Output Preflight
- Render Monitoring
- Post-Render Spot Check
- Final QA and Merge
- QA Report
- Human Listening Review
- Cleanup
- Safety Rules

## Core Model

Timeline boundaries come from audio evidence, not STT.

- Marker detection finds the intentional edit point.
- VAD analysis helps review marker boundaries; automatic silence removal uses only explicit long silences from `silencedetect`.
- STT is semantic evidence for deciding which side of the marker to remove.
- Join maps are the source of truth for post-render waveform QA.
- Join maps are also the source of truth for post-render visual join QA.
- A marker is not a command to delete the whole previous VAD speech segment.
- Mixed marker+silence work is marker-first, silence-second, render-once.
- Rendering happens once from the original source timeline.

## Workflow

For a batch, build the source manifest from the user-provided originals before any search. Do not infer the batch with an unscoped `*.mp4` glob because preview, candidate, and artifact media can be mistaken for source footage.

1. Resolve the original media and requested output path. If the output name already exists, compare it with the current source and reviewed plan before reuse. An occupied name is not proof that it represents the current cut; preserve it unchanged and choose a distinct candidate path when provenance or compatibility is unclear.

2. Analyze the original media.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/video_cut_workflow.py analyze INPUT.mp4
```

3. Read the generated `review.md`.

If marker detection returns zero candidates, review a full-source transcript and the full visual timeline before choosing preserve-all. Zero detected markers do not prove there are no false starts or retakes.

4. Classify each marker and fill `remove_intervals` in `cut-plan.json`, or record a reviewed preserve-all decision with an empty list.

5. Audit the plan.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/audit_cut_plan.py cut-plan.json
```

6. Dry-run render once.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/video_cut_workflow.py render cut-plan.json --dry-run
```

7. Render the reviewed plan. The final media stays at `OUTPUT.mp4`; generated evidence goes under `OUTPUT.video-cut-artifacts/` by default.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/video_cut_workflow.py render cut-plan.json --output OUTPUT.mp4
```

8. Audit rendered waveform continuity at actual joins only. Enumerate the media's audio streams and run once per track with `0:a:N` FFmpeg stream specifiers.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/audit_waveform_joins.py OUTPUT.mp4 OUTPUT.video-cut-artifacts/OUTPUT.join-map.json --audio-track 0:a:0
```

`render`는 marker evidence가 있는 plan이면 최종본의 잔존 마커도 자동 검사하며, 검출 결과가 남으면 실패한다.

9. Score every rendered visual join and inspect every generated candidate strip.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/audit_visual_joins.py OUTPUT.mp4 OUTPUT.video-cut-artifacts/OUTPUT.join-map.json
```

10. For multi-file deliverables, spot-check marker-risk joins before merge.

11. Merge only the edited files that passed spot-check and decode verification. The final media stays at `MERGED.mp4`; merge evidence goes under `MERGED.video-cut-artifacts/` by default.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/merge_reviewed_outputs.py --output MERGED.mp4 --spot-check-summary spot-check-summary.json PART1.edited.mp4 PART2.edited.mp4
```

When re-encoding a bumper plus reviewed body, `--audio-bitrate auto` uses the highest input bitrate for each audio track. Use an explicit delivery target such as `--audio-bitrate 160k` when required.

12. Inspect the reported output audio bitrates. Keep a rejected merge at its distinct candidate path; archive it only with approval and never overwrite an occupied delivery name.

13. Audit the accepted merged output's waveform and visual joins against its merged join map.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/audit_waveform_joins.py MERGED.mp4 MERGED.video-cut-artifacts/MERGED.join-map.json --audio-track 0:a:0
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/audit_visual_joins.py MERGED.mp4 MERGED.video-cut-artifacts/MERGED.join-map.json
```

14. Re-run marker detection, risky-join spot-checks, and long-silence detection on the accepted final file.

15. Transcribe the accepted final file into the artifact folder. Any local STT works as long as it emits `[{start, end, text}]` JSON, `{"segments": [...]}`, or SRT.

```bash
ffmpeg -v error -y -i MERGED.mp4 -map 0:a:0 -ac 1 -ar 16000 /tmp/merged.wav
<your-local-stt> --json /tmp/merged.wav -o MERGED.video-cut-artifacts/MERGED.transcript.json
```

16. Build and open the 2x HTML review editor from the accepted final join map, feeding it that transcript. Add waveform `listen` or warning timestamps with repeatable `--point SECONDS:LABEL` options.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/build-listening-review.py MERGED.mp4 MERGED.video-cut-artifacts/MERGED.join-map.json --transcript MERGED.video-cut-artifacts/MERGED.transcript.json --open
```

17. Approve or reject every review point, complete the full-listen checkbox, export the JSON, move it into the final artifact folder, and validate it against the accepted media and join map.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/build-listening-review.py MERGED.mp4 MERGED.video-cut-artifacts/MERGED.join-map.json --validate MERGED.video-cut-artifacts/MERGED.listening-review.json
```

18. Only after the validator prints `review_status: approved`, copy the reviewed plan next to the final artifacts, then dry-run cleanup before deleting generated evidence/log artifacts.

```bash
cp WORKDIR/segments/*.analysis/*cut-plan.reviewed.json MERGED.video-cut-artifacts/plan/
python3 ${CLAUDE_PLUGIN_ROOT}/skills/video-cut-editor/scripts/cleanup_artifacts.py WORKDIR
```

## Request Modes

- Marker only: review markers, fill marker intervals, audit, render once.
- Silence only: run silence dry-run/sample, confirm padding, render once.
- Marker + silence: review markers first in `marker-cut-plan.reviewed.json`, audit that marker plan, run `scripts/build_mixed_cut_plan.py --marker-plan marker-cut-plan.reviewed.json`, audit the generated plan, preview that exact plan, then render once.

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
- A terminal or orchestration wrapper can return before its child encoder exits. Before `ffprobe`, decode QA, rename, or promotion, confirm the named `ffmpeg` process exited and the candidate output is no longer open with `lsof`.
- If ffmpeg fails, report the log path with the error; the log is the source for the failing command and tail output.

## Post-Render Spot Check

- `verify: ok` confirms structure and decode, not semantic cut quality.
- Treat editorial audio as `not reviewed` until a person listens; STT and waveform checks cannot approve natural cadence or clipped syllables.
- A waveform `listen` result stays unresolved after STT cross-check until a person listens.
- Waveform QA must read `*.join-map.json` and check only actual edit/merge joins.
- Waveform QA must cover every real audio stream with explicit `0:a:N` specifiers.
- Visual QA must score every actual edit/merge join and directly inspect every candidate strip.
- SSIM ranks visual candidates; it does not approve or reject editorial continuity by itself.
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
- Before stream-copy concat, prove codec parameter-set compatibility with a trial full decode. Matching codec, dimensions, fps, tag, and color metadata do not prove that HEVC streams concatenate safely.
- If the trial has timestamp, SPS, or decode errors, preserve the input bodies and re-encode the final concat instead.
- In re-encode mode, `auto` selects the highest reported input bitrate per audio track so a silent bumper cannot lower the body audio quality.
- Use `--audio-bitrate` when the delivery bitrate is fixed; `auto` rejects a large drop from the duration-weighted input estimate.
- Read the output audio bitrates from stdout and the QA report before accepting the merge.
- After merge, confirm decode verification and duration close to the sum of reviewed inputs.
- If a custom FFmpeg concat has no join map, store and inspect a frame capture around every external-clip boundary before calling visual QA complete.
- If the output is archived and re-rendered, discard its QA result and re-run final decode, per-track waveform, marker, visual, long-silence, and spot-check QA on the accepted file.
- After visual repair, re-run both visual join QA and long-silence detection.
- Spot-check the first and last 10 seconds of the merged output before reporting final delivery.
- Include `--merged-spot-check` when the head/tail spot-check has a JSON result.
- Read the merge warning summary; timestamp warnings can be acceptable only when duration and decode verification pass.

## QA Report

- Use the helper-generated `*.qa-report.md` in the artifact folder as the standard final QA report.
- The report should include input durations, stream preflight, marker-risk spot-check count, merged head/tail spot-check count, merge warnings, expected duration, actual duration, and decode result.
- The report should include the requested and actual output audio bitrates for every track.
- If a spot-check JSON is not available, mark that report item as `not provided` instead of inventing a result.

## Human Listening Review

- Technical QA does not approve cadence, clipped syllables, or perceived audio quality.
- After final technical QA, run `scripts/build-listening-review.py` with the accepted media and its join map; use `--help` for optional warning-derived points.
- The generator automatically includes source-file merge joins and reasons containing `marker`, `full_retake`, `local_correction`, `cut_before_marker`, `cut_after_marker`, `intentional_long_cut`, `repeated_take`, `abandoned_phrase`, or `self_correction`.
- Add waveform `listen`, merge warning, or previous-failure timestamps with `--point SECONDS:LABEL`; each jump starts four seconds before the target.
- Pass the final media's transcript with `--transcript JSON_OR_SRT` so every card shows what is said around its join. A duplicated or clipped sentence is caught by reading; playback alone needs the reviewer to notice it by ear.
- Each edit-join card also prints its source-timeline span, because a rejection is fixed in the cut plan, and that plan is written in source seconds rather than delivered-file seconds.
- Keep the video visible beside an independently scrollable marker list on wide screens; stack them on narrow screens.
- Highlight the marker matching the current playback position and show the current and next marker above the list.
- Merge manual and automatic review points at the same timestamp so one join is reviewed once while retaining the manual label.
- The HTML editor stores approval/rejection and notes locally and exports `video-cut-editor.listening-review.v1` JSON.
- Browser storage is working state, not durable approval evidence. Move the exported JSON into the final artifact folder.
- Run the same script with `--validate REVIEW_JSON`; it rejects pending items and stale media/join-map hashes.
- Treat `pending` as unfinished and `needs_revision` as a return to the reviewed plan/render workflow.
- Accept human listening only when validation prints `review_status: approved`.
- When the reviewer answers in conversation instead of exporting, write the JSON for them and record how the approval arrived in an `approval_source` field, so the file is never mistaken for a click-through review.
- Loading the page in a headless or agent-controlled browser verifies rendering, not delivery. Finish with the command that opens it in the reviewer's own browser, and confirm the front window actually holds that URL.
- If the page does not open or the video does not load, report its path and keep human approval pending.
- Preserve source, edited output, rejected output, logs, and QA evidence until that approval.

## Cleanup

- Cleanup is a post-delivery step after the edited or merged media is confirmed.
- New render/merge 부산물은 `<output-stem>.video-cut-artifacts/`에 모은다.
- Dry-run cleanup first.
- Delete generated evidence/log/workspace artifacts only after reviewing the candidate list.
- Preserve source media, `*.edited.mp4`, and `*.merged.mp4` by default.
- Use `scripts/cleanup_artifacts.py WORKDIR --delete` only after the dry-run candidate list is correct.
- Before removing a work directory wholesale, copy its reviewed cut plan into `<output-stem>.video-cut-artifacts/plan/`. That file is what re-renders the delivered cut from the source, and the cleanup script does not treat it as a candidate, so a directory-level delete takes it silently.
- Keep `<body-stem>.video-cut-artifacts/` in place while more merges are possible. Merging without it writes a join map holding only the bumper joins, and every waveform and visual audit run against that map silently checks two joins instead of all of them.

## Safety Rules

- Render an empty marker-based plan only as a reviewed preserve-all decision after full-source transcript and visual review.
- Do not chain edits through intermediate renders.
- Do not merge before marker-risk spot-checks pass.
- Do not cleanup before final media exists and passes decode verification.
- Do not report waveform QA from a final MP4 alone unless the checked target list came from a join map.
- Do not report visual continuity from decode verification, coarse contact sheets, or SSIM scores alone.
- Do not reuse QA from a rejected or superseded final render; evidence must match the accepted output file.
- Do not restore a whole long silence to repair one visual jump; split only reviewed `silence` intervals and review the new draft plan.
- Do not use STT timestamps as final cut boundaries.
- Do not let broad marker intervals pass audit unless the reason says `full_retake` or `intentional_long_cut` and the review evidence supports it.
- Preserve an occupied output in place unless replacement or archival is explicitly approved. Render a distinct candidate when the requested name is unavailable.
- Report when the render is re-encoded; exact trim/concat is not bitstream lossless.
