// School Feedback Platform - Main JavaScript

// Global variables
let authToken = localStorage.getItem('authToken');
let currentUser = null;
let categories = [];
let subjects = [];

// DOM elements
const sections = {
    home: document.getElementById('homeSection'),
    login: document.getElementById('loginSection'),
    dashboard: document.getElementById('dashboardSection')
};

const buttons = {
    home: document.getElementById('homeBtn'),
    login: document.getElementById('loginBtn'),
    dashboard: document.getElementById('dashboardBtn'),
    logout: document.getElementById('logoutBtn')
};

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadInitialData();
});

function initializeApp() {
    // Check if user is logged in
    if (authToken) {
        showLoggedInState();
        loadUserInfo();
    } else {
        showLoggedOutState();
    }
    
    // Show home section by default
    showSection('home');
}

function setupEventListeners() {
    // Navigation
    buttons.home.addEventListener('click', () => showSection('home'));
    buttons.login.addEventListener('click', () => showSection('login'));
    buttons.dashboard.addEventListener('click', () => showSection('dashboard'));
    buttons.logout.addEventListener('click', logout);
    
    // Forms
    document.getElementById('feedbackForm').addEventListener('submit', handleFeedbackSubmit);
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    
    // Feedback text counter
    const feedbackText = document.getElementById('feedbackText');
    const charCounter = document.querySelector('.char-counter');
    feedbackText.addEventListener('input', function() {
        const count = this.value.length;
        charCounter.textContent = `${count}/1000 karakters`;
        
        // Real-time sentiment preview
        if (count > 10) {
            showSentimentPreview(this.value);
        } else {
            hideSentimentPreview();
        }
    });
    
    // Dashboard filters
    document.getElementById('applyFilters').addEventListener('click', loadFeedbackData);
}

async function loadInitialData() {
    try {
        // Load categories
        const categoriesResponse = await fetch('http://localhost:8000/categories');
        categories = await categoriesResponse.json();
        populateSelect('category', categories);
        populateSelect('filterCategory', categories);
        
        // Load subjects
        const subjectsResponse = await fetch('http://localhost:8000/subjects');
        subjects = await subjectsResponse.json();
        populateSelect('subject', subjects);
        populateSelect('filterSubject', subjects);
        
    } catch (error) {
        console.error('Error loading initial data:', error);
        showToast('Fout bij het laden van gegevens', 'error');
    }
}

function populateSelect(selectId, options) {
    const select = document.getElementById(selectId);
    const currentOptions = select.querySelectorAll('option:not(:first-child)');
    currentOptions.forEach(option => option.remove());
    
    options.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option.id;
        optionElement.textContent = option.name;
        select.appendChild(optionElement);
    });
}

async function handleFeedbackSubmit(e) {
    e.preventDefault();
    
    const formData = {
        text: document.getElementById('feedbackText').value,
        category_id: parseInt(document.getElementById('category').value),
        subject_id: parseInt(document.getElementById('subject').value)
    };
    
    // Validate form
    const validation = FormValidator.validateForm(formData, {
        text: [
            (value) => FormValidator.validateRequired(value, 'Feedback tekst'),
            (value) => FormValidator.validateFeedbackText(value)
        ],
        category_id: [(value) => FormValidator.validateRequired(value.toString(), 'Categorie')],
        subject_id: [(value) => FormValidator.validateRequired(value.toString(), 'Vak')]
    });
    
    if (!validation.isValid) {
        Object.keys(validation.errors).forEach(field => {
            const fieldElement = document.getElementById(field === 'text' ? 'feedbackText' : field);
            FormValidator.showFieldError(fieldElement, validation.errors[field]);
        });
        return;
    }
    
    // Clear previous errors
    ['feedbackText', 'category', 'subject'].forEach(field => {
        FormValidator.clearFieldError(document.getElementById(field));
    });
    
    const submitBtn = e.target.querySelector('button[type="submit"]');
    submitBtn.classList.add('loading');
    
    try {
        const response = await fetch('http://localhost:8000/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            const result = await response.json();
            showToast('Feedback succesvol verstuurd! Bedankt voor je bijdrage.', 'success');
            
            // Reset form
            document.getElementById('feedbackForm').reset();
            document.querySelector('.char-counter').textContent = '0/1000 karakters';
            hideSentimentPreview();
            
            // Show sentiment result
            showSentimentResult(result.sentiment);
            
        } else {
            throw new Error('Fout bij het versturen van feedback');
        }
    } catch (error) {
        console.error('Error submitting feedback:', error);
        showToast('Er is een fout opgetreden. Probeer het opnieuw.', 'error');
    } finally {
        submitBtn.classList.remove('loading');
    }
}

async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    const submitBtn = e.target.querySelector('button[type="submit"]');
    submitBtn.classList.add('loading');
    
    try {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        
        const response = await fetch('http://localhost:8000/auth/login', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const result = await response.json();
            authToken = result.access_token;
            localStorage.setItem('authToken', authToken);
            
            showToast('Succesvol ingelogd!', 'success');
            showLoggedInState();
            await loadUserInfo();
            showSection('dashboard');
            
            // Reset login form
            document.getElementById('loginForm').reset();
            
        } else {
            throw new Error('Ongeldige inloggegevens');
        }
    } catch (error) {
        console.error('Login error:', error);
        showToast('Inloggen mislukt. Controleer je gegevens.', 'error');
    } finally {
        submitBtn.classList.remove('loading');
    }
}

async function loadUserInfo() {
    if (!authToken) return;
    
    try {
        const response = await fetch('http://localhost:8000/auth/me', {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (response.ok) {
            currentUser = await response.json();
            console.log('Current user:', currentUser);
        } else {
            // Token might be expired
            logout();
        }
    } catch (error) {
        console.error('Error loading user info:', error);
        logout();
    }
}

function logout() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('authToken');
    showLoggedOutState();
    showSection('home');
    showToast('Succesvol uitgelogd', 'info');
}

function showLoggedInState() {
    buttons.login.style.display = 'none';
    buttons.dashboard.style.display = 'inline-block';
    buttons.logout.style.display = 'inline-block';
}

function showLoggedOutState() {
    buttons.login.style.display = 'inline-block';
    buttons.dashboard.style.display = 'none';
    buttons.logout.style.display = 'none';
}

function showSection(sectionName) {
    // Hide all sections
    Object.values(sections).forEach(section => {
        section.classList.remove('active');
    });
    
    // Remove active class from all buttons
    Object.values(buttons).forEach(button => {
        button.classList.remove('active');
    });
    
    // Show selected section
    sections[sectionName].classList.add('active');
    buttons[sectionName].classList.add('active');
    
    // Load section-specific data
    if (sectionName === 'dashboard' && authToken) {
        loadDashboardData();
    }
}

async function loadDashboardData() {
    try {
        // Load analytics
        const analyticsResponse = await fetch('http://localhost:8000/analytics', {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (analyticsResponse.ok) {
            const analytics = await analyticsResponse.json();
            updateDashboardStats(analytics);
        }
        
        // Load feedback data
        await loadFeedbackData();
        
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showToast('Fout bij het laden van dashboard gegevens', 'error');
    }
}

function updateDashboardStats(analytics) {
    document.getElementById('totalFeedback').textContent = analytics.total_feedback;
    document.getElementById('avgSentiment').textContent = analytics.average_sentiment.toFixed(2);
    
    const sentiment = analytics.sentiment_distribution;
    document.getElementById('positiveFeedback').textContent = sentiment.Positive || 0;
    document.getElementById('negativeFeedback').textContent = sentiment.Negative || 0;
    document.getElementById('neutralFeedback').textContent = sentiment.Neutral || 0;
}

async function loadFeedbackData() {
    if (!authToken) return;
    
    const filters = {
        category_id: document.getElementById('filterCategory').value,
        subject_id: document.getElementById('filterSubject').value,
        sentiment: document.getElementById('filterSentiment').value
    };
    
    // Build query string
    const params = new URLSearchParams();
    Object.keys(filters).forEach(key => {
        if (filters[key]) {
            params.append(key, filters[key]);
        }
    });
    
    try {
        const response = await fetch(`http://localhost:8000/feedback?${params}`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (response.ok) {
            const feedbackList = await response.json();
            displayFeedbackList(feedbackList);
        }
    } catch (error) {
        console.error('Error loading feedback data:', error);
        showToast('Fout bij het laden van feedback', 'error');
    }
}

function displayFeedbackList(feedbackList) {
    const container = document.getElementById('feedbackList');
    
    if (feedbackList.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #718096;">Geen feedback gevonden met de huidige filters.</p>';
        return;
    }
    
    container.innerHTML = feedbackList.map(feedback => `
        <div class="feedback-item ${feedback.sentiment_label.toLowerCase()}">
            <div class="feedback-meta">
                <span>${feedback.category} - ${feedback.subject}</span>
                <span class="sentiment-badge ${feedback.sentiment_label.toLowerCase()}">
                    ${feedback.sentiment_label} (${(feedback.sentiment_score || 0).toFixed(2)})
                </span>
            </div>
            <div class="feedback-text">${feedback.text}</div>
            <div style="font-size: 0.75rem; color: #a0aec0; margin-top: 0.5rem;">
                ${new Date(feedback.created_at).toLocaleString('nl-NL')}
            </div>
        </div>
    `).join('');
}

async function showSentimentPreview(text) {
    if (text.length < 10) return;
    
    try {
        const response = await fetch(`http://localhost:8000/test-sentiment?text=${encodeURIComponent(text)}`);
        if (response.ok) {
            const result = await response.json();
            const preview = document.getElementById('sentimentPreview');
            const label = preview.querySelector('.sentiment-label');
            const score = preview.querySelector('.sentiment-score');
            
            label.textContent = result.label;
            label.className = `sentiment-label ${result.label.toLowerCase()}`;
            score.textContent = `Score: ${result.score.toFixed(2)}`;
            
            preview.style.display = 'block';
        }
    } catch (error) {
        console.error('Error getting sentiment preview:', error);
    }
}

function hideSentimentPreview() {
    document.getElementById('sentimentPreview').style.display = 'none';
}

function showSentimentResult(sentiment) {
    const message = `Sentiment gedetecteerd: ${sentiment.label} (Score: ${sentiment.score.toFixed(2)}, Confidence: ${(sentiment.confidence * 100).toFixed(1)}%)`;
    showToast(message, 'info');
}

function showToast(message, type = 'info') {
    // Use UIComponents if available, otherwise fallback to alert
    if (typeof UIComponents !== 'undefined') {
        UIComponents.showToast(message, type);
    } else {
        alert(message);
    }
}

// Auto-refresh dashboard data every 30 seconds
setInterval(() => {
    if (authToken && sections.dashboard.classList.contains('active')) {
        loadDashboardData();
    }
}, 30000);
