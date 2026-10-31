from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).parents[1] / "scripts" / "pyannote-chunks.py"
SPEC = importlib.util.spec_from_file_location("pyannote_chunks", SCRIPT)
chunks = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(chunks)


def seg(key: str, start: float, end: float, vector: list[float] | None) -> dict:
    row = {"key": key, "start": start, "end": end}
    if vector is not None:
        row["embedding"] = vector
    return row


class PlanTest(unittest.TestCase):
    def test_short_recording_is_one_chunk(self) -> None:
        self.assertEqual(chunks.plan_chunks([[0.0, 800.0]], 850.0), [[0.0, 850.0]])

    def test_cut_lands_in_longest_pause_near_target(self) -> None:
        speech = [[0.0, 560.0], [561.0, 650.0], [653.0, 1300.0]]
        self.assertEqual(chunks.plan_chunks(speech, 1300.0), [[0.0, 651.5], [651.5, 1300.0]])

    def test_no_pause_near_target_cuts_at_target(self) -> None:
        self.assertEqual(chunks.plan_chunks([[0.0, 1300.0]], 1300.0), [[0.0, 600.0], [600.0, 1300.0]])

    def test_last_chunk_absorbs_short_tail(self) -> None:
        planned = chunks.plan_chunks([[0.0, 1500.0]], 1500.0)
        self.assertEqual(len(planned), 2)
        self.assertLessEqual(planned[-1][1] - planned[-1][0], 900.0)


class JoinTest(unittest.TestCase):
    def test_same_voice_in_other_chunks_joins(self) -> None:
        segments = [seg("01-S01", 0, 30, [1.0, 0.0]), seg("02-S01", 600, 630, [0.95, 0.05]),
                    seg("01-S02", 30, 40, [0.0, 1.0])]
        groups = chunks.cluster(chunks.speaker_vectors(segments))
        self.assertIn(["01-S01", "02-S01"], [sorted(g) for g in groups])
        labels = chunks.global_labels(segments, groups)
        self.assertEqual(labels["01-S01"], labels["02-S01"])
        self.assertEqual(labels["01-S01"], "SPEAKER_00")
        self.assertEqual(labels["01-S02"], "SPEAKER_01")

    def test_two_labels_of_one_voice_inside_a_chunk_join(self) -> None:
        segments = [seg("01-S01", 0, 30, [1.0, 0.0]), seg("01-S03", 40, 60, [0.9, 0.1])]
        labels = chunks.global_labels(segments, chunks.cluster(chunks.speaker_vectors(segments)))
        self.assertEqual(labels["01-S01"], labels["01-S03"])

    def test_different_voices_stay_apart(self) -> None:
        segments = [seg("01-S01", 0, 30, [1.0, 0.0]), seg("02-S01", 600, 630, [0.3, 0.95])]
        labels = chunks.global_labels(segments, chunks.cluster(chunks.speaker_vectors(segments)))
        self.assertNotEqual(labels["01-S01"], labels["02-S01"])

    def test_short_or_unembedded_speaker_keeps_own_label(self) -> None:
        segments = [seg("01-S01", 0, 30, [1.0, 0.0]), seg("02-S01", 600, 630, [1.0, 0.0]),
                    seg("02-S02", 640, 643, [1.0, 0.0]), seg("02-S03", 650, 650.5, None)]
        labels = chunks.global_labels(segments, chunks.cluster(chunks.speaker_vectors(segments)))
        self.assertEqual(len({labels["01-S01"], labels["02-S02"], labels["02-S03"]}), 3)

    def test_profile_is_one_voice_per_person(self) -> None:
        segments = [seg("01-S01", 0, 30, [1.0, 0.0]), seg("02-S01", 600, 610, [0.0, 1.0]),
                    seg("02-S02", 620, 621, None)]
        labels = {"01-S01": "SPEAKER_00", "02-S01": "SPEAKER_00", "02-S02": "SPEAKER_01"}
        profiles = chunks.speaker_profiles(segments, labels)
        self.assertEqual(profiles["SPEAKER_00"]["seconds"], 40.0)
        self.assertAlmostEqual(profiles["SPEAKER_00"]["embedding"][0], 0.94868, places=4)
        self.assertEqual(profiles["SPEAKER_01"], {"seconds": 1.0, "embedding": []})

    def test_empty_stretch_needs_speech(self) -> None:
        segments = [seg("01-S01", 0, 10, None), seg("01-S01", 25, 30, None), seg("01-S01", 50, 55, None)]
        speech = [[0.0, 10.0], [12.0, 20.0], [25.0, 30.0], [50.0, 55.0]]
        self.assertEqual(chunks.empty_stretches(segments, speech, 70.0), [[10.0, 25.0]])


if __name__ == "__main__":
    unittest.main()
