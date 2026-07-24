# Apple-only regression benchmark

This benchmark compares two Apple `SpeechTranscriber` runs. It never invokes Whisper or another recognizer, and it does not commit audio or reference transcripts.

## 목차

- [Private corpus workflow](#private-corpus-workflow)
- [Release command](#release-command)
- [Local manifest schema v1](#local-manifest-schema-v1)
- [Run directory](#run-directory)
- [Metrics and gates](#metrics-and-gates)

## Private corpus workflow

Prepare a metadata-only input under a private directory. `scaffold` hashes the explicitly listed audio, requires unique hashes and both splits, copies only the documented metadata fields, and does not create gold text or either sign-off file.

```json
{
  "schema_version": 1,
  "recordings": [
    {
      "id": "calibration-01",
      "split": "calibration",
      "environment": "iphone-table",
      "speaker_configuration": "two-speakers",
      "audio_file": "/private/audio/calibration-01.m4a",
      "result_file": "recordings/calibration-01.json"
    },
    {
      "id": "evaluation-01",
      "split": "evaluation",
      "environment": "meeting-room",
      "speaker_configuration": "single-speaker",
      "audio_file": "/private/audio/evaluation-01.m4a",
      "result_file": "recordings/evaluation-01.json"
    }
  ]
}
```

```bash
install -m 600 /dev/null ~/.config/stt/benchmarks/empty-context.txt

python3 skills/shared/stt/scripts/benchmark.py scaffold \
  --input ~/.config/stt/benchmarks/recordings.json \
  --output ~/.config/stt/benchmarks/manifest.json

python3 skills/shared/stt/scripts/benchmark.py capture \
  --manifest ~/.config/stt/benchmarks/manifest.json \
  --binary /path/to/apple-stt \
  --vocab-file ~/.config/stt/benchmarks/empty-context.txt \
  --run-dir ~/.voice-memos/benchmarks/runs/no-context

python3 skills/shared/stt/scripts/benchmark.py capture \
  --manifest ~/.config/stt/benchmarks/manifest.json \
  --binary /path/to/apple-stt \
  --vocab-file ~/.config/stt/benchmarks/common-context.txt \
  --run-dir ~/.voice-memos/benchmarks/runs/context-100
```

Native analysis capture always passes a generated vocab file to `apple-stt`. Use an explicit empty `--vocab-file` for a no-context run. Without the command-level override, native capture combines the recording's optional `vocab_file` and `context`; the current native binary does not load ambient `~/.config/stt/vocab.txt`. A command-level `--vocab-file` completely replaces every recording context, so no-context and common-context runs retain the same manifest hash. Context is never derived from a draft or gold transcript, and any term dropped by Apple's 100-term/input limits aborts the capture. The deployed legacy exception is documented below.

The default private roots are `~/.config/stt/benchmarks` for manifests and `~/.voice-memos/benchmarks` for runs. `--allow-root` explicitly selects another root. Existing controlled directories must already belong to the current user with mode `0700`; the tool rejects rather than repairs an insecure directory. New controlled child directories use mode `0700`, files use `0600`, symlink or irregular path components are rejected, and capture refuses an existing run directory. Success output contains counts and hashes, not private paths or transcript text.

To freeze the currently deployed legacy binary as a production baseline, explicitly provide the deployed vocab snapshot and opt into the benchmark-only adapter:

```bash
python3 skills/shared/stt/scripts/benchmark.py capture \
  --legacy-json \
  --manifest ~/.config/stt/benchmarks/manifest.json \
  --binary ~/.local/bin/apple-stt \
  --vocab-file ~/.config/stt/vocab.txt \
  --run-dir ~/.voice-memos/benchmarks/runs/deployed-legacy
```

`--legacy-json` accepts only the installed `--json` array contract and reproduces the deployed Voice Memos call shape: the legacy binary loads the ambient vocab and Voice Memos passes the same frozen file explicitly. Capture rejects a missing or different ambient file and verifies both snapshots before and after every subprocess. The adapter records `input_mode: "ambient_plus_explicit_same_file"`, separate ambient and explicit hashes and counts, their effective sum, and aggregate duplicate counts; the config fingerprint binds the complete profile. With the current 611-entry deployed file this is 611 ambient + 611 explicit = 1,222 configured hints. The legacy output cannot reveal which terms Apple actually applied, so provenance keeps `applied_terms_observable: false`. The adapter also binds its source hash, requires valid non-empty timed segments, deliberately omits strict Voice Memos evidence fields, and is accepted only by the exact `benchmark.py` evaluator source that captured it.

## Release command

```bash
python3 skills/shared/stt/scripts/benchmark.py compare \
  --manifest ~/.config/stt/benchmarks/manifest.json \
  --baseline-dir ~/.voice-memos/benchmarks/runs/<baseline> \
  --candidate-dir ~/.voice-memos/benchmarks/runs/<candidate> \
  --profile transcription \
  --expect-context-only-change \
  --gate
```

The command writes `report.json` and `report.md` atomically in the candidate run directory. `--gate` exits `1` for `fail` or `insufficient_data`; malformed input exits `2`. Reports contain IDs and aggregate metrics, not transcript text.

Use `--profile transcription` for Gate 1. It keeps corpus, human-gold, fingerprints, bundle sign-off, CER, named-term, and changed/alignment sign-off gates while omitting correction-selector denominators and thresholds. Add `--expect-context-only-change` only for native strict no-context versus context A/B; it requires two strict runs with the same binary, macOS build, locale/model state, and a different bound config. Legacy adapter runs cannot satisfy this relation. Omit it when comparing the deployed legacy binary with a new candidate binary. The default `--profile full` retains every Gate 2 review-selector and optional Claude gate.

## Local manifest schema v1

Keep the manifest and referenced audio outside the shared repository. Use at least six `calibration` and six held-out `evaluation` recordings. Each split must cover at least three capture environments, two speaker configurations, and 50 named-term occurrences; the `full` profile additionally requires 50 `replace` correction targets. Every recording requires a unique source audio hash, so a copy cannot pad a split or leak into both splits.

```json
{
  "schema_version": 1,
  "recordings": [
    {
      "id": "calibration-01",
      "split": "calibration",
      "environment": "iphone-table",
      "speaker_configuration": "two-speakers",
      "audio_file": "/private/audio/calibration-01.m4a",
      "audio_sha256": "<lowercase sha256>",
      "result_file": "recordings/calibration-01.json",
      "utterances": [
        {"id": "g001", "start_ms": 0, "end_ms": 2100, "text": "exact reference text"}
      ],
      "named_terms": [
        {"utterance_id": "g001", "term": "short spoken term"}
      ],
      "required_phrases": [
        {"utterance_id": "g001", "text": "required phrase"}
      ],
      "correction_targets": [
        {
          "id": "t001",
          "utterance_id": "g001",
          "start_byte": 0,
          "end_byte": 5,
          "label": "replace",
          "allowed_replacements": ["gold replacement"]
        }
      ]
    }
  ]
}
```

Target offsets are half-open UTF-8 byte offsets in the exact reference utterance. Suggestion offsets remain hypothesis-local and are never compared directly with these values. `label` is `replace` or `no_change`; only `replace` targets count toward candidate error recall and its minimum denominator.

After a person verifies every gold utterance, create `gold-signoff.json` beside the finalized manifest. The tool never creates it.

```json
{
  "schema_version": 1,
  "manifest_sha256": "<canonical finalized manifest sha256>",
  "recording_ids": ["calibration-01", "evaluation-01"],
  "human_verified": true
}
```

## Run directory

Each native `result_file` is an immutable Apple analysis schema-v1 object with `engine: "apple-speech-transcriber"`, source hash/duration, and timed segments. The evaluator binds every native result's engine version, locale, context fingerprint, and result hash to `run.json`; it also recomputes the config fingerprint. Every run declares exactly one `result_mode` (`strict` or `legacy`), and every result must match it, so adapter and native evidence cannot be mixed. Legacy adapter results use the separate benchmark-only contract described above. The directory also contains `run.json`:

```json
{
  "schema_version": 1,
  "result_mode": "strict",
  "manifest_sha256": "<canonical manifest sha256>",
  "fingerprints": {
    "binary_sha256": "...",
    "macos_build": "...",
    "locale": "ko-KR",
    "config_sha256": "...",
    "locale_model_state": "installed"
  },
  "frozen_thresholds": {
    "candidate_error_recall_min": 0.8,
    "candidate_segment_ratio_max": 0.1,
    "candidate_duration_ratio_max": 0.2,
    "candidate_character_ratio_max": 0.2,
    "review_minutes_per_audio_hour_max": 15,
    "calibration_split_sha256": "<canonical calibration split sha256>"
  },
  "recordings": {
    "calibration-01": {
      "candidate_segment_ids": ["s0001"],
      "review_seconds": {"s0001": 12.4},
      "processing_seconds": 3.2,
      "peak_memory_mb": 188,
      "auto_applied_count": 0,
      "wrong_approved_count": 0,
      "residual_error_count": 1,
      "context_fingerprint": "...",
      "result_sha256": "..."
    }
  }
}
```

`macos_build` must be a non-empty string and `locale_model_state` must be `installed`. The bound `config_sha256` covers locale, `result_mode`, normalized result paths, and each recording's context or legacy vocab profile fingerprint.

Choose duration, character, and review-time ceilings from calibration, then freeze them. The evaluator verifies the calibration split hash so evaluation results cannot be used to retune thresholds.

`signoff.json` records explicit review of all changed evaluation segments and any unmapped or tied temporal component:

```json
{
  "schema_version": 1,
  "manifest_sha256": "<canonical manifest sha256>",
  "baseline_bundle_sha256": "<run.json plus baseline result files>",
  "candidate_bundle_sha256": "<run.json plus candidate result files>",
  "changed_segment_ids": ["evaluation-01:s0001"],
  "alignment_issue_ids": ["candidate:evaluation-01:c0002"]
}
```

The tool never authors `signoff.json`. All three hashes must match the exact evaluated evidence bundle; changing a run or manifest invalidates the sign-off. Read the exact expected values from `report.json.signoff_binding` after an initial non-passing comparison.

## Metrics and gates

- Temporal scoring uses connected many-to-many overlap components. Ordered gold and Apple text is concatenated inside each component. Unmapped or tied ranges require sign-off.
- Surface CER uses Unicode NFC plus collapsed whitespace. Content CER additionally removes Unicode punctuation and whitespace.
- Named-term recall scores each manifest occurrence in its gold temporal component. Omissions count required phrases absent after content normalization.
- Evaluation deltas use deterministic paired per-recording bootstrap 95% intervals. Recall proportions also include Wilson intervals.
- Content CER's upper delta bound must be at most `0.005`; named-term recall's lower delta bound must be at least `0`; at least one point estimate must improve.
- Candidate error recall must be at least `0.8`, candidate segment ratio at most `0.1`, and the other candidate ratios must satisfy the frozen calibration limits.
- Active review seconds are capped at 120 seconds per candidate and reported as minutes per audio hour.
- Missing required recordings, environments, speaker configurations, targets, named occurrences, thresholds, fingerprints, or metric denominators is `insufficient_data`, never pass.
- Any automatic application, wrong approved correction, unsigned changed segment, or unsigned alignment issue fails the release gate.

Claude suggestion evaluation is optional for the Apple-only release. To request it, add `"requested_features": ["claude_suggestions"]`, complete `claude_fingerprints` in `run.json`, and attach per-recording suggestion results. It then requires at least 30 validated non-abstaining evaluation suggestions, precision at least `0.8`, and invalid/refusal rate at most `0.1`. Without that request, a missing Claude denominator does not block Apple transcription.

Each suggestion entry uses `status: suggested|abstain|invalid|refusal|transport_failure`. A `suggested` entry also carries `target_id`, hypothesis-side `alignment: "aligned"|"unaligned"`, `replacement`, and `approved`. It is a true positive only when the aligned target is `replace` and the content-normalized replacement matches one of that target's allowed replacements. Other valid non-abstaining suggestions are false positives.
