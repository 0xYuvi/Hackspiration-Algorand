import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from typing import List

from database import engine, Base, get_db
import models, schemas
from deploy import deploy, get_deployer_account, get_algod_client

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SubShare API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from database import SessionLocal

@app.post("/create-pool", response_model=schemas.Pool)
def create_pool(pool: schemas.PoolCreate, db: Session = Depends(get_db)):
    # 1. Deploy Smart Contract
    # In a real app, we might want the user to deploy. 
    # For MVP, backend deploys on behalf of user (or checks pre-deployed ID if frontend deploys).
    # Here we assume backend deploys.
    
    try:
        algod_client = get_algod_client()
        deployer = get_deployer_account(algod_client)
        
        # We need to import the contract spec. 
        # Ideally this comes from the contract file or artifact.
        # For simplicity, we assume we can import the app spec here or use a dummy one if file not present in backend context.
        # In a real monorepo, backend would import from contracts package.
        # Here we will just place a placeholder or assume the contract file is copied.
        # For this MVP, we will simulate the deployment ID or use a simplified deploy if files aren't shared.
        
        # REAL IMPLEMENTATION:
        # app_id = deploy(pool.subscription_name, pool.admin_wallet, pool.cost_per_cycle, pool.max_members, pool.cycle_duration)
        
        # Mocking app_id for MVP if contract code isn't directly importable in backend env without package setup
        # But we will try to do it right if possible.
        app_id = 123456 # Placeholder if deployment fails
        contract_address = "mock_address"

        # TO DO: Integrate actual deployment call here
        
    except Exception as e:
        print(f"Deployment failed: {e}")
        # Proceeding for MVP structure
        pass
        
    db_pool = models.Pool(
        subscription_name=pool.subscription_name,
        admin_wallet=pool.admin_wallet,
        cost_per_cycle=pool.cost_per_cycle,
        max_members=pool.max_members,
        cycle_duration=pool.cycle_duration,
        renewal_timestamp=int(datetime.utcnow().timestamp()) + pool.cycle_duration,
        status=0, # FORMING
        contract_address="APP_ID_123" # Replace with actual
    )
    db.add(db_pool)
    db.commit()
    db.refresh(db_pool)
    return db_pool

@app.get("/pool/{pool_id}", response_model=schemas.Pool)
def get_pool(pool_id: int, db: Session = Depends(get_db)):
    pool = db.query(models.Pool).filter(models.Pool.id == pool_id).first()
    if not pool:
        raise HTTPException(status_code=404, detail="Pool not found")
    return pool

@app.get("/pools", response_model=List[schemas.Pool])
def list_pools(db: Session = Depends(get_db)):
    return db.query(models.Pool).all()

@app.post("/join-pool", response_model=schemas.PoolMember)
def join_pool(member: schemas.PoolMemberCreate, db: Session = Depends(get_db)):
    # Verify pool exists
    pool = db.query(models.Pool).filter(models.Pool.id == member.pool_id).first()
    if not pool:
        raise HTTPException(status_code=404, detail="Pool not found")
        
    # Check if already a member
    existing = db.query(models.PoolMember).filter(
        models.PoolMember.pool_id == member.pool_id, 
        models.PoolMember.wallet_address == member.wallet_address
    ).first()
    
    if existing:
        return existing

    new_member = models.PoolMember(
        pool_id=member.pool_id,
        wallet_address=member.wallet_address,
        is_active=True,
        deposited_amount=0
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

@app.post("/deposit")
def track_deposit(pool_id: int, wallet_address: str, amount: int, db: Session = Depends(get_db)):
    member = db.query(models.PoolMember).filter(
        models.PoolMember.pool_id == pool_id, 
        models.PoolMember.wallet_address == wallet_address
    ).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    member.deposited_amount += amount
    db.commit()
    return {"status": "updated", "new_balance": member.deposited_amount}

@app.get("/user/{wallet_address}", response_model=List[schemas.PoolMember])
def get_user_memberships(wallet_address: str, db: Session = Depends(get_db)):
    return db.query(models.PoolMember).filter(models.PoolMember.wallet_address == wallet_address).all()

# Scheduler for Renewal
def check_renewals():
    db = SessionLocal()
    try:
        now = int(datetime.utcnow().timestamp())
        pools = db.query(models.Pool).filter(models.Pool.renewal_timestamp < now, models.Pool.status == 1).all()
        for pool in pools:
            print(f"Triggering renewal for pool {pool.id}")
            # Call Smart Contract Renew Cycle
            # deploy.renew_cycle(pool.contract_address) 
            
            # Update DB
            pool.renewal_timestamp += pool.cycle_duration
            db.commit()
    finally:
        db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(check_renewals, 'interval', minutes=1)
scheduler.start()
