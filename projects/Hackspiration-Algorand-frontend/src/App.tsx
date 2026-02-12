import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import { WalletProvider, useWallet, WalletManager, WalletId } from '@txnlab/use-wallet-react'
import { SnackbarProvider } from 'notistack'
import Dashboard from './components/Dashboard'
import CreatePool from './components/CreatePool'
import PoolDetails from './components/PoolDetails'
import ConnectWallet from './components/ConnectWallet'
import { useState } from 'react'
import { getAlgodConfigFromViteEnvironment } from './utils/network/getAlgoClientConfigs'

// Define supported wallets
const supportedWallets = [
  WalletId.PERA,
  WalletId.DEFLY,
  WalletId.EXODUS,
  WalletId.KIBISIS,
]

const Layout = ({ children }: { children: React.ReactNode }) => {
  const { activeAddress } = useWallet()
  const [openWalletModal, setOpenWalletModal] = useState(false)

  return (
    <div className="min-h-screen bg-gray-900 text-white font-sans">
      <nav className="p-4 border-b border-gray-800 flex justify-between items-center bg-gray-900">
        <Link to="/" className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
          SubShare
        </Link>
        <div className="flex gap-6 items-center">
          <Link to="/" className="hover:text-blue-400 transition">Dashboard</Link>
          <Link to="/create" className="hover:text-blue-400 transition">Create Pool</Link>
          <button
            onClick={() => setOpenWalletModal(true)}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition font-medium"
          >
            {activeAddress ? `${activeAddress.slice(0, 6)}...${activeAddress.slice(-4)}` : "Connect Wallet"}
          </button>
        </div>
      </nav>
      <main className="container mx-auto p-8">
        {children}
      </main>
      <ConnectWallet openModal={openWalletModal} closeModal={() => setOpenWalletModal(false)} />
    </div>
  )
}

export default function App() {
  const algodConfig = getAlgodConfigFromViteEnvironment()

  const walletManager = new WalletManager({
    wallets: supportedWallets,
    defaultNetwork: algodConfig.network === 'mainnet' ? 'mainnet' : 'testnet',
    networks: {
      [algodConfig.network]: {
        algod: {
          baseServer: algodConfig.server,
          port: algodConfig.port,
          token: String(algodConfig.token),
        },
      },
    },
    options: {
      resetNetwork: true,
    },
  })

  return (
    <SnackbarProvider maxSnack={3}>
      <WalletProvider manager={walletManager}>
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/create" element={<CreatePool />} />
              <Route path="/pool/:id" element={<PoolDetails />} />
            </Routes>
          </Layout>
        </Router>
      </WalletProvider>
    </SnackbarProvider>
  )
}
