# Cut Plan Schema

`video_cut_workflow.py render` consumes this JSON shape.

```json
{
  "source": "/absolute/path/input.mp4",
  "output": "/absolute/path/output.mp4",
  "status": "reviewed",
  "silence_policy": {
    "source": "ffmpeg_silencedetect",
    "min_duration": 1.0,
    "padding": 0.3
  },
  "remove_intervals": [
    {
      "start": 12.34,
      "end": 18.9,
      "reason": "cut_before_marker: failed wording before retake"
    }
  ]
}
```

Rules:

- Times are seconds on the original source timeline.
- An empty `remove_intervals` is a reviewed preserve-all decision; render copies the source and writes a zero-join map.
- Before approving an empty plan with no detected markers, review the full-source transcript and visual timeline because unmarked retakes remain possible.
- Intervals must not overlap.
- `start` must be lower than `end`.
- Keep reasons short but explicit enough to audit later.
- Use `local_correction` for short failed word or phrase cuts.
- Use `full_retake` or `cut_before_marker` only when the whole failed clause or sentence is repeated after the marker.
- Use `skip` in review notes, not `remove_intervals`, when a marker has no valid retake.
- Use `status: reviewed` after the plan has been checked by a person or agent.
- Set a programmatically transformed plan back to `status: draft`; audit and preview that exact plan before marking it reviewed again.
- Run `scripts/audit_cut_plan.py PLAN.json` before render and resolve findings instead of bypassing them.
- Automatic silence intervals must include `silence_policy` and their `silence_sources`; old VAD-complement plans must fail audit.
- Visual-safe silence splits must remain inside their explicit `silence_sources` and preserve that evidence on every replacement interval.
- Render writes `OUTPUT.join-map.json` by default; keep it for waveform join QA.
