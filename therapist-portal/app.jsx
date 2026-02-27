<<<<<<< HEAD
const API_URL = 'http://localhost:8000';
let currentTherapist = null;
let currentPatient = null;

// Check if already logged in
window.onload = () => {
    const therapist = localStorage.getItem('therapist');
    if (therapist) {
        currentTherapist = JSON.parse(therapist);
        showDashboard();
    }
};

// Handle Login
async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const response = await fetch(`${API_URL}/api/therapist/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        if (!response.ok) {
            throw new Error('Login failed');
        }
        
        const data = await response.json();
        currentTherapist = data.therapist;
        localStorage.setItem('therapist', JSON.stringify(currentTherapist));
        localStorage.setItem('therapist_token', data.token);
        
        showDashboard();
    } catch (error) {
        alert('Login failed. Please check your credentials.');
    }
}

// Logout
function logout() {
    localStorage.removeItem('therapist');
    localStorage.removeItem('therapist_token');
    currentTherapist = null;
    location.reload();
}

// Show Dashboard
async function showDashboard() {
    document.getElementById('login-section').classList.add('hidden');
    document.getElementById('dashboard-section').classList.remove('hidden');
    document.getElementById('chat-section').classList.add('hidden');
    document.getElementById('therapist-name').textContent = currentTherapist.name;
    document.getElementById('welcome-name').textContent = currentTherapist.name;
    
    await loadPatients();
    await loadPendingAppointments();
}

// Load Patients
async function loadPatients() {
    try {
        const token = localStorage.getItem('therapist_token');
        const response = await fetch(`${API_URL}/api/therapist/patients`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const data = await response.json();
        const patients = data.patients || [];
        
        document.getElementById('total-patients').textContent = patients.length;
        
        const patientsList = document.getElementById('patients-list');
        patientsList.innerHTML = '';
        
        if (patients.length === 0) {
            patientsList.innerHTML = `
                <div class="text-center py-12">
                    <div class="text-6xl mb-4">👥</div>
                    <p class="text-gray-600 dark:text-gray-400">No patients yet. Patients will appear here once they opt in for your services.</p>
                </div>
            `;
            return;
        }
        
        patients.forEach(patient => {
            const patientCard = document.createElement('div');
            patientCard.className = 'border border-gray-200 dark:border-gray-600 rounded-xl p-5 hover:shadow-xl hover:border-purple-300 dark:hover:border-purple-500 transition cursor-pointer bg-gradient-to-br from-white to-purple-50 dark:from-gray-700 dark:to-purple-900/20';
            patientCard.onclick = () => openChat(patient);
            patientCard.innerHTML = `
                <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-4">
                        <div class="w-14 h-14 rounded-full bg-gradient-to-r from-purple-500 to-indigo-500 flex items-center justify-center text-white font-bold text-xl shadow-lg">
                            ${patient.username.charAt(0).toUpperCase()}
                        </div>
                        <div>
                            <h4 class="font-bold text-gray-800 dark:text-white text-lg">${patient.username}</h4>
                            <p class="text-sm text-gray-600 dark:text-gray-400">💬 Last: ${patient.last_message || 'No messages yet'}</p>
                        </div>
                    </div>
                    <button class="bg-gradient-to-r from-purple-600 to-indigo-600 text-white px-5 py-2.5 rounded-lg hover:from-purple-700 hover:to-indigo-700 transition shadow-lg font-semibold">
                        Open Chat 💬
                    </button>
                </div>
            `;
            patientsList.appendChild(patientCard);
        });
    } catch (error) {
        console.error('Error loading patients:', error);
    }
}

// Open Chat
async function openChat(patient) {
    currentPatient = patient;
    document.getElementById('dashboard-section').classList.add('hidden');
    document.getElementById('chat-section').classList.remove('hidden');
    document.getElementById('chat-patient-name').textContent = patient.username;
    
    await loadMessages();
    
    // Poll for new messages
    if (window.messageInterval) clearInterval(window.messageInterval);
    window.messageInterval = setInterval(loadMessages, 3000);
}

// Back to Dashboard
function backToDashboard() {
    if (window.messageInterval) clearInterval(window.messageInterval);
    currentPatient = null;
    showDashboard();
}

// Load Messages
async function loadMessages() {
    if (!currentPatient) return;
    
    try {
        const token = localStorage.getItem('therapist_token');
        const response = await fetch(`${API_URL}/api/therapist/messages/${currentPatient.user_id}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const data = await response.json();
        const messages = data.messages || [];
        
        const chatMessages = document.getElementById('chat-messages');
        chatMessages.innerHTML = '';
        
        if (messages.length === 0) {
            chatMessages.innerHTML = `
                <div class="text-center py-12">
                    <div class="text-6xl mb-4">💬</div>
                    <p class="text-gray-600 dark:text-gray-400">No messages yet. Start the conversation!</p>
                </div>
            `;
            return;
        }
        
        messages.forEach(msg => {
            const messageDiv = document.createElement('div');
            messageDiv.className = `flex ${msg.sender === 'therapist' ? 'justify-end' : 'justify-start'} fade-in`;
            messageDiv.innerHTML = `
                <div class="max-w-md px-5 py-3 rounded-2xl shadow-lg ${
                    msg.sender === 'therapist'
                        ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-br-none'
                        : 'bg-white text-gray-800 border border-gray-200 rounded-bl-none'
                }">
                    <p class="whitespace-pre-wrap text-sm">${msg.message}</p>
                    <p class="text-xs mt-1 ${msg.sender === 'therapist' ? 'text-purple-200' : 'text-gray-400'}">
                        ${new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </p>
                </div>
            `;
            chatMessages.appendChild(messageDiv);
        });
        
        chatMessages.scrollTop = chatMessages.scrollHeight;
    } catch (error) {
        console.error('Error loading messages:', error);
    }
}

// Send Message
async function sendMessage(event) {
    event.preventDefault();
    
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    
    if (!message || !currentPatient) return;
    
    try {
        const token = localStorage.getItem('therapist_token');
        await fetch(`${API_URL}/api/therapist/send-message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                user_id: currentPatient.user_id,
                message: message
            })
        });
        
        input.value = '';
        await loadMessages();
    } catch (error) {
        alert('Failed to send message');
    }
}

// Load Pending Appointments
async function loadPendingAppointments() {
    try {
        const token = localStorage.getItem('therapist_token');
        console.log('Loading pending appointments for therapist:', currentTherapist);
        
        const response = await fetch(`${API_URL}/api/therapist/pending-appointments`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (!response.ok) {
            console.error('Failed to fetch pending appointments:', response.status);
            return;
        }
        
        const data = await response.json();
        const appointments = data.appointments || [];
        
        console.log('Pending appointments:', appointments);
        
        // Update pending requests count
        document.getElementById('pending-requests').textContent = appointments.length;
        
        const appointmentsList = document.getElementById('pending-appointments-list');
        appointmentsList.innerHTML = '';
        
        if (appointments.length === 0) {
            appointmentsList.innerHTML = `
                <div class="text-center py-8">
                    <div class="text-5xl mb-3">✅</div>
                    <p class="text-gray-600 dark:text-gray-400">No pending appointment requests</p>
                </div>
            `;
            return;
        }
        
        appointments.forEach(apt => {
            const aptCard = document.createElement('div');
            aptCard.className = 'border-2 border-yellow-400 dark:border-yellow-600 bg-gradient-to-br from-yellow-50 to-orange-50 dark:from-yellow-900/30 dark:to-orange-900/30 rounded-xl p-5 hover:shadow-2xl transition';
            aptCard.innerHTML = `
                <div class="flex items-start justify-between">
                    <div class="flex items-start space-x-4 flex-1">
                        <div class="w-14 h-14 rounded-full bg-gradient-to-r from-yellow-400 to-orange-500 flex items-center justify-center text-white font-bold text-xl shadow-lg">
                            ${apt.username.charAt(0).toUpperCase()}
                        </div>
                        <div class="flex-1">
                            <h4 class="font-bold text-gray-800 dark:text-white text-xl mb-3">${apt.username}</h4>
                            <div class="bg-white/60 dark:bg-gray-700/60 rounded-lg p-3 space-y-2">
                                <p class="text-sm text-gray-700 dark:text-gray-300"><span class="font-semibold">📅 Date:</span> ${apt.date}</p>
                                <p class="text-sm text-gray-700 dark:text-gray-300"><span class="font-semibold">🕒 Time:</span> ${apt.time}</p>
                                <p class="text-sm text-gray-700 dark:text-gray-300"><span class="font-semibold">📋 Type:</span> <span class="px-2 py-1 bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300 rounded font-medium">${apt.type}</span></p>
                                ${apt.notes ? `<p class="text-sm text-gray-700 dark:text-gray-300"><span class="font-semibold">📝 Notes:</span> ${apt.notes}</p>` : ''}
                            </div>
                        </div>
                    </div>
                    <div class="flex gap-2 ml-4">
                        <button 
                            onclick="acceptAppointment(${apt.id})"
                            class="px-5 py-2.5 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg font-bold hover:from-green-600 hover:to-green-700 transition shadow-lg"
                        >
                            ✓ Accept
                        </button>
                        <button 
                            onclick="rejectAppointment(${apt.id})"
                            class="px-5 py-2.5 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-lg font-bold hover:from-red-600 hover:to-red-700 transition shadow-lg"
                        >
                            ✗ Reject
                        </button>
                    </div>
                </div>
            `;
            appointmentsList.appendChild(aptCard);
        });
    } catch (error) {
        console.error('Failed to load pending appointments:', error);
        document.getElementById('pending-requests').textContent = '!';
    }
}

// Accept Appointment
async function acceptAppointment(appointmentId) {
    try {
        const token = localStorage.getItem('therapist_token');
        const response = await fetch(`${API_URL}/api/therapist/appointments/${appointmentId}/accept`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            alert('✅ Appointment accepted successfully!');
            await loadPendingAppointments();
        }
    } catch (error) {
        alert('Failed to accept appointment');
    }
}

// Reject Appointment
async function rejectAppointment(appointmentId) {
    if (!confirm('Are you sure you want to reject this appointment?')) {
        return;
    }
    
    try {
        const token = localStorage.getItem('therapist_token');
        const response = await fetch(`${API_URL}/api/therapist/appointments/${appointmentId}/reject`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            alert('Appointment rejected');
            await loadPendingAppointments();
        }
    } catch (error) {
        alert('Failed to reject appointment');
    }
}

=======
const API_URL = 'http://localhost:8000';
let currentTherapist = null;
let currentPatient = null;

// Check if already logged in
window.onload = () => {
    const therapist = localStorage.getItem('therapist');
    if (therapist) {
        currentTherapist = JSON.parse(therapist);
        showDashboard();
    }
};

// Handle Login
async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const response = await fetch(`${API_URL}/api/therapist/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        if (!response.ok) {
            throw new Error('Login failed');
        }
        
        const data = await response.json();
        currentTherapist = data.therapist;
        localStorage.setItem('therapist', JSON.stringify(currentTherapist));
        localStorage.setItem('therapist_token', data.token);
        
        showDashboard();
    } catch (error) {
        alert('Login failed. Please check your credentials.');
    }
}

// Logout
function logout() {
    localStorage.removeItem('therapist');
    localStorage.removeItem('therapist_token');
    currentTherapist = null;
    location.reload();
}

// Show Dashboard
async function showDashboard() {
    document.getElementById('login-section').classList.add('hidden');
    document.getElementById('dashboard-section').classList.remove('hidden');
    document.getElementById('chat-section').classList.add('hidden');
    document.getElementById('therapist-name').textContent = currentTherapist.name;
    document.getElementById('welcome-name').textContent = currentTherapist.name;
    
    await loadPatients();
    await loadPendingAppointments();
}

// Load Patients
async function loadPatients() {
    try {
        const token = localStorage.getItem('therapist_token');
        const response = await fetch(`${API_URL}/api/therapist/patients`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const data = await response.json();
        const patients = data.patients || [];
        
        document.getElementById('total-patients').textContent = patients.length;
        
        const patientsList = document.getElementById('patients-list');
        patientsList.innerHTML = '';
        
        if (patients.length === 0) {
            patientsList.innerHTML = `
                <div class="text-center py-12">
                    <div class="text-6xl mb-4">👥</div>
                    <p class="text-gray-600 dark:text-gray-400">No patients yet. Patients will appear here once they opt in for your services.</p>
                </div>
            `;
            return;
        }
        
        patients.forEach(patient => {
            const patientCard = document.createElement('div');
            patientCard.className = 'border border-gray-200 dark:border-gray-600 rounded-xl p-5 hover:shadow-xl hover:border-purple-300 dark:hover:border-purple-500 transition cursor-pointer bg-gradient-to-br from-white to-purple-50 dark:from-gray-700 dark:to-purple-900/20';
            patientCard.onclick = () => openChat(patient);
            patientCard.innerHTML = `
                <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-4">
                        <div class="w-14 h-14 rounded-full bg-gradient-to-r from-purple-500 to-indigo-500 flex items-center justify-center text-white font-bold text-xl shadow-lg">
                            ${patient.username.charAt(0).toUpperCase()}
                        </div>
                        <div>
                            <h4 class="font-bold text-gray-800 dark:text-white text-lg">${patient.username}</h4>
                            <p class="text-sm text-gray-600 dark:text-gray-400">💬 Last: ${patient.last_message || 'No messages yet'}</p>
                        </div>
                    </div>
                    <button class="bg-gradient-to-r from-purple-600 to-indigo-600 text-white px-5 py-2.5 rounded-lg hover:from-purple-700 hover:to-indigo-700 transition shadow-lg font-semibold">
                        Open Chat 💬
                    </button>
                </div>
            `;
            patientsList.appendChild(patientCard);
        });
    } catch (error) {
        console.error('Error loading patients:', error);
    }
}

// Open Chat
async function openChat(patient) {
    currentPatient = patient;
    document.getElementById('dashboard-section').classList.add('hidden');
    document.getElementById('chat-section').classList.remove('hidden');
    document.getElementById('chat-patient-name').textContent = patient.username;
    
    await loadMessages();
    
    // Poll for new messages
    if (window.messageInterval) clearInterval(window.messageInterval);
    window.messageInterval = setInterval(loadMessages, 3000);
}

// Back to Dashboard
function backToDashboard() {
    if (window.messageInterval) clearInterval(window.messageInterval);
    currentPatient = null;
    showDashboard();
}

// Load Messages
async function loadMessages() {
    if (!currentPatient) return;
    
    try {
        const token = localStorage.getItem('therapist_token');
        const response = await fetch(`${API_URL}/api/therapist/messages/${currentPatient.user_id}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const data = await response.json();
        const messages = data.messages || [];
        
        const chatMessages = document.getElementById('chat-messages');
        chatMessages.innerHTML = '';
        
        if (messages.length === 0) {
            chatMessages.innerHTML = `
                <div class="text-center py-12">
                    <div class="text-6xl mb-4">💬</div>
                    <p class="text-gray-600 dark:text-gray-400">No messages yet. Start the conversation!</p>
                </div>
            `;
            return;
        }
        
        messages.forEach(msg => {
            const messageDiv = document.createElement('div');
            messageDiv.className = `flex ${msg.sender === 'therapist' ? 'justify-end' : 'justify-start'} fade-in`;
            messageDiv.innerHTML = `
                <div class="max-w-md px-5 py-3 rounded-2xl shadow-lg ${
                    msg.sender === 'therapist'
                        ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-br-none'
                        : 'bg-white text-gray-800 border border-gray-200 rounded-bl-none'
                }">
                    <p class="whitespace-pre-wrap text-sm">${msg.message}</p>
                    <p class="text-xs mt-1 ${msg.sender === 'therapist' ? 'text-purple-200' : 'text-gray-400'}">
                        ${new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </p>
                </div>
            `;
            chatMessages.appendChild(messageDiv);
        });
        
        chatMessages.scrollTop = chatMessages.scrollHeight;
    } catch (error) {
        console.error('Error loading messages:', error);
    }
}

// Send Message
async function sendMessage(event) {
    event.preventDefault();
    
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    
    if (!message || !currentPatient) return;
    
    try {
        const token = localStorage.getItem('therapist_token');
        await fetch(`${API_URL}/api/therapist/send-message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                user_id: currentPatient.user_id,
                message: message
            })
        });
        
        input.value = '';
        await loadMessages();
    } catch (error) {
        alert('Failed to send message');
    }
}

// Load Pending Appointments
async function loadPendingAppointments() {
    try {
        const token = localStorage.getItem('therapist_token');
        console.log('Loading pending appointments for therapist:', currentTherapist);
        
        const response = await fetch(`${API_URL}/api/therapist/pending-appointments`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (!response.ok) {
            console.error('Failed to fetch pending appointments:', response.status);
            return;
        }
        
        const data = await response.json();
        const appointments = data.appointments || [];
        
        console.log('Pending appointments:', appointments);
        
        // Update pending requests count
        document.getElementById('pending-requests').textContent = appointments.length;
        
        const appointmentsList = document.getElementById('pending-appointments-list');
        appointmentsList.innerHTML = '';
        
        if (appointments.length === 0) {
            appointmentsList.innerHTML = `
                <div class="text-center py-8">
                    <div class="text-5xl mb-3">✅</div>
                    <p class="text-gray-600 dark:text-gray-400">No pending appointment requests</p>
                </div>
            `;
            return;
        }
        
        appointments.forEach(apt => {
            const aptCard = document.createElement('div');
            aptCard.className = 'border-2 border-yellow-400 dark:border-yellow-600 bg-gradient-to-br from-yellow-50 to-orange-50 dark:from-yellow-900/30 dark:to-orange-900/30 rounded-xl p-5 hover:shadow-2xl transition';
            aptCard.innerHTML = `
                <div class="flex items-start justify-between">
                    <div class="flex items-start space-x-4 flex-1">
                        <div class="w-14 h-14 rounded-full bg-gradient-to-r from-yellow-400 to-orange-500 flex items-center justify-center text-white font-bold text-xl shadow-lg">
                            ${apt.username.charAt(0).toUpperCase()}
                        </div>
                        <div class="flex-1">
                            <h4 class="font-bold text-gray-800 dark:text-white text-xl mb-3">${apt.username}</h4>
                            <div class="bg-white/60 dark:bg-gray-700/60 rounded-lg p-3 space-y-2">
                                <p class="text-sm text-gray-700 dark:text-gray-300"><span class="font-semibold">📅 Date:</span> ${apt.date}</p>
                                <p class="text-sm text-gray-700 dark:text-gray-300"><span class="font-semibold">🕒 Time:</span> ${apt.time}</p>
                                <p class="text-sm text-gray-700 dark:text-gray-300"><span class="font-semibold">📋 Type:</span> <span class="px-2 py-1 bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300 rounded font-medium">${apt.type}</span></p>
                                ${apt.notes ? `<p class="text-sm text-gray-700 dark:text-gray-300"><span class="font-semibold">📝 Notes:</span> ${apt.notes}</p>` : ''}
                            </div>
                        </div>
                    </div>
                    <div class="flex gap-2 ml-4">
                        <button 
                            onclick="acceptAppointment(${apt.id})"
                            class="px-5 py-2.5 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg font-bold hover:from-green-600 hover:to-green-700 transition shadow-lg"
                        >
                            ✓ Accept
                        </button>
                        <button 
                            onclick="rejectAppointment(${apt.id})"
                            class="px-5 py-2.5 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-lg font-bold hover:from-red-600 hover:to-red-700 transition shadow-lg"
                        >
                            ✗ Reject
                        </button>
                    </div>
                </div>
            `;
            appointmentsList.appendChild(aptCard);
        });
    } catch (error) {
        console.error('Failed to load pending appointments:', error);
        document.getElementById('pending-requests').textContent = '!';
    }
}

// Accept Appointment
async function acceptAppointment(appointmentId) {
    try {
        const token = localStorage.getItem('therapist_token');
        const response = await fetch(`${API_URL}/api/therapist/appointments/${appointmentId}/accept`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            alert('✅ Appointment accepted successfully!');
            await loadPendingAppointments();
        }
    } catch (error) {
        alert('Failed to accept appointment');
    }
}

// Reject Appointment
async function rejectAppointment(appointmentId) {
    if (!confirm('Are you sure you want to reject this appointment?')) {
        return;
    }
    
    try {
        const token = localStorage.getItem('therapist_token');
        const response = await fetch(`${API_URL}/api/therapist/appointments/${appointmentId}/reject`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            alert('Appointment rejected');
            await loadPendingAppointments();
        }
    } catch (error) {
        alert('Failed to reject appointment');
    }
}

>>>>>>> 8f42418579ec6d512ce83ecf248d8ad6a4c96c7f
