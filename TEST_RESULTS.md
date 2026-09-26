# Verification results

## UI usability update

The updated main browser workflow passed again with no JavaScript page errors. A focused regression suite also passed: `python tests/ui_usability_check.py`.

New coverage: document-name search and empty search results; comparison loads automatically; action-plan generation uses the chosen document; brief edits survive internal navigation and autosave survives reload; draft objective/facts survive internal navigation; unavailable AI opens setup details; mobile navigation closes through Escape and backdrop; background controls are inert while the mobile menu is open. A test initially attempted string evaluation blocked by CSP; its assertion was changed to a locator-based assertion without weakening CSP.

UI changes include larger readable controls, synchronized mobile source tabs, responsive navigation, checklist progress, document selection, autosave status, and protection against replacing an existing brief without confirmation.

Observed on 26 September 2026, Windows, Python 3.14.7, installed Microsoft Edge through Playwright. Local server: `http://127.0.0.1:8000`.

## Deterministic server tests

Command: `python test.py`

**13 passed, 0 failed, 1 dependency deprecation warning; 1.44 seconds.**

Covered:

- Synthetic sample loading is idempotent; exact excerpts and paragraph offsets validate; the known 30/45-day deposit conflict is present.
- TXT, DOCX body/table and text-based PDF upload/extraction; PDF page anchors.
- Scanned PDF, unsupported extension, invalid PDF signature, empty content and size/character limits.
- Deterministic comparison detects the intended changed amounts, notice periods and end date.
- Unsupported question returns “I couldn’t find this in the provided document.”
- Embedded hostile instructions stay document text and do not trigger an action in the deterministic path.
- Missing AI credentials return a useful 503 response, without substituting demo analysis.
- Invalid AI source excerpts are rejected; mocked timeout and malformed JSON preserve the existing findings.
- Separate browser sessions cannot read or delete another session's document.
- Checklist and brief persistence, deletion, cross-origin rejection, inactivity expiration and session rate limit.
- Whitespace-only paste rejection and linked immutable document versions.

The warning is Starlette's deprecation notice about its current `httpx` TestClient integration. Tests still pass. Dependency migration should be addressed during production hardening.

## Browser workflow

Command: `python tests/browser_check.py`

**Passed with no JavaScript page errors.**

Verified sample loading; exact source and related-source navigation; changed amounts and four changed passages; unsupported Q&A; late-fee passage retrieval; 60-calendar-day notice calculation; task edit/completion persistence after reload; editable lawyer brief; actual clipboard copy/readback; actual downloaded TXT artifact; print action invocation and printable content; real TXT upload and document deletion.

Desktop viewport: 1440 × 1050. Mobile viewport: 390 × 844. Checked no horizontal document overflow, working source/analysis mobile controls, mobile navigation, and keyboard focus reaching interactive controls. Desktop and mobile screenshots were visually inspected. This is basic accessibility verification, not a WCAG audit or screen-reader test.

Print was intercepted to verify that `window.print()` is invoked with the generated printable text. The operating-system print dialog and actual PDF printer output were not automated.

Artifacts generated in `test-artifacts/`: empty and populated overview screenshots, comparison screenshot, mobile overview/review screenshots, and downloaded `lawyer-brief.txt`.

## Issues found and fixed

1. Windows CRLF line endings initially produced false comparison differences. Extraction now normalizes line endings before segmentation and comparison.
2. A malformed option tag prevented choosing the scenario counting convention. Corrected and verified through the full scenario workflow.
3. A browser-test selector omitted the citation button's arrow prefix. The selector was corrected; exact source text is asserted after navigation.

## AI and legal-content evaluation

No live provider credentials were supplied. **No live AI, Hindi/Marathi translation, legal accuracy or semantic quality evaluation has been performed.** Provider tests use mocked failure responses. Citation checks establish textual support, not truth or the correctness of an interpretation. The prompt-injection test covers the deterministic path; it is not evidence of live-model jailbreak resistance.

External legal research, OCR, public hosting, production security, parser stress/fuzz testing, multi-instance operations and screen-reader compatibility remain unverified. These boundaries are also described in the application and README.
