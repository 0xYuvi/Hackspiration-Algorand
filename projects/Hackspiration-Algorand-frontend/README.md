# Hackspiration-Algorand-frontend

This is the React frontend for the Hackspiration-Algorand application, providing a user interface to interact with the SubSharePool smart contracts.

## Features
-   **React & Tailwind CSS**: Modern, responsive UI.
-   **AlgoKit Utils**: Simplified interaction with Algorand.
-   **use-wallet**: Seamless integration with Algorand wallets (Pera, Defly, Daffi, Exodus, etc.).
-   **Smart Contract Integration**: Generated TypeScript clients for `SubSharePool`.

## Setup

### Prerequisites
-   [Node.js](https://nodejs.org/en/download/) (v18.0+)
-   [AlgoKit CLI](https://github.com/algorandfoundation/algokit-cli#install)

### Installation
1.  Navigate to the project directory:
    ```bash
    cd projects/Hackspiration-Algorand-frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```

## Development

### Start Development Server
Run the local development server:
```bash
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) to view it in the browser.

### Build
Build the application for production:
```bash
npm run build
```

### Wallet Connection
The application uses `use-wallet` to connect to Algorand wallets.
-   **LocalNet**: Use KMD (Key Management Daemon) or a local wallet provider.
-   **TestNet/MainNet**: Use Pera, Defly, or other supported wallets.

## Smart Contract Integration
The frontend interacts with the `SubSharePool` smart contract using generated TypeScript clients.
-   Contracts are located in `src/contracts`.
-   See [src/contracts/README.md](src/contracts/README.md) for details on generating and using clients.

## Testing
Run the test suite:
```bash
npm test
```
