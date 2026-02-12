import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import { Calendar, Users, DollarSign, Activity } from 'lucide-react'

interface Pool {
    id: number
    subscription_name: string
    cost_per_cycle: number
    max_members: number
    current_members?: number // Calculated or from DB
    cycle_duration: number
    renewal_timestamp: number
    status: number
}

// Mock data if backend not reachable
const mockPools: Pool[] = []

export default function Dashboard() {
    const [pools, setPools] = useState<Pool[]>(mockPools)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetchPools()
    }, [])

    const fetchPools = async () => {
        try {
            const response = await axios.get('http://localhost:8000/pools')
            setPools(response.data)
        } catch (error) {
            console.error("Failed to fetch pools", error)
        } finally {
            setLoading(false)
        }
    }

    const getStatusColor = (status: number) => {
        if (status === 0) return "text-yellow-400"
        if (status === 1) return "text-green-400"
        return "text-red-400"
    }

    const getStatusText = (status: number) => {
        if (status === 0) return "Forming"
        if (status === 1) return "Active"
        return "Dissolved"
    }

    if (loading) return <div className="text-center py-20">Loading pools...</div>

    return (
        <div>
            <div className="flex justify-between items-center mb-8">
                <h1 className="text-3xl font-bold">Available Pools</h1>
                <Link to="/create" className="bg-purple-600 hover:bg-purple-700 px-6 py-2 rounded-lg font-bold transition">
                    + Create New Pool
                </Link>
            </div>

            {pools.length === 0 ? (
                <div className="text-center py-20 bg-gray-800 rounded-xl">
                    <h3 className="text-xl text-gray-400">No pools found. Create one!</h3>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {pools.map(pool => (
                        <div key={pool.id} className="bg-gray-800 rounded-xl p-6 border border-gray-700 hover:border-purple-500 transition shadow-lg">
                            <div className="flex justify-between items-start mb-4">
                                <h3 className="text-xl font-bold">{pool.subscription_name}</h3>
                                <span className={`text-sm font-bold uppercase tracking-wider ${getStatusColor(pool.status)}`}>
                                    {getStatusText(pool.status)}
                                </span>
                            </div>

                            <div className="space-y-3 text-gray-300">
                                <div className="flex items-center gap-2">
                                    <DollarSign size={18} className="text-purple-400" />
                                    <span>{(pool.cost_per_cycle / 1000000).toFixed(2)} ALGO / cycle</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <Users size={18} className="text-blue-400" />
                                    <span>Max {pool.max_members} members</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <Calendar size={18} className="text-green-400" />
                                    <span>Renew: {new Date(pool.renewal_timestamp * 1000).toLocaleDateString()}</span>
                                </div>
                            </div>

                            <Link to={`/pool/${pool.id}`} className="block mt-6 text-center bg-gray-700 hover:bg-gray-600 py-2 rounded-lg transition font-medium">
                                View Details
                            </Link>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}
