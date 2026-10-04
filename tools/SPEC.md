# CFA Level I Audio Review: script spec

You are writing ONE episode script for a private study podcast for a candidate sitting the CFA Level I exam on November 17, 2026 (2026 curriculum). He studies with Kaplan Schweser, so every episode is keyed to Kaplan module numbers and names. He listens while running and commuting, at normal speed, with no screen. Your script is turned directly into speech by a text to speech engine, so you are writing for the ear.

## Length and shape

- Target 4,400 to 4,700 words of spoken text (about 29 to 31 minutes). Stay inside that range. Count with `wc -w` before finishing.
- Do NOT write an intro or outro. The production adds "Episode N, title, modules covered" before your text and a sign off after it. Start directly with the first section header.
- Required structure, in this order:
  1. `## The big picture` : 1 to 2 minutes. What this group of modules is about, why it matters on the exam, how the pieces connect.
  2. One section per Kaplan module, in Kaplan's order, header written exactly as `## Module 1.1, Interest Rates and Return Measurement` (module number, comma, Kaplan module name exactly as given in your assignment). Spend time roughly in proportion to the Kaplan minutes given in your assignment, but give more time to concepts that are heavily tested or easy to confuse. Very small modules can be short.
  3. `## Recall check` : 6 questions. Each question is one line that starts with `Q: `. The production inserts a 5 second pause after every Q line automatically. The next paragraph must start with `Answer:` and give the answer and the reason in 2 to 4 sentences. Mix concept questions, "which is most likely" style questions, and at most two quick mental math questions with round numbers.
  4. `## Recap` : 6 to 8 must know points, spoken as short sentences in one or two paragraphs (no list markers).
- Inside each module section, cover: what the idea is and why it exists (first principles), how it works, any formula spoken slowly with every term defined, a tiny worked example with round numbers that can be followed without paper, and the exam traps (why the tempting wrong answer tempts). Repeat the single most important formula or rule once more at the end of its section.

## Markup (the only markup allowed)

- `## Header text` on its own line: section header, read by a second voice.
- `Q: question text` on its own line: recall question, read by the second voice, followed by an automatic pause.
- Everything else: plain paragraphs separated by one blank line, read by the main narrator. Keep paragraphs to 2 to 6 sentences.
- No markdown anywhere else: no bullets, numbers lists, bold, italics, tables, parentheses for asides (rewrite as a sentence), brackets, URLs, emojis.

## Writing for the ear

- Short and medium sentences. Conversational, precise, calm. Second person is fine ("you"). No filler, no hype, no jokes that waste time.
- Signpost: "Three things drive this." "First... Second... Third..." "Here is the trap."
- Formulas: say them in words, never symbols. Write "the holding period return equals the ending price minus the beginning price plus any income, all divided by the beginning price." Never write =, +, ×, /, ^, Σ, Greek letters, subscripts or superscripts. Say "sigma squared", "beta", "r squared", "one plus r, raised to the power n".
- Numbers: digits are fine for plain numbers and decimals ("6 percent", "1.08", "250 dollars"). Always write "percent" as a word, never the % sign. Write money as "1,000 dollars", never with a $ sign. Write "basis points" in words. Avoid long decimals; round to what a listener can hold.
- Do not use slashes. Write "price to earnings ratio", "debt to equity", "the I Y key" style phrasing.
- No hyphens or dashes of any kind, no semicolons. Rewrite hyphenated words as separate words ("time weighted", "money weighted", "long term", "put call parity") EXCEPT inside the exact Kaplan module name in a section header, which must be copied exactly.
- Acronyms: these are handled by the voice engine and may be used freely after you define them once: NPV, IRR, WACC, CAPM, SML, CML, GDP, ESG, IFRS, GAAP, EPS, ROE, ROA, EBIT, EBITDA, LIFO, FIFO, ABS, MBS, CMO, CDO, ETF, REIT, FX, ANOVA, CFA, YTM, OAS, DDM, FCFE, FCFF, PPE, DTA, DTL, VaR, LBO, VC, CPI, OTC, CCP, LIBOR, SOFR. Any other acronym: spell it with spaces the first time ("P V B P") or just say the words.
- Calculator: the candidate uses a TI BA II Plus Professional. Where a calculator procedure is the core skill (time value of money, NPV and IRR, statistics worksheet, amortization, bond pricing), give a short spoken keystroke walkthrough: name the worksheet, clearing it, the settings that matter (P Y and C Y, begin or end mode), the inputs in order, which key computes, the sign convention and the expected display. Write the calculator as "the B A two plus". Elsewhere skip keystrokes.

## Content rules

- Scope is the 2026 CFA Level I curriculum as represented by the Kaplan module names you are given. Do not wander into Level II material. If you must mention something beyond Level I, say so in one sentence, or leave it out.
- FSA: IFRS is the default. State U.S. GAAP differences where they are testable.
- Accuracy is the priority. Every formula, definition, direction of effect and number must be right. Verify every calculation by running Python before you finalize. If you are not sure a specific detail is in the 2026 Level I curriculum or is stated a certain way, either leave it out or state it in a way that is correct regardless.
- Everything must be your own original explanation. Do not quote or closely paraphrase Kaplan SchweserNotes, Secret Sauce, Kaplan quizzes or QBank, or CFA Institute curriculum text. Never invent LOS numbers, page numbers, or claims about what Kaplan or CFA Institute "say". Recall questions must be your own.
- Optionally, at most twice per episode, add one sentence linking a concept to bank or credit union balance sheet work (capital planning, interest rate risk, funding). Keep it generic. No names of employers or people.
- Do not mention the listener's name or personal details. The script is published on a public website.

## Deliverable

Write the script as plain UTF-8 text to the path given in your assignment. Then run these checks and fix anything they flag:

```
wc -w FILE
grep -nP '[%$=+×/^;\x{2013}\x{2014}\[\]\(\)*_#]' FILE | grep -v '^[0-9]*:## '
grep -nP '\w-\w' FILE | grep -v '^[0-9]*:## '
```

Header lines (starting with `## `) may contain the exact Kaplan module name, including any hyphen or slash in it. Nothing else may contain those characters.

Reply with: final word count, the list of section headers, and every number or formula you verified with Python (one line each).

## Tool use

Use WebSearch (or the Parallel web_search tool) for scope checks rather than page fetches. Keep CPU use light, because audio rendering runs on this machine.
