#!/usr/bin/env swift
// Retired compatibility shim. SpeechTranscriber via apple-stt is the only ASR path.

import Foundation

fputs("stt_fallback.swift is retired; use apple-stt (SpeechTranscriber)\n", stderr)
exit(64)
