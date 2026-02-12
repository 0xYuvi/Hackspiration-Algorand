from sqlalchemy import Column, Integer, String, BigInteger, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    wallet_address = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    memberships = relationship("PoolMember", back_populates="user")

class Pool(Base):
    __tablename__ = "pools"
    id = Column(Integer, primary_key=True, index=True)
    contract_address = Column(String, unique=True, index=True)
    subscription_name = Column(String)
    admin_wallet = Column(String)
    cost_per_cycle = Column(BigInteger)
    max_members = Column(Integer)
    cycle_duration = Column(Integer)
    renewal_timestamp = Column(BigInteger)
    status = Column(Integer) # 0=FORMING, 1=ACTIVE, 2=DISSOLVED
    created_at = Column(DateTime, default=datetime.utcnow)

    members = relationship("PoolMember", back_populates="pool")

class PoolMember(Base):
    __tablename__ = "pool_members"
    id = Column(Integer, primary_key=True, index=True)
    pool_id = Column(Integer, ForeignKey("pools.id"))
    wallet_address = Column(String, ForeignKey("users.wallet_address"))
    is_active = Column(Boolean, default=True)
    deposited_amount = Column(BigInteger, default=0)
    joined_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="memberships")
    pool = relationship("Pool", back_populates="members")
