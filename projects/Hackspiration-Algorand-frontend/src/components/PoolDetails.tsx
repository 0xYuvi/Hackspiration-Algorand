import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import axios from 'axios'
import { useWallet } from '@txnlab/use-wallet-react'
import algosdk from 'algosdk'
import { getAlgodConfigFromViteEnvironment } from '../utils/network/getAlgoClientConfigs'

interface Pool {
    id: number
    subscription_name: string
    admin_wallet: string
    cost_per_cycle: number
    max_members: number
    cycle_duration: number
    renewal_timestamp: number
    status: number
    contract_address: string
}

interface Member {
    pool_id: number
    wallet_address: string
    is_active: boolean
    deposited_amount: number
}

export default function PoolDetails() {
    const { id } = useParams()
    const { activeAddress, signTransactions } = useWallet()
    const [pool, setPool] = useState<Pool | null>(null)
    const [member, setMember] = useState<Member | null>(null)
    const [amount, setAmount] = useState('')
    const [loading, setLoading] = useState(false)

    const algodConfig = getAlgodConfigFromViteEnvironment()
    const algodClient = new algosdk.Algodv2(
        algodConfig.token,
        algodConfig.server,
        algodConfig.port
    )

    useEffect(() => {
        fetchPool()
    }, [id])

    useEffect(() => {
        if (activeAddress && pool) {
            checkMembership()
        }
    }, [activeAddress, pool])

    const fetchPool = async () => {
        try {
            const res = await axios.get(`http://localhost:8000/pool/${id}`)
            setPool(res.data)
        } catch (e) {
            console.error(e)
        }
    }

    const checkMembership = async () => {
        try {
            const res = await axios.get(`http://localhost:8000/user/${activeAddress}`)
            const membership = res.data.find((m: Member) => m.pool_id === Number(id))
            setMember(membership || null)
        } catch (e) {
            console.error(e)
        }
    }

    const handleJoin = async () => {
        if (!activeAddress) return alert("Connect wallet")
        setLoading(true)
        try {
            await axios.post('http://localhost:8000/join-pool', {
                pool_id: Number(id),
                wallet_address: activeAddress,
                is_active: true,
                deposited_amount: 0
            })
            checkMembership()
        } catch (e) {
            console.error(e)
            alert("Failed to join")
        } finally {
            setLoading(false)
        }
    }

    const handleDeposit = async () => {
        if (!pool || !activeAddress) return
        setLoading(true)

        try {
            const amountMicroAlgo = parseFloat(amount) * 1000000

            const suggestedParams = await algodClient.getTransactionParams().do()

            const txn = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
                from: activeAddress,
                to: pool.contract_address || activeAddress, // Fallback if no contract address
                amount: BigInt(Math.round(amountMicroAlgo)),
                suggestedParams,
            })

            const encodedTxn = algosdk.encodeUnsignedTransaction(txn)

            const signedTxn = await signTransactions([encodedTxn])

            const { txId } = await algodClient.sendRawTransaction(signedTxn).do()
            console.log("Transaction ID:", txId)

            await algosdk.waitForConfirmation(algodClient, txId, 4)

            // Notify backend
            await axios.post(`http://localhost:8000/deposit?pool_id=${id}&wallet_address=${activeAddress}&amount=${amountMicroAlgo}`)

            alert(`Deposit successful! TX: ${txId}`)
            checkMembership()

        } catch (e) {
            console.error(e)
            alert("Deposit failed")
        } finally {
            setLoading(false)
        }
    }

    if (!pool) return <div className="text-center p-10">Loading...</div>

    return (
        <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-gray-800 p-8 rounded-xl border border-gray-700">
                <h1 className="text-3xl font-bold mb-4">{pool.subscription_name}</h1>
                <div className="space-y-4 text-gray-300">
                    <p><strong>Cost:</strong> {(pool.cost_per_cycle / 1000000).toFixed(2)} ALGO</p>
                    <p><strong>Members:</strong> {pool.max_members} max</p>
                    <p><strong>Renewal:</strong> {new Date(pool.renewal_timestamp * 1000).toLocaleDateString()}</p>
                    <p><strong>Status:</strong> {pool.status === 0 ? 'Forming' : 'Active'}</p>
                    <p className="text-xs text-gray-500 break-all">Contract: {pool.contract_address}</p>
                </div>
            </div>

            <div className="bg-gray-800 p-8 rounded-xl border border-gray-700">
                <h2 className="text-2xl font-bold mb-6">Your Membership</h2>

                {!activeAddress ? (
                    <p className="text-yellow-400">Please connect wallet to interact.</p>
                ) : !member ? (
                    <button
                        onClick={handleJoin}
                        disabled={loading}
                        className="w-full bg-blue-600 hover:bg-blue-700 py-3 rounded-lg font-bold transition"
                    >
                        {loading ? "Joining..." : "Join Pool"}
                    </button>
                ) : (
                    <div className="space-y-6">
                        <div className="bg-gray-700 p-4 rounded-lg">
                            <p className="text-sm text-gray-400">Deposited</p>
                            <p className="text-2xl font-bold text-green-400">{(member.deposited_amount / 1000000).toFixed(2)} ALGO</p>
                        </div>

                        <div>
                            <label className="block text-sm font-bold mb-2">Deposit Share (ALGO)</label>
                            <div className="flex gap-2">
                                <input
                                    type="number"
                                    value={amount}
                                    onChange={(e) => setAmount(e.target.value)}
                                    className="flex-1 bg-gray-900 border border-gray-600 rounded-lg p-3 text-white"
                                    placeholder="0.00"
                                />
                                <button
                                    onClick={handleDeposit}
                                    disabled={loading}
                                    className="bg-green-600 hover:bg-green-700 px-6 rounded-lg font-bold"
                                >
                                    {loading ? "..." : "Deposit"}
                                </button>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}
