import json
from pathlib import Path

import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


def _ok(receipt):
    assert tx_execution_succeeded(receipt)
    return receipt


@pytest.mark.integration
def test_studionet_private_detail_match(default_account, secondary_account):
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "found_match.py")
    deployed = _ok(factory.deploy_contract_tx(args=["A match requires agreement on at least two distinctive non-public details and no material conflict."], account=default_account, wait_transaction_status=TransactionStatus.FINALIZED))
    address = extract_contract_address(deployed)
    finder = factory.build_contract(address, account=default_account)
    claimant = factory.build_contract(address, account=secondary_account)
    found = "Blue backpack with a stitched fox inside and locker key number 48."
    claim = "My blue backpack has a stitched fox inside and locker key number 48."
    found_commitment = finder.make_commitment(args=["FOUND", "item-1", found, "finder-secret-001"]).call()
    claim_commitment = claimant.make_commitment(args=["CLAIM", "claim-1", claim, "claimant-secret-001"]).call()
    _ok(finder.register_found(args=["item-1", "Blue backpack found near the station.", found_commitment]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(finder.reveal_found_details(args=["item-1", found, "finder-secret-001"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(claimant.open_claim(args=["claim-1", "item-1", claim_commitment]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(claimant.reveal_claim(args=["claim-1", claim, "claimant-secret-001"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    intelligent = _ok(claimant.review_claim(args=["claim-1"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    result = finder.get_claim(args=["claim-1"]).call()["result"]
    assert result in ("MATCH", "POSSIBLE", "NO_MATCH")
    print("STUDIONET_RECORD=" + json.dumps({"address": address, "deploy_tx": deployed["hash"], "intelligent_tx": intelligent["hash"], "observed": result}, sort_keys=True))
