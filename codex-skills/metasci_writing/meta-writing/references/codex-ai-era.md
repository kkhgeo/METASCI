<!-- owner: codex; generated: true; do-not-edit: true -->
# Codex AI Era Rules — meta-writing

> Canonical source: `codex_scientific_writing_kernel/rules/`
> Apply every rule together with its diagnostic check, action, and exceptions.

## SW-AI-001 — retain-human-accountability

- **Rule:** Use AI as an assistive tool while keeping judgment, reasoning, argumentation, final approval, and accountability with the author.
- **Rationale:** Delegating core reasoning wholesale removes the critical scrutiny and authorial accountability that writing should preserve.
- **Diagnostic check:** Do core claims, arguments, or interpretations depend on AI output without independent author review and approval?
- **Action:** Separate AI-assisted tasks from judgments requiring author review, and assign final decisions, evidence checks, and approval explicitly to the author.
- **Operations:** plan, draft, rewrite, review, verify, submit
- **Stages:** planning, drafting, revision, verification, submission
- **Scales:** process, manuscript
- **Sections:** all, submission
- **Severity / evidence:** critical / moderate
- **Support counts:** 6 slugs, 4 independent source families
- **Evidence judgment:** Several studies, commentaries, and resonance sources support human accountability, while its operational form varies by policy and task layer.
- **Source-bank rule:** `ai-era-2`
- **Supporting sources:** `zhu-2026`, `huang-2023`, `connellpensky-2025`, `tweets-01b`, `tweets-01d`, `tweets-03`
- **Exceptions:**
  - Mechanical tasks such as format conversion still require output checking, but not the same level of substantive review.
  - Follow the applicable institutional and venue policy when defining permissible AI assistance.

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
