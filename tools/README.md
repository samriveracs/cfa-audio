# How this feed is made

Original study audio for the November 2026 CFA Level I exam, keyed to Kaplan Schweser module numbers. Not produced by or affiliated with Kaplan or CFA Institute.

- `manifest.json`: the 48 episodes, their topics and the Kaplan modules each covers.
- `SPEC.md`: rules every script follows (structure, spoken form, accuracy, originality).
- `REVIEW.md`: the independent fact check every script passes before recording.
- `tts_episode.py`: turns a transcript into an MP3 with the open source Kokoro 82M voice model and two co hosts, `af_heart` in American English and `bm_lewis` in British English. Untagged scripts alternate hosts by section. Scripts written as dialogue tag each paragraph `HEART:` or `LEWIS:` (questions `HEART Q:` or `LEWIS Q:`) and the voices follow the tags. Chapters per module, loudness normalized to -16 LUFS, MP3 40 kbps mono.
- `build_site.py`: writes `feed.xml` and `index.html` from the rendered episodes. Each episode file carries a version suffix (`E01_v3.mp3`), set per episode in `versions.json` with `v2` as the default.
- `REVISE.md`: how an episode is reworked into a dialogue after the listener finishes the matching reading.
- `render_daemon.sh`, `publish.sh`: render in order and push.

To fix an episode: edit its transcript, rerun `tts_episode.py N` with the Kokoro model files (`kokoro-v1.0.onnx`, `voices-v1.0.bin` from the kokoro-onnx model-files-v1.0 release), bump that episode's version in `versions.json` so podcast apps fetch the new file, run `build_site.py`, and push.
