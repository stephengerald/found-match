from pathlib import Path
import json

CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "found_match.py"
SDK = "v0.2.16"
PROMPT = "Independently compare a lost-item claim"
RULES = "A match requires agreement on at least two distinctive non-public details and no material conflict. Generic similarity alone is only possible."


def deploy(vm, direct_deploy, alice):
    vm.sender = alice
    return direct_deploy(str(CONTRACT), RULES, sdk_version=SDK)


def test_commit_reveal_match_and_two_party_handoff(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    found_details = "Blue canvas backpack with a stitched fox inside and locker key numbered 48."
    claim_details = "My blue canvas backpack has a stitched fox inside and locker key number 48."
    found_nonce = "finder-nonce-001"
    claim_nonce = "claimant-nonce-001"
    found_commitment = contract.make_commitment("FOUND", "item-1", found_details, found_nonce)
    claim_commitment = contract.make_commitment("CLAIM", "claim-1", claim_details, claim_nonce)
    contract.register_found("item-1", "Blue backpack found near the west station entrance.", found_commitment)
    contract.reveal_found_details("item-1", found_details, found_nonce)
    direct_vm.sender = direct_bob
    contract.open_claim("claim-1", "item-1", claim_commitment)
    contract.reveal_claim("claim-1", claim_details, claim_nonce)
    direct_vm.mock_llm(PROMPT, json.dumps({"result": "MATCH"}))
    contract.review_claim("claim-1")
    contract.confirm_handoff("claim-1")
    direct_vm.sender = direct_alice
    contract.confirm_handoff("claim-1")
    assert contract.get_claim("claim-1")["result"] == "HANDED_OVER"
    assert contract.get_found("item-1")["status"] == "CLAIMED"
    leader = direct_vm._captured_validators[-1][0]
    assert direct_vm.run_validator(leader_result=leader) is True


def test_commitment_and_identity_checks(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    details = "Black umbrella with a wooden duck handle and initials carved below the grip."
    commitment = contract.make_commitment("FOUND", "umbrella", details, "secure-nonce-88")
    contract.register_found("umbrella", "Black umbrella found in the lobby.", commitment)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("only_finder"):
        contract.reveal_found_details("umbrella", details, "secure-nonce-88")
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("found_commitment_mismatch"):
        contract.reveal_found_details("umbrella", details, "wrong-nonce-999")


def test_non_match_cannot_handoff_and_bad_model_output_fails(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    found = "Red lunch bag with a silver astronaut pin and two green containers."
    claim = "Red lunch bag containing one blue container and no pins or badges."
    contract.register_found("lunch", "Red lunch bag found after class.", contract.make_commitment("FOUND", "lunch", found, "found-secret-42"))
    contract.reveal_found_details("lunch", found, "found-secret-42")
    direct_vm.sender = direct_bob
    contract.open_claim("c2", "lunch", contract.make_commitment("CLAIM", "c2", claim, "claim-secret-42"))
    contract.reveal_claim("c2", claim, "claim-secret-42")
    direct_vm.mock_llm(PROMPT, json.dumps({"result": "NO_MATCH"}))
    contract.review_claim("c2")
    with direct_vm.expect_revert("confirmed_match_required"):
        contract.confirm_handoff("c2")
    direct_vm.clear_mocks()
    direct_vm.sender = direct_alice
    found2 = "Gray notebook with a torn yellow corner and the number 917 on the inside cover."
    contract.register_found("book", "Gray notebook found in room 4.", contract.make_commitment("FOUND", "book", found2, "found-secret-91"))
    contract.reveal_found_details("book", found2, "found-secret-91")
    direct_vm.sender = direct_bob
    claim2 = "My gray notebook has a torn yellow corner and number 917 inside."
    contract.open_claim("c3", "book", contract.make_commitment("CLAIM", "c3", claim2, "claim-secret-91"))
    contract.reveal_claim("c3", claim2, "claim-secret-91")
    direct_vm.mock_llm(PROMPT, json.dumps({"result": "LIKELY"}))
    with direct_vm.expect_revert("invalid_match_result"):
        contract.review_claim("c3")

