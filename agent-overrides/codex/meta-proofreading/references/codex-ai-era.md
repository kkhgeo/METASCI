<!-- owner: codex; generated: true; do-not-edit: true -->
# Codex AI Era Rules — meta-proofreading

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

## SW-AI-003 — do-not-use-detectors-as-proof

- **Rule:** Do not use an AI-detector score as sole or definitive evidence of authorship, plagiarism, or misconduct.
- **Rationale:** Detectors produce false positives, show bias against non-native writers, and cannot assess factual or argumentative validity.
- **Diagnostic check:** Is authorship or misconduct being inferred from a detector score alone?
- **Action:** Treat the score as a non-determinative signal, combine it with process evidence, source comparison, and contextual human review, and avoid categorical authorship claims.
- **Operations:** review, evaluate, verify
- **Stages:** verification, evaluation
- **Scales:** manuscript, section, paragraph
- **Sections:** all
- **Severity / evidence:** high / moderate
- **Support counts:** 2 slugs, 2 independent source families
- **Evidence judgment:** One direct study and one resonance source support a strong caution, but broader generalization remains limited.
- **Source-bank rule:** `ai-era-10`
- **Supporting sources:** `tsigaris-2026`, `tweets-03`
- **Exceptions:**
  - If institutional procedure requires a detector, report its limitations and the need for additional evidence.
  - Assess plagiarism separately through phrase and source comparison rather than conflating it with an AI score.

## SW-AI-004 — disclose-ai-use-by-policy

- **Rule:** Record the AI tool and the task it performed, and disclose that use to the extent required by the applicable venue or institutional policy.
- **Rationale:** Recording intervention level and author review enables more transparent and reconstructable accountability than naming a tool or declaring use alone.
- **Diagnostic check:** Is there enough record to reconstruct the tool, task, intervention level, author review status, and applicable policy?
- **Action:** Preserve prompts and outputs or a change-summary log, verify the current policy, and draft the required disclosure statement.
- **Operations:** draft, verify, submit
- **Stages:** drafting, verification, submission
- **Scales:** process, manuscript
- **Sections:** submission
- **Severity / evidence:** high / provisional
- **Support counts:** 1 slugs, 1 independent source families
- **Evidence judgment:** The bank provides only one direct supporting source, and disclosure requirements vary by policy, so this remains a conditional provisional rule.
- **Source-bank rule:** `ai-era-15`
- **Supporting sources:** `tsigaris-2026`
- **Exceptions:**
  - Do not make declarations of non-use a universal requirement; provide one only when the applicable policy requires it.
  - Do not retain sensitive information or copyrighted source material verbatim in logs; follow the governing retention policy.
