# Security

## Controls reviewed

- The contract pins the concrete GenVM runner `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`.
- User text, identifiers, arrays, and lifecycle counts are bounded.
- Role and phase checks reject unauthorized or repeated transitions.
- Model input is framed as untrusted evidence; output is restricted to fixed enums or exact-length bitmasks.
- Validator replay recomputes the decision instead of trusting a leader-only answer.
- No private key, wallet file, secret, production credential, token custody, or GEN transfer exists in the repository.

## Threats and limitations

The contract judges only the revealed on-chain descriptions. Commitments prevent post-hoc changes but do not keep revealed details secret; no external source is collected.

Do not place passwords, identity documents, tracking codes, or dangerous meeting details on-chain. Physical identity and safe handoff remain off-chain responsibilities.

On-chain text is public and permanent. Frontends must warn users not to submit secrets, personal identifiers, or confidential evidence. A value-bearing or regulated deployment needs a separate threat model, authenticated sources, operational appeals, and an audited settlement adapter.

Report suspected vulnerabilities privately to the repository owner. Do not place exploit details in a public issue before coordinated review.
