# Evidence and source policy

## What validators receive

The contract judges only the revealed on-chain descriptions. Commitments prevent post-hoc changes but do not keep revealed details secret; no external source is collected.

All submitted text is treated as untrusted evidence, never as instructions. Evidence fields and aggregate storage are bounded before they reach the prompt. The decision schema is fixed and independently replayed by validators.

## Who selects the evidence

The authorized roles in the state machine—finder and claimant—supply the evidence. Their signatures establish which on-chain role submitted a record; they do not prove that the record is truthful or complete.

## External collection

This version performs no live web browsing, URL fetching, hidden source lookup, or mutable off-chain collection. That makes the deployed judgment reproducible from contract state, while leaving source authenticity as an explicit application-layer responsibility.

## Trust and production boundary

Do not place passwords, identity documents, tracking codes, or dangerous meeting details on-chain. Physical identity and safe handoff remain off-chain responsibilities. If an adapter later fetches external material, its allowlist, content bounds, snapshot rules, publisher trust, correction policy, and failure behavior require a new review.
