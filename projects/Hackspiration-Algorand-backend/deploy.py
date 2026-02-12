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
from contract import app

logger = logging.getLogger(__name__)

def get_deployer_account(algod_client: algod.AlgodClient) -> Account:
    # Use KMD for localnet/testnet MVP
    return get_kmd_wallet_account(algod_client, "unencrypted-default-wallet", "test")
    # In production, load from env
    # import os
    # mnemonic = os.getenv("DEPLOYER_MNEMONIC")
    # return Account(private_key=to_private_key(mnemonic))

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
    
    # Get deployer account
    deployer = get_deployer_account(algod_client)

    app_spec = app.build(client=algod_client) # Adjust build based on Beaker version usage
    # Wait, app.build() signature?
    # Spec might just be app.build()
    
    deploy(app_spec, algod_client, deployer)
