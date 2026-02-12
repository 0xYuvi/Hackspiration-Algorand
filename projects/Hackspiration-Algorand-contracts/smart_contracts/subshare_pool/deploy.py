import logging
import base64
from algosdk.v2client import algod
from algosdk.mnemonic import to_private_key
from algokit_utils import (
    Account,
    ApplicationSpecification,
    ApplicationClient,
    get_algod_client,
    get_indexer_client,
    get_kmd_wallet_account,
)
from contract import SubSharePool

logger = logging.getLogger(__name__)

def deploy(
    app_spec: ApplicationSpecification,
    algod_client: algod.AlgodClient,
    deployer: Account,
) -> None:
    app_client = ApplicationClient(
        algod_client=algod_client,
        app_spec=app_spec,
        signer=deployer,
    )

    app_id, app_addr, tx_id = app_client.create(
        subscription_name="Netflix Share",
        admin_address=deployer.address,
        cost_per_cycle=1000000, # 1 Algo
        max_members=4,
        cycle_duration=60*60*24*30 # 30 days
    )
    
    logger.info(f"Deployed app_id: {app_id}, app_addr: {app_addr}")
    return app_id

if __name__ == "__main__":
    import json
    
    # Get localnet or testnet client
    algod_client = get_algod_client()
    indexer_client = get_indexer_client()
    
    # Get deployer account (using localnet default or environment variable)
    deployer = get_kmd_wallet_account(algod_client, "unencrypted-default-wallet", "test")
    # In production/testnet, use mnemonic from env
    # import os
    # mnemonic = os.getenv("DEPLOYER_MNEMONIC")
    # if mnemonic:
    #     private_key = to_private_key(mnemonic)
    #     deployer = Account(private_key=private_key)

    app = SubSharePool()
    app_spec = app.application_spec()
    
    deploy(app_spec, algod_client, deployer)
