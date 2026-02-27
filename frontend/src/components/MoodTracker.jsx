import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Navbar from './Navbar';

const API_URL = 'http://localhost:8000';

const moods = [
  { emoji: '😊', label: 'Happy', value: 'happy' },
  { emoji: '😐', label: 'Neutral', value: 'neutral' },
  { emoji: '😢', label: 'Sad', value: 'sad' },
  { emoji: '😰', label: 'Anxious', value: 'anxious' },
  { emoji: '😡', label: 'Angry', value: 'angry' },
];

const activities = [
  { icon: '😴', label: 'Sleep', value: 'sleep' },
  { icon: '🏃', label: 'Exercise', value: 'exercise' },
  { icon: '🤝', label: 'Social', value: 'social' },
  { icon: '💼', label: 'Work', value: 'work' },
  { icon: '🍕', label: 'Food', value: 'food' },
  { icon: '🎮', label: 'Leisure', value: 'leisure' },
];

function MoodTracker({ setToken }) {
  const navigate = useNavigate();
  const [selectedMood, setSelectedMood] = useState('');
  const [intensity, setIntensity] = useState(3);
  const [notes, setNotes] = useState('');
  const [selectedActivities, setSelectedActivities] = useState([]);
  const [moodHistory, setMoodHistory] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [showSuccess, setShowSuccess] = useState(false);
  const [coinsEarned, setCoinsEarned] = useState(0);

  useEffect(() => {
    fetchMoodHistory();
    fetchAnalytics();
  }, []);

  const fetchMoodHistory = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/mood/history?days=30`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setMoodHistory(response.data.entries);
    } catch (err) {
      console.error('Error fetching mood history:', err);
    }
  };

  const fetchAnalytics = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/mood/analytics`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setAnalytics(response.data);
    } catch (err) {
      console.error('Error fetching analytics:', err);
    }
  };

  const handleActivityToggle = (value) => {
    setSelectedActivities(prev =>
      prev.includes(value)
        ? prev.filter(a => a !== value)
        : [...prev, value]
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selectedMood) {
      alert('Please select a mood');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${API_URL}/api/mood/log`,
        {
          mood: moods.find(m => m.value === selectedMood).emoji,
          intensity,
          notes,
          activities: selectedActivities.join(',')
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      setCoinsEarned(response.data.coins_earned);
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);

      // Reset form
      setNotes('');
      setIntensity(3);

      // Refresh data
      fetchMoodHistory();
      fetchAnalytics();
    } catch (err) {
      console.error('Error logging mood:', err);
      
      // Show more specific error message
      let errorMessage = 'Failed to log mood';
      if (err.response) {
        // Server responded with error
        errorMessage = `Failed to log mood: ${err.response.data.detail || err.response.statusText}`;
        console.error('Response error:', err.response.data);
      } else if (err.request) {
        // Request made but no response
        errorMessage = 'Failed to log mood: Server not responding. Make sure the backend is running on http://localhost:8000';
        console.error('No response from server');
      } else {
        // Error setting up request
        errorMessage = `Failed to log mood: ${err.message}`;
      }
      
      alert(errorMessage);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-300">
      <Navbar setToken={setToken} />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
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
            📊 Mood Tracker
          </h1>
          <p className="text-gray-600 dark:text-gray-300 transition-colors duration-300">
            Track your emotions and identify patterns over time
          </p>
        </div>

        {/* Success Message */}
        {showSuccess && (
          <div className="mb-6 bg-green-100 dark:bg-green-900/30 border-2 border-green-500 rounded-xl p-4 animate-bounce transition-colors duration-300">
            <div className="flex items-center gap-3">
              <span className="text-4xl">🎉</span>
              <div>
                <p className="text-green-800 dark:text-green-200 font-semibold transition-colors duration-300">
                  Mood logged successfully!
                </p>
                {coinsEarned > 0 && (
                  <p className="text-green-700 dark:text-green-300 transition-colors duration-300">
                    🪙 +{coinsEarned} NeuraCoins earned!
                  </p>
                )}
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Log Mood Form */}
          <div className="lg:col-span-2">
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8 transition-colors duration-300">
              <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-100 mb-6 transition-colors duration-300">
                How are you feeling today?
              </h2>

              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Mood Selection */}
                <div>
                  <label className="block text-gray-700 dark:text-gray-300 font-semibold mb-4 transition-colors duration-300">
                    Select your mood:
                  </label>
                  <div className="grid grid-cols-5 gap-4">
                    {moods.map(mood => (
                      <button
                        key={mood.value}
                        type="button"
                        onClick={() => setSelectedMood(mood.value)}
                        className={`p-4 rounded-xl border-2 transition-all duration-300 transform hover:scale-110 ${
                          selectedMood === mood.value
                            ? 'border-purple-500 bg-purple-100 dark:bg-purple-900/40 dark:border-purple-400 scale-110'
                            : 'border-gray-300 dark:border-gray-600 hover:border-purple-300 dark:hover:border-purple-500'
                        }`}
                      >
                        <div className="text-4xl mb-2">{mood.emoji}</div>
                        <div className="text-sm text-gray-700 dark:text-gray-300 transition-colors duration-300">
                          {mood.label}
                        </div>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Intensity Slider */}
                <div>
                  <label className="block text-gray-700 dark:text-gray-300 font-semibold mb-2 transition-colors duration-300">
                    Intensity: {intensity}/5
                  </label>
                  <input
                    type="range"
                    min="1"
                    max="5"
                    value={intensity}
                    onChange={(e) => setIntensity(parseInt(e.target.value))}
                    className="w-full h-3 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer accent-purple-600 transition-colors duration-300"
                  />
                  <div className="flex justify-between text-sm text-gray-600 dark:text-gray-400 mt-1 transition-colors duration-300">
                    <span>Mild</span>
                    <span>Moderate</span>
                    <span>Intense</span>
                  </div>
                </div>

                {/* Activities */}
                <div>
                  <label className="block text-gray-700 dark:text-gray-300 font-semibold mb-4 transition-colors duration-300">
                    What influenced your mood?
                  </label>
                  <div className="grid grid-cols-3 gap-3">
                    {activities.map(activity => (
                      <button
                        key={activity.value}
                        type="button"
                        onClick={() => handleActivityToggle(activity.value)}
                        className={`p-3 rounded-lg border-2 transition-all duration-300 ${
                          selectedActivities.includes(activity.value)
                            ? 'border-purple-500 bg-purple-100 dark:bg-purple-900/40 dark:border-purple-400'
                            : 'border-gray-300 dark:border-gray-600 hover:border-purple-300 dark:hover:border-purple-500'
                        }`}
                      >
                        <div className="text-2xl mb-1">{activity.icon}</div>
                        <div className="text-sm text-gray-700 dark:text-gray-300 transition-colors duration-300">
                          {activity.label}
                        </div>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Notes */}
                <div>
                  <label className="block text-gray-700 dark:text-gray-300 font-semibold mb-2 transition-colors duration-300">
                    Notes (optional):
                  </label>
                  <textarea
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    rows="3"
                    className="w-full px-4 py-3 border-2 border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 dark:bg-gray-700 dark:text-gray-100 transition-colors duration-300"
                    placeholder="Anything else you'd like to note about your mood..."
                  />
                </div>

                {/* Submit Button */}
                <button
                  type="submit"
                  className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-4 rounded-xl font-semibold hover:from-purple-700 hover:to-pink-700 transition-all duration-300 transform hover:scale-105 shadow-lg"
                >
                  Log Mood for Today
                </button>
              </form>
            </div>
          </div>

          {/* Analytics Sidebar */}
          <div className="space-y-6">
            {/* Quick Stats */}
            {analytics && analytics.total_entries > 0 && (
              <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 transition-colors duration-300">
                <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4 transition-colors duration-300">
                  📈 Your Stats
                </h3>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600 dark:text-gray-400 transition-colors duration-300">
                      Total Entries
                    </span>
                    <span className="text-2xl font-bold text-purple-600 dark:text-purple-400 transition-colors duration-300">
                      {analytics.total_entries}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600 dark:text-gray-400 transition-colors duration-300">
                      Most Common
                    </span>
                    <span className="text-3xl">
                      {analytics.most_common_mood}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600 dark:text-gray-400 transition-colors duration-300">
                      Avg Intensity
                    </span>
                    <span className="text-2xl font-bold text-purple-600 dark:text-purple-400 transition-colors duration-300">
                      {analytics.average_intensity}/5
                    </span>
                  </div>
                </div>
              </div>
            )}

            {/* Recent Entries */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 transition-colors duration-300">
              <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4 transition-colors duration-300">
                📅 Recent Entries
              </h3>
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {moodHistory.slice(0, 10).map(entry => (
                  <div
                    key={entry.id}
                    className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg transition-colors duration-300"
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-3xl">{entry.mood}</span>
                      <div>
                        <div className="text-sm font-semibold text-gray-800 dark:text-gray-100 transition-colors duration-300">
                          {entry.date}
                        </div>
                        <div className="text-xs text-gray-600 dark:text-gray-400 transition-colors duration-300">
                          Intensity: {entry.intensity}/5
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
                {moodHistory.length === 0 && (
                  <p className="text-gray-500 dark:text-gray-400 text-center py-4 transition-colors duration-300">
                    No entries yet. Start tracking today!
                  </p>
                )}
              </div>
            </div>

            {/* Tips */}
            <div className="bg-gradient-to-br from-purple-100 to-pink-100 dark:from-purple-900/30 dark:to-pink-900/30 rounded-2xl shadow-lg p-6 transition-colors duration-300">
              <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-3 transition-colors duration-300">
                💡 Tips
              </h3>
              <ul className="space-y-2 text-sm text-gray-700 dark:text-gray-300 transition-colors duration-300">
                <li className="flex items-start gap-2">
                  <span>•</span>
                  <span>Track your mood daily for best insights</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>•</span>
                  <span>Note patterns between activities and moods</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>•</span>
                  <span>Earn 50 NeuraCoins for 7-day streaks!</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default MoodTracker;
