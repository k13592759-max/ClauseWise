# ClauseWise — Understand before you agree

A working local, session-only legal-information workspace. Built with Python/FastAPI, Pydantic, and a dependency-free responsive JavaScript interface. Python was available in the supplied workspace; Node.js was not. No account, database, analytics, or public hosting is configured.

## Run

Requires Python 3.11+ (tested with 3.14.7).

```powershell
python -m pip install --target .packages -r requirements.txt
python app.py
```

Open **http://127.0.0.1:8000**. Keep the terminal running. Dependencies are installed locally into `.packages`; an ordinary virtual environment also works. On this managed Windows workspace, the sandbox could not read dependencies installed outside it; server and test commands were run with approved external execution.

## Optional live AI

The application works without AI credentials using disclosed text-based tools and editorial synthetic examples. No live model has been verified in this delivery.

Set process environment variables before starting the server:

```powershell
$env:AI_API_KEY = "your-provider-key"
$env:AI_BASE_URL = "https://api.openai.com/v1"
$env:AI_MODEL = "gpt-4.1-mini"
python app.py
```

`.env.example` documents these settings; `.env` files are **not automatically loaded**. The provider must support the OpenAI-compatible `/chat/completions` endpoint and JSON object responses. Select a suitable model yourself; availability, costs, provider retention and language quality have not been verified. Keys never enter browser code. Run live analysis explicitly in the document review screen. The server sends document clauses and jurisdiction to the configured provider, applies a 45-second timeout, validates the output schema, and rejects any finding with an invented source ID or excerpt. A failed request preserves the existing review and can be retried. Exact citation validation does not establish that an interpretation is correct.

## Complete demonstration

1. Click **Explore a sample**. Confirm a jurisdiction or select **Unknown**. Three fictional documents load; nothing is inferred from currency or location.
2. Review the rental agreement. Switch reading depth to beginner or detailed to read editorial sample explanations alongside the full source.
3. Open **Attention flags**. Inspect the conflicting 30/45-day deposit-return provisions, then click each source citation.
4. Open **Compare**, select the rental original and revision, choose your role and compare. Rent changes from INR 20,000 to INR 23,000; deposit from INR 60,000 to INR 69,000; notice from 60 to 90 calendar days; the end date changes; the deposit conflict is resolved in the revision.
5. In **Ask ClauseWise**, ask about late payment. Matching passages include the one-time INR 500 fee. Ask “Are pets permitted?” to see the unsupported-answer state.
6. In document review, choose **What if?**, use receipt date 2026-10-01 and exclude receipt day. The original rental's 60-day arithmetic gives 30 November 2026, with explicit assumptions.
7. Generate an **Action Plan**, edit and check an item, then reload to verify session persistence.
8. Generate a **Lawyer Brief**, supplying your objective and facts. Edit, save, copy, download a text file, or print/save as PDF through your browser.
9. Delete a document or clear the workspace in **Privacy & Settings**.

## Architecture

- `app.py`: API, input validation, session isolation, extraction, passage anchors, deterministic flags, retrieval and comparison; optional server-side model adapter.
- `sample_explanations.py`: explicitly editorial explanations used **only** for synthetic sample documents.
- `static/`: semantic HTML, responsive CSS, JavaScript workspace and deterministic scenario date arithmetic.
- `samples/`: rental, revised rental and freelancer TXT documents, using fictional parties.
- `tests/`: deterministic API tests and a headless Edge end-to-end workflow.

PDF extraction keeps actual page numbers. DOCX and TXT use paragraph IDs and offsets without invented pagination. Line endings are normalized before segmentation. Each version has its own document and version ID; uploads can link to a parent document. Original records are not overwritten by revisions. Comparison aligns headings, marks fuzzy alignments uncertain, and uses word-level diffs independent of the model. Q&A retrieves matching passages; it does not synthesize a legal opinion. Scenario arithmetic uses UTC and asks the user to choose the counting convention.

## Privacy and limits

- Server-memory session records; random HTTP-only SameSite=Strict cookie; Secure cookie when accessed over HTTPS. No accounts or database. This local HTTP server makes no transport-encryption claim.
- Data survives reloads in the same session, but not server restarts. Sessions expire after 60 minutes of inactivity, purged on a subsequent request. Closing a tab alone does not immediately delete server memory. Multiple tabs sharing the cookie share a workspace.
- Delete removes the document and linked tasks, and clears the brief. Clear session removes all documents, tasks and brief. No application backups exist. User downloads and clipboard copies are outside deletion scope.
- 5 MB/file; 80,000 extracted characters; 100 PDF pages; 12 documents/session; live AI limit 30,000 characters. Files and AI inputs exceeding limits are rejected, never silently truncated.
- Text PDF, DOCX body paragraphs/tables and UTF-8 TXT supported. Scanned, partly empty or encrypted PDFs are rejected with a useful fallback. OCR unavailable. DOCX headers, footers, comments and text boxes are excluded and disclosed. Extracted text order/accuracy is not visually verified.
- Mutation limit of 40 requests/minute/session. Cross-origin mutations rejected; CSP and escaped rendering applied. Raw document contents are not logged by the application. No analytics or external fonts/scripts.
- Document instructions cannot invoke tools: the model has no tools or action capability. A server prompt treats documents as untrusted; schema and citation checks are additional safeguards, not a proof that prompt injection is impossible.

## Tests

```powershell
python test.py
# Start python app.py in another terminal, then:
python tests/browser_check.py
# Focused UI regression coverage:
python tests/ui_usability_check.py
```

Browser tests use installed Microsoft Edge via Playwright. Install Edge, or change the channel in the script for your platform. Artifacts go to `test-artifacts/` (ignored by git). See `TEST_RESULTS.md` for actual observed results and coverage boundaries.

## Known limitations / production work

This is a polished local demonstration, **not production-ready**.

- Uploaded documents receive extractive summaries and generic keyword-based review prompts without AI. Sample documents include authored plain-language explanations and a known conflict. Comprehensive entity extraction, obligation extraction and conflict detection for arbitrary documents are not implemented.
- Live AI generates cited findings only. Q&A remains lexical passage retrieval and may miss paraphrases or retrieve irrelevant matches. No embedding retrieval, multi-document synthesized answers, or external legal research. Ask about changed terms in Compare.
- Comparison shows deterministic wording changes with conditional review guidance; it does not currently provide model-generated semantic change explanations or reliable cross-reference alignment across heavily reorganized documents.
- The scenario explorer currently implements calendar-day notice dates and payment-passage retrieval. It does not calculate arbitrary penalties, business days, holidays or competing triggers.
- Hindi/Marathi explanations depend on the configured model. No translation or live model quality evaluation has run.
- Date and obligation extracts require human confirmation. No calendar reminders, messages, lawyer contacts or payments are sent.
- Parsing is bounded by file and extracted-content limits but is synchronous and not process-isolated. Add CPU/memory/time isolation, malware screening and structured validation of all checklist records before accepting hostile public uploads.
- Production needs reviewed provider contracts, HTTPS, authentication if accounts exist, durable tenant-isolated storage with defined backup deletion, secrets management, global/user rate limits, CSRF hardening for the hosting environment, monitoring without content logs, expiry scheduling, dependency pinning/audits, load testing and independent security/accessibility/legal-content review.
- In-memory sessions require one worker and one instance; do not scale this storage layer horizontally. Application process memory cannot be guaranteed securely erased.

## Hosting

Public hosting remains incomplete. To run a private single-instance evaluation on Linux, create a virtual environment, install requirements, and run:

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 1 --no-access-log
```

Place behind a properly configured HTTPS reverse proxy and restrict access. Configure trusted proxy headers for your actual topology so HTTPS cookies work correctly. Do not treat these commands as a production hardening procedure; complete the production requirements above before public use.
