# SubShare - Instructions

## 1. Prerequisites
- Node.js & npm
- Python 3.12+
- Docker (for PostgreSQL) or a local PostgreSQL instance
- Algorand Pera Wallet (Mobile or Web)

## 2. Backend Setup
1. Navigate to `projects/Hackspiration-Algorand-backend`
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Setup Database:
   - Ensure PostgreSQL is running.
   - Create valid `.env` file or export `DATABASE_URL`:
     ```bash
     export DATABASE_URL="postgresql://user:password@localhost/subshare_db"
     ```
5. Run Backend:
   ```bash
   uvicorn main:app --reload
   ```

## 3. Frontend Setup
1. Navigate to `projects/Hackspiration-Algorand-frontend`
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run Frontend:
   ```bash
   npm run dev
   ```

## 4. Smart Contract Deployment (Testnet)
To deploy contracts to Testnet:
1. Ensure your `.env` in `projects/Hackspiration-Algorand-backend` has:
   ```
   DEPLOYER_MNEMONIC="your 25 word mnemonic..."
   ALGOD_SERVER="https://testnet-api.algonode.cloud"
   ALGOD_TOKEN=""
   ```
2. The backend attempts to deploy when creating a pool.
3. For manual deployment, run:
   ```bash
   cd projects/Hackspiration-Algorand-backend
   python deploy.py
   ```

## 5. Usage
1. Open Frontend (http://localhost:5173).
2. Connect Pera Wallet (Testnet).
3. Click "Create Pool" to start a new subscription group.
4. Share the Pool ID/Link.
5. Members join and deposit ALGO.
6. Once full, the contract triggers payout to Admin.

## Notes
- The MVP uses a simplified deployment flow. In production, the backend should handle smart contract compilation and deployment more robustly or offload it to the frontend via user signing.
- Ensure your Pera Wallet is on **Testnet**.
