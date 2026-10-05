# Revising an episode with the listener's Kaplan pages

Use this when the listener shares the Kaplan SchweserNotes pages they just studied for an episode's modules and asks for that episode to be reworked. Episode 1, version 5 and Episode 2, version 3 (October 5, 2026) are the models to follow: transcripts/E01.txt and transcripts/E02.txt.

## Who it is for

The listener hears these while running or driving, with no paper, screen or calculator. Every sentence has to work by ear alone. Calculation practice stays in Kaplan's QBank and quizzes. The episode's job is understanding: what each idea means, why it works, when to use it, which way things move, and the traps.

## Inputs and handling

- Extract the PDFs to text in a private working folder such as kaplan/ENN/ outside this repo. Never copy Kaplan files or text into this public repo or anywhere else that is shared.
- Read every page. List each learning outcome and concept, the conventions Kaplan uses (sign conventions, notation, which date a value lands on), and Kaplan's own worked examples, numbers and phrasing so they can be avoided.
- Read the current script and the episode's review note.

## Listening rules

- Opening: the renderer says "Episode N. Topic, Modules X through Y." The script then opens with one short paragraph that lists the topics in plain words, at most two sentences. No greetings, no host introductions, no big picture banter. Go straight into the first module.
- No calculator content of any kind: no keystrokes, worksheets, modes, sign conventions for entering cash flows, or "on the calculator".
- Few numbers. No formulas read aloud as symbols or step by step arithmetic, and no worked numeric examples to follow. A formula may appear only as a short relationship in words when the relationship is the idea (payment divided by the rate, dividend yield plus growth). Use a simple round number only when it carries the point by itself (up 10 percent then down 10 percent leaves you behind).
- Never assume the listener can see anything: no "as you can see", tables, notation on a page, or "write this down".
- Teach with specific, everyday or market examples and analogies: picture first, then the idea in words, then the direction or comparison that matters, then the trap.
- Name the proper term every time a concept is introduced, then explain it in plain English. The listener wants the jargon for colleagues and the plain version for senior leaders.
- Format: two host dialogue. Every paragraph starts with `HEART:` or `LEWIS:`. Recall questions start with `HEART Q:` or `LEWIS Q:`, and the other host answers in a paragraph that starts with `Answer.` Headers stay `## Module N.N, exact Kaplan name`. Keep each host within about 45 to 55 percent of the words.
- One host explains, the other asks the question a listener would ask, adds an example, or catches the trap. No filler, praise or chat between them. A one or two sentence takeaway at the end of a module is fine.
- `## Recall check`: about 10 to 12 conceptual questions (which measure, which direction, why, when), never a calculation. Each answer gives the answer in one sentence, then "Here is why." and the mechanism in two to four sentences, so the listener learns the reasoning rather than memorizing the pair.
- End with `## Key takeaways`, about three minutes: memory hooks first (mnemonics, acronyms, short rules and analogies that are literally accurate), then "how you would say it to a senior leader" lines, each followed by "The jargon is" and the proper terms. Every hook is fact checked like the body.
- Cover every concept on the Kaplan pages and match Kaplan's conventions so nothing contradicts what the listener just read. Use original wording and original examples. Do not reuse Kaplan's examples, numbers or sentence structure, and do not describe what Kaplan says or does.
- Length follows the material, with no target and no padding.
- All other SPEC.md rules still apply: spoken form, no symbols or slashes, no hyphens, dashes or semicolons outside headers, acronyms, accuracy checked, no personal details.

## Check, record and publish

1. Independent fact check with REVIEW.md plus: the listening rules above, coverage and conventions against the Kaplan extract, and anything copied from Kaplan. Apply the fixes and save a short review note as reviews/ENN_vK.md.
2. Pronunciation check: print the phonemes (kokoro_onnx Tokenizer.phonemize, en-us and en-gb) for every unusual term, abbreviation and hook word in the script. Respell anything wrong in the PRON list in bin/tts_episode.py so the fix applies to every episode. Known fixes: arbitrage, arbitrageur, arithmetic, covariance, MAD, Platy. Avoid numbers with decimals in prose.
3. Keep the previous script in scripts/old/ENN_vK.txt and replace scripts/ENN.txt.
4. Render with tts_episode.py N. It follows the speaker tags and uses the one line opening.
5. Bump the episode's file version in audio/versions.json so podcast apps fetch the new file, run publish.sh, and confirm the feed and file on the live site.
6. Tell the listener what changed, the new length, and that the old download should be deleted if their app kept it.
