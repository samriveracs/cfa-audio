# How this feed is made

Original study audio for the November 2026 CFA Level I exam, keyed to Kaplan Schweser module numbers. Not produced by or affiliated with Kaplan or CFA Institute.

- `manifest.json`: the 48 episodes, their topics and the Kaplan modules each covers.
- `SPEC.md`: rules every script follows (structure, spoken form, accuracy, originality).
- `REVIEW.md`: the independent fact check every script passes before recording.
- `tts_episode.py`: turns `transcripts/ENN.txt` into `episodes/ENN.mp3` with the open source Kokoro 82M voice model (narrator `af_heart`, headers and questions `am_michael`), chapters per module, loudness normalized to -16 LUFS, MP3 40 kbps mono.
- `build_site.py`: writes `feed.xml` and `index.html` from the rendered episodes.
- `render_daemon.sh`, `publish.sh`: render in order and push.

To fix an episode: edit its transcript, rerun `tts_episode.py N` with the Kokoro model files (`kokoro-v1.0.onnx`, `voices-v1.0.bin` from the kokoro-onnx model-files-v1.0 release), keep the same file name, run `build_site.py`, and push.
