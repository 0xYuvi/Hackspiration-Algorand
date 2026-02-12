# Contracts Integration

This directory contains the generated TypeScript clients for interacting with the specific smart contracts of the **Hackspiration-Algorand** project.

## Generated Clients

### 1. `SubSharePoolClient`
-   **Source**: `projects/Hackspiration-Algorand-contracts/smart_contracts/subshare_pool`
-   **Usage**: Create, join, and manage subscription pools.

### 2. `HelloWorldClient`
-   **Source**: `projects/Hackspiration-Algorand-contracts/smart_contracts/hackspiration_algorand`
-   **Usage**: Basic interaction testing.

## Generating Clients

To regenerate the clients after modifying the smart contracts:

1.  Navigate to the project root or the frontend directory.
2.  Run the following command:
    ```bash
    npm run generate:app-clients
    ```
    (This command uses `algokit project link` to automatically generate and place the clients here).

## Usage Example

```typescript
import * as algokit from '@algorandfoundation/algokit-utils';
import { SubSharePoolClient } from './SubSharePoolClient';

// ... inside your component or function
const algod = algokit.getAlgoClient();
const indexer = algokit.getAlgoIndexerClient();
const kmd = algokit.getAlgoKmdClient();

const client = new SubSharePoolClient(
  {
    resolveBy: 'id',
    id: 123, // App ID
  },
  algod
);

// Call a method
const result = await client.getGlobalState();
```
