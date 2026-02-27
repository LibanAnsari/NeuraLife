import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Navbar from './Navbar';

const API_URL = 'http://localhost:8000';

const journalPrompts = [
  "What am I grateful for today?",
  "What's weighing on my mind right now?",
  "What went well today?",
  "What do I need to forgive myself for?",
  "What am I looking forward to?",
  "How can I be kinder to myself?",
  "What did I learn today?",
  "What would make tomorrow better?",
];

const moods = ['😊', '😐', '😢', '😰', '😡', '💙', '🌟'];

function Journal({ setToken }) {
  const navigate = useNavigate();
  const [entries, setEntries] = useState([]);
  const [showNewEntry, setShowNewEntry] = useState(false);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [selectedPrompt, setSelectedPrompt] = useState('');
  const [selectedMood, setSelectedMood] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [showSuccess, setShowSuccess] = useState(false);
  const [coinsEarned, setCoinsEarned] = useState(0);

  useEffect(() => {
    fetchEntries();
  }, []);

  const fetchEntries = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/journal/entries`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setEntries(response.data.entries);
    } catch (err) {
      console.error('Error fetching journal entries:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!content.trim()) {
      alert('Please write something in your journal');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${API_URL}/api/journal/entry`,
        {
          title: title || 'Untitled Entry',
          content,
          prompt: selectedPrompt,
          mood: selectedMood
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      setCoinsEarned(response.data.coins_earned);
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);

      // Reset form
      setTitle('');
      setContent('');
      setSelectedPrompt('');
      setSelectedMood('');
      setShowNewEntry(false);

      // Refresh entries
      fetchEntries();
    } catch (err) {
      console.error('Error creating journal entry:', err);
      alert('Failed to save journal entry');
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this entry?')) return;

    try {
      const token = localStorage.getItem('token');
      await axios.delete(`${API_URL}/api/journal/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchEntries();
    } catch (err) {
      console.error('Error deleting entry:', err);
    }
  };

  const filteredEntries = entries.filter(entry =>
    entry.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    entry.content.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-300">
      <Navbar setToken={setToken} />

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8 flex items-center justify-between">
          <div>
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
              📔 Journal
            </h1>
            <p className="text-gray-600 dark:text-gray-300 transition-colors duration-300">
              Express your thoughts and feelings privately
            </p>
          </div>

          <button
            onClick={() => setShowNewEntry(!showNewEntry)}
            className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-3 rounded-xl font-semibold hover:from-purple-700 hover:to-pink-700 transition-all duration-300 transform hover:scale-105 shadow-lg"
          >
            {showNewEntry ? 'Cancel' : '+ New Entry'}
          </button>
        </div>

        {/* Success Message */}
        {showSuccess && (
          <div className="mb-6 bg-green-100 dark:bg-green-900/30 border-2 border-green-500 rounded-xl p-4 animate-bounce transition-colors duration-300">
            <div className="flex items-center gap-3">
              <span className="text-4xl">✅</span>
              <div>
                <p className="text-green-800 dark:text-green-200 font-semibold transition-colors duration-300">
                  Journal entry saved!
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

        {/* New Entry Form */}
        {showNewEntry && (
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8 mb-8 transition-colors duration-300">
            <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-100 mb-6 transition-colors duration-300">
              Write a New Entry
            </h2>

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Mood Selection */}
              <div>
                <label className="block text-gray-700 dark:text-gray-300 font-semibold mb-2 transition-colors duration-300">
                  How are you feeling?
                </label>
                <div className="flex gap-2">
                  {moods.map(mood => (
                    <button
                      key={mood}
                      type="button"
                      onClick={() => setSelectedMood(mood)}
                      className={`text-3xl p-3 rounded-lg transition-all duration-300 ${
                        selectedMood === mood
                          ? 'bg-purple-100 dark:bg-purple-900/40 scale-125'
                          : 'hover:bg-gray-100 dark:hover:bg-gray-700'
                      }`}
                    >
                      {mood}
                    </button>
                  ))}
                </div>
              </div>

              {/* Prompt Selection */}
              <div>
                <label className="block text-gray-700 dark:text-gray-300 font-semibold mb-2 transition-colors duration-300">
                  Need a prompt? (optional)
                </label>
                <select
                  value={selectedPrompt}
                  onChange={(e) => setSelectedPrompt(e.target.value)}
                  className="w-full px-4 py-3 border-2 border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 dark:bg-gray-700 dark:text-gray-100 transition-colors duration-300"
                >
                  <option value="">Select a writing prompt...</option>
                  {journalPrompts.map((prompt, idx) => (
                    <option key={idx} value={prompt}>{prompt}</option>
                  ))}
                </select>
              </div>

              {/* Title */}
              <div>
                <label className="block text-gray-700 dark:text-gray-300 font-semibold mb-2 transition-colors duration-300">
                  Title (optional)
                </label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Give your entry a title..."
                  className="w-full px-4 py-3 border-2 border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 dark:bg-gray-700 dark:text-gray-100 transition-colors duration-300"
                />
              </div>

              {/* Content */}
              <div>
                <label className="block text-gray-700 dark:text-gray-300 font-semibold mb-2 transition-colors duration-300">
                  {selectedPrompt || 'What\'s on your mind?'}
                </label>
                <textarea
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  rows="10"
                  placeholder="Start writing..."
                  className="w-full px-4 py-3 border-2 border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 dark:bg-gray-700 dark:text-gray-100 transition-colors duration-300"
                  required
                />
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-2 transition-colors duration-300">
                  {content.length} characters
                </p>
              </div>

              <button
                type="submit"
                className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-4 rounded-xl font-semibold hover:from-purple-700 hover:to-pink-700 transition-all duration-300 transform hover:scale-105 shadow-lg"
              >
                Save Entry
              </button>
            </form>
          </div>
        )}

        {/* Search */}
        <div className="mb-6">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="🔍 Search entries..."
            className="w-full px-6 py-4 border-2 border-gray-300 dark:border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 dark:bg-gray-700 dark:text-gray-100 text-lg transition-colors duration-300"
          />
        </div>

        {/* Entries List */}
        <div className="space-y-4">
          {filteredEntries.length === 0 && (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">📝</div>
              <h3 className="text-xl font-semibold text-gray-800 dark:text-gray-100 mb-2 transition-colors duration-300">
                No journal entries yet
              </h3>
              <p className="text-gray-600 dark:text-gray-400 transition-colors duration-300">
                Start writing to express your thoughts and feelings
              </p>
            </div>
          )}

          {filteredEntries.map(entry => (
            <div
              key={entry.id}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 transition-all duration-300 hover:shadow-xl border-2 border-transparent hover:border-purple-300 dark:hover:border-purple-600"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  {entry.mood && <span className="text-3xl">{entry.mood}</span>}
                  <div>
                    <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100 transition-colors duration-300">
                      {entry.title}
                    </h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400 transition-colors duration-300">
                      {new Date(entry.created_at).toLocaleDateString('en-US', {
                        weekday: 'long',
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => handleDelete(entry.id)}
                  className="text-red-500 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300 transition-colors duration-300"
                >
                  🗑️
                </button>
              </div>

              {entry.prompt && (
                <div className="mb-3 p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg transition-colors duration-300">
                  <p className="text-sm text-purple-700 dark:text-purple-300 font-semibold transition-colors duration-300">
                    💭 {entry.prompt}
                  </p>
                </div>
              )}

              <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap transition-colors duration-300">
                {entry.content}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Journal;
