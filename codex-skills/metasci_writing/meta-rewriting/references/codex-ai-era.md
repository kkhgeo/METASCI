<!-- owner: codex; generated: true; do-not-edit: true -->
# Codex AI Era Rules — meta-rewriting

> Canonical source: `codex_scientific_writing_kernel/rules/`
> Apply every rule together with its diagnostic check, action, and exceptions.

## SW-AI-002 — verify-ai-factual-claims

- **Rule:** Do not present AI-generated or AI-transformed facts, numbers, legal claims, or citations as verified until they have been checked against an original or authoritative source.
- **Rationale:** Generative AI can present errors and hallucinations fluently and with unwarranted confidence.
- **Diagnostic check:** Does every AI-involved factual claim have a verifiable source and a recorded fidelity status?
- **Action:** Build an evidence inventory, mark unchecked items as unverified, and require tool-limited consumers to defer factual correction to the author rather than inventing a fix.
- **Operations:** draft, rewrite, review, verify
- **Stages:** drafting, revision, verification
- **Scales:** manuscript, section, paragraph, sentence
- **Sections:** all, references
- **Severity / evidence:** critical / strong
- **Support counts:** 4 slugs, 4 independent source families
- **Evidence judgment:** Several independent studies and commentaries directly support the risk of AI hallucination and factual error.
- **Source-bank rule:** `ai-era-4`
- **Supporting sources:** `connellpensky-2025`, `huang-2023`, `tsigaris-2026`, `zhu-2026`
- **Exceptions:**
  - Even after grammar-only or formatting-only assistance, confirm that numbers and citations were not moved or altered.
  - Do not automatically delete an unverifiable claim; flag it for author judgment.
