# Revising an episode with the listener's Kaplan pages

Use this when the listener shares the Kaplan SchweserNotes pages they just studied for an episode's modules and asks for that episode to be reworked. Episode 1 (October 4, 2026) is the model to follow: transcripts/E01.txt.

## Inputs and handling

- Extract the PDFs to text in a private working folder such as kaplan/ENN/ outside this repo. Never copy Kaplan files or text into this public repo or anywhere else that is shared.
- Read every page. List each learning outcome and concept, the conventions Kaplan uses (sign conventions, notation, which root or exponent, which date a value lands on), and Kaplan's own worked examples and numbers so they can be avoided.
- Read the current script and the episode's review note.

## Rewrite rules

- Format: two host dialogue. Every paragraph starts with `HEART:` or `LEWIS:`. Recall questions start with `HEART Q:` or `LEWIS Q:`, and the other host answers in a paragraph that starts with `Answer.` Headers stay `## Module N.N, exact Kaplan name`. Keep the two hosts within about 45 to 55 percent of the words each.
- One host explains, the other asks the question a listener would ask, adds an analogy, or catches the trap. No filler or praise between them.
- Teach for the ear: an analogy or everyday picture first, then the recipe in words, then one small worked example with round numbers that can be followed without paper, then the trap. Explain why a formula works rather than reciting symbols. Give calculator keystrokes only where the calculator is the skill.
- Cover every concept on the Kaplan pages and match Kaplan's conventions so nothing contradicts what the listener just read. Use original wording and original examples. Do not reuse Kaplan's examples or numbers.
- Length follows the material. No fixed target. Episode 1 runs about 8,800 words, roughly 55 minutes.
- All other SPEC.md rules still apply: spoken form, no symbols or slashes, no hyphens, dashes or semicolons outside headers, acronyms, accuracy checked in Python, no personal details.

## Check, record and publish

1. Independent fact check with REVIEW.md plus: keep the tags, compare coverage and conventions against the Kaplan extract, and remove anything copied from Kaplan.
2. Keep the previous script in scripts/old/ENN_vK.txt and replace scripts/ENN.txt.
3. Render with tts_episode.py N. It follows the speaker tags.
4. Bump the episode's file version in audio/versions.json (for example "1": "v3") so podcast apps fetch the new file, run publish.sh, and confirm the feed and file on the live site.
5. Tell the listener what changed, the new length, and that the old download should be deleted if their app kept it.
