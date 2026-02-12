from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    wallet_address: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class PoolBase(BaseModel):
    subscription_name: str
    admin_wallet: str
    cost_per_cycle: int
    max_members: int
    cycle_duration: int
    renewal_timestamp: int
    status: int

class PoolCreate(PoolBase):
    pass

class Pool(PoolBase):
    id: int
    contract_address: Optional[str]
    created_at: datetime
    class Config:
        orm_mode = True

class PoolMemberBase(BaseModel):
    pool_id: int
    wallet_address: str
    is_active: bool
    deposited_amount: int

class PoolMemberCreate(PoolMemberBase):
    pass

class PoolMember(PoolMemberBase):
    id: int
    joined_at: datetime
    class Config:
        orm_mode = True
