# SubShare

## Programmable Recurring Multi-Party Escrow on Algorand

SubShare is a decentralized recurring shared payment protocol built on Algorand.  
It automates pooled expenses using deterministic smart contract logic instead of trust.

---

# 🔍 What This Project Demonstrates

- Recurring pooled payment logic using Algorand smart contracts
- Deterministic escrow + automated payout
- On-chain state management
- Wallet-based participation
- Backend orchestration for renewal cycles
- Real testnet transactions (not mocked)

---

# ✅ Features Implemented (Current MVP)

### Smart Contract Layer
- Pool creation
- Member joining
- Share deposit validation
- Escrow tracking
- Automatic payout when fully funded
- Renewal timestamp management
- Pool dissolution with refunds
- Local + global state tracking
- Testnet deployment script

### Backend (FastAPI)
- Pool metadata storage (PostgreSQL)
- Contract deployment integration
- Member tracking
- Deposit recording
- Renewal automation scheduler
- REST API endpoints

### Frontend (React + Vite)
- Pool creation UI
- Dashboard listing active pools
- Pool details page
- Join pool flow
- Deposit flow
- Real wallet integration (Pera)
- Transaction confirmation display

### Renewal Automation
- Scheduled backend job checks renewal timestamps
- Calls contract renewal logic if conditions satisfied
- Dissolves pool if deposits incomplete

---

# 🚧 Features NOT Yet Implemented

These are intentionally out of scope for MVP:

- AI-based pool matching
- Reputation scoring
- Dispute resolution
- Voting mechanisms
- Multi-subscription bundling
- Dynamic pricing
- Pro-rated mid-cycle refunds
- Admin rotation
- Mainnet deployment

---

# 🎯 Project Scope Clarification

This repository represents the foundational infrastructure layer.

It focuses on:
- On-chain recurring payment enforcement
- Escrow guarantees
- Automated renewal handling

It does NOT yet include higher-level features such as AI matching or governance.

---

# 📌 Future Roadmap

- AI-based pool optimization
- Risk scoring
- Mainnet deployment
- Cross-pool analytics
- SDK for third-party integrations
- UI/UX refinement
- Smart contract audit

---

# 📄 License

MIT License
