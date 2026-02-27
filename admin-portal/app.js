// Admin Portal JavaScript

const API_URL = 'http://localhost:8000';

// Dark Mode Management
let isDarkMode = localStorage.getItem('adminDarkMode') === 'true';

function initTheme() {
    if (isDarkMode) {
        document.documentElement.classList.add('dark');
        document.getElementById('themeIcon').textContent = '☀️';
    } else {
        document.documentElement.classList.remove('dark');
        document.getElementById('themeIcon').textContent = '🌙';
    }
}

function toggleTheme() {
    isDarkMode = !isDarkMode;
    localStorage.setItem('adminDarkMode', isDarkMode);
    initTheme();
}

// Initialize theme on load
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
});

// Login Handler
document.getElementById('loginForm').addEventListener('submit', (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    if (username === 'admin1' && password === '123456') {
        // Store admin session
        localStorage.setItem('adminLoggedIn', 'true');
        
        // Hide login, show dashboard
        document.getElementById('loginScreen').classList.add('hidden');
        document.getElementById('adminDashboard').classList.remove('hidden');
        
        // Load dashboard data
        loadDashboardData();
    } else {
        document.getElementById('loginError').classList.remove('hidden');
        setTimeout(() => {
            document.getElementById('loginError').classList.add('hidden');
        }, 3000);
    }
});

// Check if already logged in
if (localStorage.getItem('adminLoggedIn') === 'true') {
    document.getElementById('loginScreen').classList.add('hidden');
    document.getElementById('adminDashboard').classList.remove('hidden');
    loadDashboardData();
}

// Logout Handler
document.getElementById('logoutBtn').addEventListener('click', () => {
    localStorage.removeItem('adminLoggedIn');
    document.getElementById('loginScreen').classList.remove('hidden');
    document.getElementById('adminDashboard').classList.add('hidden');
});

// Theme Toggle Handler
document.getElementById('themeToggle').addEventListener('click', toggleTheme);

// Tab Navigation
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;
        
        // Update active tab button
        document.querySelectorAll('.tab-btn').forEach(b => {
            b.classList.remove('active', 'text-purple-600', 'dark:text-purple-400', 'border-b-2', 'border-purple-600', 'dark:border-purple-400');
            b.classList.add('text-gray-600', 'dark:text-gray-400');
        });
        btn.classList.add('active', 'text-purple-600', 'dark:text-purple-400', 'border-b-2', 'border-purple-600', 'dark:border-purple-400');
        btn.classList.remove('text-gray-600', 'dark:text-gray-400');
        
        // Show active tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.add('hidden');
        });
        document.getElementById(tabName + 'Tab').classList.remove('hidden');
        
        // Load tab-specific data
        loadTabData(tabName);
    });
});

// Load Dashboard Data
async function loadDashboardData() {
    try {
        // Load all data
        await Promise.all([
            loadUsers(),
            loadTherapists(),
            loadSessions(),
            loadQuizResults()
        ]);
        
        updateStats();
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

let usersData = [];
let therapistsData = [];
let sessionsData = [];
let quizResultsData = [];

// Load Users
async function loadUsers() {
    try {
        const response = await fetch(`${API_URL}/api/admin/users`);
        if (response.ok) {
            usersData = await response.json();
            renderUsers(usersData);
        } else {
            // Fallback: Load from direct database query
            usersData = await loadUsersDirectly();
            renderUsers(usersData);
        }
    } catch (error) {
        console.error('Error loading users:', error);
        usersData = await loadUsersDirectly();
        renderUsers(usersData);
    }
}

async function loadUsersDirectly() {
    // This is a fallback - we'll create an admin API endpoint
    return [];
}

function renderUsers(users) {
    const tbody = document.getElementById('usersTableBody');
    tbody.innerHTML = '';
    
    users.forEach(user => {
        const row = document.createElement('tr');
        row.className = 'table-row-hover transition';
        row.innerHTML = `
            <td class="px-6 py-4">
                <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold">
                        ${user.username.charAt(0).toUpperCase()}
                    </div>
                    <span class="font-medium text-gray-800 dark:text-white">${user.username}</span>
                </div>
            </td>
            <td class="px-6 py-4 text-gray-600 dark:text-gray-300">${user.email}</td>
            <td class="px-6 py-4">
                ${user.is_premium ? 
                    '<span class="px-3 py-1 bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400 rounded-full text-xs font-semibold">⭐ Premium</span>' : 
                    '<span class="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded-full text-xs font-semibold">Free</span>'
                }
            </td>
            <td class="px-6 py-4">
                <span class="font-bold text-purple-600 dark:text-purple-400">${user.neuracoins} 💰</span>
            </td>
            <td class="px-6 py-4">
                <button onclick="togglePremium('${user.username}', ${!user.is_premium})" class="px-3 py-1 ${user.is_premium ? 'bg-red-500 hover:bg-red-600' : 'bg-green-500 hover:bg-green-600'} text-white rounded-lg text-xs font-medium transition">
                    ${user.is_premium ? 'Revoke' : 'Grant'} Premium
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Load Therapists
async function loadTherapists() {
    try {
        const response = await fetch(`${API_URL}/api/admin/therapists`);
        if (response.ok) {
            therapistsData = await response.json();
            renderTherapists(therapistsData);
        } else {
            therapistsData = await loadTherapistsDirectly();
            renderTherapists(therapistsData);
        }
    } catch (error) {
        console.error('Error loading therapists:', error);
        therapistsData = await loadTherapistsDirectly();
        renderTherapists(therapistsData);
    }
}

async function loadTherapistsDirectly() {
    return [];
}

function renderTherapists(therapists) {
    const tbody = document.getElementById('therapistsTableBody');
    tbody.innerHTML = '';
    
    therapists.forEach(therapist => {
        const row = document.createElement('tr');
        row.className = 'table-row-hover transition';
        row.innerHTML = `
            <td class="px-6 py-4">
                <div class="flex items-center space-x-3">
                    <div class="text-2xl">${therapist.avatar || '🩺'}</div>
                    <span class="font-medium text-gray-800 dark:text-white">${therapist.name}</span>
                </div>
            </td>
            <td class="px-6 py-4 text-gray-600 dark:text-gray-300">${therapist.email}</td>
            <td class="px-6 py-4">
                <span class="px-3 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 rounded-full text-xs font-semibold">
                    ${therapist.specialization}
                </span>
            </td>
            <td class="px-6 py-4 text-gray-600 dark:text-gray-300">${therapist.session_count || 0} sessions</td>
        `;
        tbody.appendChild(row);
    });
}

// Load Sessions
async function loadSessions() {
    try {
        const response = await fetch(`${API_URL}/api/admin/sessions`);
        if (response.ok) {
            sessionsData = await response.json();
            renderSessions(sessionsData);
        } else {
            sessionsData = await loadSessionsDirectly();
            renderSessions(sessionsData);
        }
    } catch (error) {
        console.error('Error loading sessions:', error);
        sessionsData = await loadSessionsDirectly();
        renderSessions(sessionsData);
    }
}

async function loadSessionsDirectly() {
    return [];
}

function renderSessions(sessions) {
    const tbody = document.getElementById('sessionsTableBody');
    tbody.innerHTML = '';
    
    sessions.forEach(session => {
        const statusColors = {
            'pending': 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400',
            'accepted': 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400',
            'rejected': 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400',
            'completed': 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400'
        };
        
        const row = document.createElement('tr');
        row.className = 'table-row-hover transition';
        row.innerHTML = `
            <td class="px-6 py-4 font-medium text-gray-800 dark:text-white">${session.user_username}</td>
            <td class="px-6 py-4 text-gray-600 dark:text-gray-300">${session.therapist_name}</td>
            <td class="px-6 py-4">
                <span class="px-3 py-1 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400 rounded-full text-xs font-semibold">
                    ${session.session_type}
                </span>
            </td>
            <td class="px-6 py-4 text-gray-600 dark:text-gray-300">${new Date(session.date + ' ' + session.time).toLocaleString()}</td>
            <td class="px-6 py-4">
                <span class="px-3 py-1 ${statusColors[session.status] || 'bg-gray-100 text-gray-700'} rounded-full text-xs font-semibold">
                    ${session.status}
                </span>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Load Quiz Results
async function loadQuizResults() {
    try {
        const response = await fetch(`${API_URL}/api/admin/quiz-results`);
        if (response.ok) {
            quizResultsData = await response.json();
            renderQuizResults(quizResultsData);
        } else {
            quizResultsData = await loadQuizResultsDirectly();
            renderQuizResults(quizResultsData);
        }
    } catch (error) {
        console.error('Error loading quiz results:', error);
        quizResultsData = await loadQuizResultsDirectly();
        renderQuizResults(quizResultsData);
    }
}

async function loadQuizResultsDirectly() {
    return [];
}

function renderQuizResults(results) {
    const tbody = document.getElementById('quizzesTableBody');
    tbody.innerHTML = '';
    
    const quizNames = {
        'phq9': 'PHQ-9 (Depression)',
        'gad7': 'GAD-7 (Anxiety)',
        'pss10': 'PSS-10 (Stress)'
    };
    
    results.forEach(result => {
        const row = document.createElement('tr');
        row.className = 'table-row-hover transition';
        row.innerHTML = `
            <td class="px-6 py-4 font-medium text-gray-800 dark:text-white">${result.user_username}</td>
            <td class="px-6 py-4 text-gray-600 dark:text-gray-300">${quizNames[result.quiz_type] || result.quiz_type}</td>
            <td class="px-6 py-4">
                <span class="font-bold text-purple-600 dark:text-purple-400">${result.score}</span>
            </td>
            <td class="px-6 py-4 text-gray-600 dark:text-gray-300">${result.result}</td>
            <td class="px-6 py-4 text-gray-600 dark:text-gray-300">${new Date(result.created_at).toLocaleDateString()}</td>
        `;
        tbody.appendChild(row);
    });
}

// Update Stats
function updateStats() {
    document.getElementById('totalUsers').textContent = usersData.length;
    document.getElementById('premiumUsers').textContent = usersData.filter(u => u.is_premium).length;
    document.getElementById('totalTherapists').textContent = therapistsData.length;
    document.getElementById('totalSessions').textContent = sessionsData.length;
}

// Load Tab Data
function loadTabData(tabName) {
    switch(tabName) {
        case 'users':
            renderUsers(usersData);
            break;
        case 'therapists':
            renderTherapists(therapistsData);
            break;
        case 'sessions':
            renderSessions(sessionsData);
            break;
        case 'quizzes':
            renderQuizResults(quizResultsData);
            break;
    }
}

// Toggle Premium (placeholder - needs backend API)
async function togglePremium(username, grantPremium) {
    try {
        const response = await fetch(`${API_URL}/api/admin/users/${username}/premium`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ is_premium: grantPremium })
        });
        
        if (response.ok) {
            // Reload users
            await loadUsers();
            updateStats();
            alert(`Premium ${grantPremium ? 'granted to' : 'revoked from'} ${username}`);
        } else {
            alert('Failed to update premium status. Admin API endpoint needed.');
        }
    } catch (error) {
        console.error('Error toggling premium:', error);
        alert('Failed to update premium status. Admin API endpoint needed.');
    }
}

// User Search
document.getElementById('userSearch').addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    const filteredUsers = usersData.filter(user => 
        user.username.toLowerCase().includes(searchTerm) || 
        user.email.toLowerCase().includes(searchTerm)
    );
    renderUsers(filteredUsers);
});
