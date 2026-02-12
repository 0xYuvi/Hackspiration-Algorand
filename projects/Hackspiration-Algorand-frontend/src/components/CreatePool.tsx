import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { useWallet } from '@txnlab/use-wallet-react'

export default function CreatePool() {
    const navigate = useNavigate()
    const { activeAddress } = useWallet()
    const [formData, setFormData] = useState({
        subscription_name: '',
        cost_per_cycle: '',
        max_members: '',
        cycle_duration: ''
    })
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')

    const handleChange = (e: any) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        })
    }

    const handleSubmit = async (e: any) => {
        e.preventDefault()
        if (!activeAddress) {
            setError('Please connect your wallet first.')
            return
        }

        setLoading(true)
        setError('')

        try {
            const payload = {
                subscription_name: formData.subscription_name,
                admin_wallet: activeAddress,
                cost_per_cycle: parseInt(formData.cost_per_cycle) * 1000000, // Convert to microAlgo
                max_members: parseInt(formData.max_members),
                cycle_duration: parseInt(formData.cycle_duration) * 86400, // Days to seconds
                renewal_timestamp: 0, // Backend sets this
                status: 0
            }

            const response = await axios.post('http://localhost:8000/create-pool', payload)
            navigate(`/pool/${response.data.id}`)
        } catch (err: any) {
            console.error(err)
            setError(err.response?.data?.detail || 'Failed to create pool')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="max-w-2xl mx-auto bg-gray-800 rounded-xl p-8 border border-gray-700 shadow-xl">
            <h2 className="text-3xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">Create a New Pool</h2>

            {error && (
                <div className="bg-red-900/50 border border-red-500 text-red-200 p-4 rounded-lg mb-6">
                    {error}
                </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                    <label className="block text-gray-300 font-bold mb-2">Subscription Name</label>
                    <input
                        type="text"
                        name="subscription_name"
                        value={formData.subscription_name}
                        onChange={handleChange}
                        className="w-full bg-gray-700 border border-gray-600 rounded-lg p-3 text-white focus:outline-none focus:border-blue-500"
                        placeholder="e.g. Netflix Premium"
                        required
                    />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label className="block text-gray-300 font-bold mb-2">Cost Per Cycle (ALGO)</label>
                        <input
                            type="number"
                            name="cost_per_cycle"
                            value={formData.cost_per_cycle}
                            onChange={handleChange}
                            className="w-full bg-gray-700 border border-gray-600 rounded-lg p-3 text-white focus:outline-none focus:border-blue-500"
                            placeholder="e.g. 5"
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-gray-300 font-bold mb-2">Maximum Members</label>
                        <input
                            type="number"
                            name="max_members"
                            value={formData.max_members}
                            onChange={handleChange}
                            className="w-full bg-gray-700 border border-gray-600 rounded-lg p-3 text-white focus:outline-none focus:border-blue-500"
                            placeholder="e.g. 4"
                            required
                        />
                    </div>
                </div>

                <div>
                    <label className="block text-gray-300 font-bold mb-2">Cycle Duration (Days)</label>
                    <input
                        type="number"
                        name="cycle_duration"
                        value={formData.cycle_duration}
                        onChange={handleChange}
                        className="w-full bg-gray-700 border border-gray-600 rounded-lg p-3 text-white focus:outline-none focus:border-blue-500"
                        placeholder="e.g. 30"
                        required
                    />
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    className={`w-full py-4 rounded-lg font-bold text-lg transition ${loading ? 'bg-gray-600 cursor-not-allowed' : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700'
                        }`}
                >
                    {loading ? 'Creating Pool...' : 'Launch Pool'}
                </button>
            </form>
        </div>
    )
}
