# Submission: Found Match

Project name: Found Match

Repository: https://github.com/stephengerald/found-match

StudioNet contract: https://explorer-studio.genlayer.com/address/0xbaFF05a23961440949Ce23c8EFa5ac7f420e35BC

Deployment transaction: https://explorer-studio.genlayer.com/tx/0x28755ee3565b88a831ad4cd94827196e5ca965526460faea6ecf98938110931e

Intelligent transaction: https://explorer-studio.genlayer.com/tx/0x59a8dd5aadd7b4cdccac869ee7b10d3070e9cd640cb072ea9a2696c6fdf35e3c

Summary: Compares a lost-item claim with a found-item record through two-sided commitment and reveal, then supports a mutual handoff confirmation.

Why it is GenLayer-native: Validators semantically compare distinctive item details under fixed matching rules and return MATCH, POSSIBLE, or NO_MATCH.

Evidence/source model: The contract judges only the revealed on-chain descriptions. Commitments prevent post-hoc changes but do not keep revealed details secret; no external source is collected.

Declared scope: Reusable, non-custodial prototype. Do not place passwords, identity documents, tracking codes, or dangerous meeting details on-chain. Physical identity and safe handoff remain off-chain responsibilities.

Review evidence: `AUDIT.md`, `SECURITY.md`, `SOURCE_POLICY.md`, and `deployments/studionet.json` bind the reviewed source hash to the public live result.
