from __future__ import annotations
import json
from pathlib import Path
from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

PROMPT = "Independently compare a lost-item claim"
RULES = "A match requires agreement on at least two distinctive non-public details and no material conflict."


def context():
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {PROMPT: json.dumps({"result": "MATCH"})}})
    return {"validators": [validator.to_dict() for validator in validators]}


def write_succeeded(receipt):
    assert tx_execution_succeeded(receipt)


def test_five_validator_match_and_handoff():
    finder, claimant = create_accounts(2)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "found_match.py")
    deployed = factory.deploy_contract_tx(args=[RULES], account=finder, wait_transaction_status=TransactionStatus.FINALIZED)
    write_succeeded(deployed)
    address = extract_contract_address(deployed)
    finder_contract = factory.build_contract(address, account=finder)
    claimant_contract = factory.build_contract(address, account=claimant)
    found = "Blue backpack with a stitched fox inside and locker key number 48."
    claim = "My blue backpack has a stitched fox inside and locker key number 48."
    found_commitment = finder_contract.make_commitment(args=["FOUND", "item-1", found, "finder-secret-001"]).call()
    claim_commitment = claimant_contract.make_commitment(args=["CLAIM", "claim-1", claim, "claimant-secret-001"]).call()
    write_succeeded(finder_contract.register_found(args=["item-1", "Blue backpack found near the station.", found_commitment]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    write_succeeded(finder_contract.reveal_found_details(args=["item-1", found, "finder-secret-001"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    write_succeeded(claimant_contract.open_claim(args=["claim-1", "item-1", claim_commitment]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    write_succeeded(claimant_contract.reveal_claim(args=["claim-1", claim, "claimant-secret-001"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    write_succeeded(claimant_contract.review_claim(args=["claim-1"]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED))
    write_succeeded(claimant_contract.confirm_handoff(args=["claim-1"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    write_succeeded(finder_contract.confirm_handoff(args=["claim-1"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    assert finder_contract.get_claim(args=["claim-1"]).call()["result"] == "HANDED_OVER"

