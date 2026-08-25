# Architecture

## State machine

A finder commits and reveals item details, a different claimant commits and reveals a claim, consensus compares the records, and both parties must confirm any matched handoff.

The relevant roles are finder and claimant. Write methods enforce role, phase, uniqueness, and bounded-storage rules before any state transition.

## Consensus boundary

Validators semantically compare distinctive item details under fixed matching rules and return MATCH, POSSIBLE, or NO_MATCH. The leader returns a small JSON schema; validators independently rerun the same decision function and accept only exact enum or bitmask values. Malformed model output raises a tagged model error and writes no decision.

## Deterministic boundary

Enrollment, authorization, commitments, counters, phase changes, caps, masks, and any score or credit arithmetic are deterministic contract logic. Only semantic interpretation of the stored evidence occurs inside `run_nondet_unsafe`.

## Off-chain boundary

Wallet custody, identity verification, indexing, notifications, private file storage, source authentication, money movement, legal process, and user-interface behavior are outside this repository. Do not place passwords, identity documents, tracking codes, or dangerous meeting details on-chain. Physical identity and safe handoff remain off-chain responsibilities.
