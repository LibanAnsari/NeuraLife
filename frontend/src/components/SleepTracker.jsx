import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Navbar from './Navbar';

const API_URL = 'http://localhost:8000';

function SleepTracker({ setToken }) {
  const navigate = useNavigate();
  const [sleepLogs, setSleepLogs] = useState([]);
  const [bedtime, setBedtime] = useState('22:00');
  const [waketime, setWaketime] = useState('07:00');
  const [quality, setQuality] = useState(3);
  const [notes, setNotes] = useState('');
  const [insights, setInsights] = useState(null);
  const [showSuccess, setShowSuccess] = useState(false);

  useEffect(() => {
    fetchSleepLogs();
    fetchInsights();
  }, []);

  const fetchSleepLogs = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/sleep/history`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSleepLogs(response.data.logs);
    } catch (err) {
      console.error('Error fetching sleep logs:', err);
    }
  };

  const fetchInsights = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/sleep/insights`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setInsights(response.data);
    } catch (err) {
      console.error('Error fetching insights:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const token = localStorage.getItem('token');
      await axios.post(
        `${API_URL}/api/sleep/log`,
        { bedtime, waketime, quality, notes },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);
      setNotes('');
      fetchSleepLogs();
      fetchInsights();
    } catch (err) {
      console.error('Error logging sleep:', err);
      alert('Failed to log sleep');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-300">
      <Navbar setToken={setToken} />

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <button
            onClick={() => navigate('/dashboard')}
            className="flex items-center gap-2 text-gray-600 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400 mb-4 transition-colors duration-300"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to Dashboard
          </button>

          <h1 className="text-4xl font-bold text-gray-800 dark:text-gray-100 mb-2 transition-colors duration-300">
            😴 Sleep Tracker
          </h1>
          <p className="text-gray-600 dark:text-gray-300 transition-colors duration-300">
            Monitor your sleep patterns for better rest
          </p>
        </div>

        {showSuccess && (
          <div className="mb-6 bg-green-100 dark:bg-green-900/30 border-2 border-green-500 rounded-xl p-4 animate-bounce transition-colors duration-300">
            <p className="text-green-800 dark:text-green-200 font-semibold transition-colors duration-300">
              ✅ Sleep logged! +30 NeuraCoins earned!
            </p>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8 transition-colors duration-300">
              <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-100 mb-6 transition-colors duration-300">
                Log Last Night's Sleep
              </h2>

              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-gray-700 dark:text-gray-300 font-semibold mb-2 transition-colors duration-300">
                      Bedtime
                    </label>
                    <input
                      type="time"
                      value={bedtime}
                      onChange={(e) => setBedtime(e.target.value)}
                      className="w-full px-4 py-3 border-2 border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 dark:bg-gray-700 dark:text-gray-100 transition-colors duration-300"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-gray-700 dark:text-gray-300 font-semibold mb-2 transition-colors duration-300">
                      Wake Time
                    </label>
                    <input
                      type="time"
                      value={waketime}
                      onChange={(e) => setWaketime(e.target.value)}
                      className="w-full px-4 py-3 border-2 border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 dark:bg-gray-700 dark:text-gray-100 transition-colors duration-300"
                      required
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-gray-700 dark:text-gray-300 font-semibold mb-2 transition-colors duration-300">
                    Sleep Quality: {'⭐'.repeat(quality)}
                  </label>
                  <input
                    type="range"
                    min="1"
                    max="5"
                    value={quality}
                    onChange={(e) => setQuality(parseInt(e.target.value))}
                    className="w-full h-3 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer accent-purple-600 transition-colors duration-300"
                  />
                  <div className="flex justify-between text-sm text-gray-600 dark:text-gray-400 mt-1 transition-colors duration-300">
                    <span>Poor</span>
                    <span>Excellent</span>
                  </div>
                </div>

                <div>
                  <label className="block text-gray-700 dark:text-gray-300 font-semibold mb-2 transition-colors duration-300">
                    Notes (optional)
                  </label>
                  <textarea
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    rows="3"
                    placeholder="How did you sleep? Any dreams?"
                    className="w-full px-4 py-3 border-2 border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 dark:bg-gray-700 dark:text-gray-100 transition-colors duration-300"
                  />
                </div>

                <button
                  type="submit"
                  className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-4 rounded-xl font-semibold hover:from-purple-700 hover:to-pink-700 transition-all duration-300 transform hover:scale-105 shadow-lg"
                >
                  Log Sleep
                </button>
              </form>
            </div>
          </div>

          <div className="space-y-6">
            {insights && insights.total_logs > 0 && (
              <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 transition-colors duration-300">
                <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4 transition-colors duration-300">
                  📊 Your Stats
                </h3>
                <div className="space-y-4">
                  <div>
                    <p className="text-gray-600 dark:text-gray-400 text-sm transition-colors duration-300">
                      Avg Sleep Duration
                    </p>
                    <p className="text-2xl font-bold text-purple-600 dark:text-purple-400 transition-colors duration-300">
                      {insights.average_duration_hours}h
                    </p>
                  </div>
                  <div>
                    <p className="text-gray-600 dark:text-gray-400 text-sm transition-colors duration-300">
                      Avg Quality
                    </p>
                    <p className="text-2xl font-bold text-purple-600 dark:text-purple-400 transition-colors duration-300">
                      {'⭐'.repeat(Math.round(insights.average_quality))}
                    </p>
                  </div>
                </div>
              </div>
            )}

            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 transition-colors duration-300">
              <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4 transition-colors duration-300">
                📅 Recent Logs
              </h3>
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {sleepLogs.slice(0, 7).map(log => (
                  <div
                    key={log.id}
                    className="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg transition-colors duration-300"
                  >
                    <div className="flex justify-between items-center mb-1">
                      <span className="font-semibold text-gray-800 dark:text-gray-100 transition-colors duration-300">
                        {log.date}
                      </span>
                      <span className="text-purple-600 dark:text-purple-400 font-bold transition-colors duration-300">
                        {log.duration_hours}h
                      </span>
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400 transition-colors duration-300">
                      {'⭐'.repeat(log.quality)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default SleepTracker;
