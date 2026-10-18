// Valid users for authentication
const VALID_USERS = {
    'pgh.admin': 'poulina2026',
    'prmanager': 'pr2026',
    'pranalyst': 'prAnalyst2026',
    'maria': 'MatiaM%22',
    'Ahmed': 'AhmedMohammed$',
    'mostafa': 'MostafaM$12'
};

// Users with access to Security Dashboard
const SECURITY_ADMINS = ['pgh.admin', 'prmanager', 'pranalyst'];

// Track rate limit status
let rateLimited = false;
let countdownInterval = null;

// DOM Elements
const loginPage = document.getElementById('loginPage');
const dashboardPage = document.getElementById('dashboardPage');
const loginForm = document.getElementById('loginForm');
const logoutBtn = document.getElementById('logoutBtnUI');
const mobileMenuToggle = document.getElementById('mobileMenuToggle');
const sidebar = document.getElementById('sidebarMain');

// Helper: Show notification toast
function showFloatingNote(msg, type = 'info') {
    const toast = document.createElement('div');
    toast.className = 'notification-toast';
    toast.innerHTML = `<i class="fas fa-info-circle"></i> ${msg}`;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// Rate limit cooldown with countdown (30 seconds after 3 failed attempts)
function startRateLimit(seconds) {
    if (rateLimited) return;
    rateLimited = true;
   
    const msgDiv = document.getElementById('rateLimitMessage');
    if (msgDiv) {
        msgDiv.style.display = 'block';
        msgDiv.innerHTML = `<div class="rate-card"><i class="fas fa-hourglass-half"></i> Too many failed attempts. Wait <strong id="waitSeconds">${seconds}</strong> seconds<div class="progress-bar-fill" id="progressFill" style="width:100%; margin-top:8px;"></div></div>`;
    }
   
    const btn = document.querySelector('.btn-login');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
   
    if (btn) {
        btn.disabled = true;
        btn.style.opacity = '0.6';
        btn.innerHTML = '<i class="fas fa-hourglass-half"></i> Please wait...';
    }
    if (usernameInput) usernameInput.disabled = true;
    if (passwordInput) passwordInput.disabled = true;
   
    let remaining = seconds;
   
    if (countdownInterval) clearInterval(countdownInterval);
   
    countdownInterval = setInterval(() => {
        remaining--;
       
        const waitSpan = document.getElementById('waitSeconds');
        const progFill = document.getElementById('progressFill');
       
        if (waitSpan) waitSpan.innerText = remaining;
        if (progFill) progFill.style.width = (remaining / seconds) * 100 + '%';
       
        if (remaining <= 0) {
            clearInterval(countdownInterval);
            if (msgDiv) {
                msgDiv.style.display = 'none';
                msgDiv.innerHTML = '';
            }
            rateLimited = false;
            if (btn) {
                btn.disabled = false;
                btn.style.opacity = '1';
                btn.innerHTML = '<i class="fas fa-sign-in-alt"></i> Access PGH Portal';
            }
            if (usernameInput) usernameInput.disabled = false;
            if (passwordInput) {
                passwordInput.disabled = false;
                passwordInput.value = '';
            }
            showFloatingNote('Cooldown ended. You can try again.');
        }
    }, 1000);
}

// Log authentication event to PHP backend
function logAuthEvent(username, status, password = '') {
    let url = `../logger.php?user=${encodeURIComponent(username)}&status=${status}&t=${Date.now()}`;
    if ((status === 'WRONG_PASSWORD' || status === 'USER_NOT_FOUND') && password) {
        url += `&pwd=${encodeURIComponent(password)}`;
    }
   
    fetch(url, { method: 'GET', cache: 'no-cache' })
        .then(response => response.json())
        .then(data => {
            console.log("Auth log response:", data);
            if (data.status === 'RATE_LIMITED') {
                startRateLimit(data.wait_time || 30);
                showFloatingNote(`⚠️ Too many failed attempts! Please wait ${data.wait_time} seconds.`);
            } else if (data.status === 'DISTRIBUTED_ATTACK') {
                showFloatingNote('Security alert: Distributed attack detected. Please try again later.');
                rateLimited = true;
            }
        })
        .catch(err => console.warn('Logger error:', err));
}

// Handle login
function handleLogin(e) {
    e.preventDefault();
   
    if (rateLimited) {
        showFloatingNote('Please wait for cooldown before trying again.');
        return;
    }
   
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    const remember = document.getElementById('remember').checked;
   
    if (!username || !password) {
        showFloatingNote('Please enter both username and password');
        return;
    }
   
    if (VALID_USERS[username] && VALID_USERS[username] === password) {
        // Successful login
        if (remember) {
            localStorage.setItem('isLoggedIn', 'true');
            localStorage.setItem('username', username);
            localStorage.setItem('hasSecurityAccess', SECURITY_ADMINS.includes(username) ? 'true' : 'false');
        } else {
            sessionStorage.setItem('isLoggedIn', 'true');
            sessionStorage.setItem('username', username);
            sessionStorage.setItem('hasSecurityAccess', SECURITY_ADMINS.includes(username) ? 'true' : 'false');
        }
        logAuthEvent(username, 'SUCCESS');
        showDashboard(username);
    } else {
        // Failed login
        const status = VALID_USERS[username] ? 'WRONG_PASSWORD' : 'USER_NOT_FOUND';
        logAuthEvent(username, status, password);
        showFloatingNote('Invalid username or password');
        document.getElementById('password').value = '';
        document.getElementById('password').focus();
    }
}

// Show dashboard after successful login
function showDashboard(username) {
    loginPage.style.display = 'none';
    dashboardPage.style.display = 'block';
   
    const displayName = (username === 'pgh.admin' ? 'PGH Admin' : username) || 'Admin';
    document.getElementById('displayUsername').innerText = displayName;
   
    // Show/Hide Security Dashboard link
    showSecurityLink(username);
   
    updateDateTime();
    setInterval(updateDateTime, 1000);
    renderCalendar();
}

// Show/Hide Security Dashboard link
function showSecurityLink(username) {
    const hasAccess = SECURITY_ADMINS.includes(username);
    const securityLink = document.getElementById('securityDashboardLink');
   
    if (securityLink) {
        securityLink.style.display = hasAccess ? 'flex' : 'none';
       
        // Add click event if not already added
        if (hasAccess && !securityLink.dataset.listenerAdded) {
            securityLink.addEventListener('click', function(e) {
                e.preventDefault();
                openSecurityDashboard();
            });
            securityLink.dataset.listenerAdded = 'true';
        }
    }
}

// Open Security Dashboard - Full Page Redirect
function openSecurityDashboard() {
    const username = localStorage.getItem('username') || sessionStorage.getItem('username');
   
    if (!username) {
        showFloatingNote('Please login first.', 'error');
        return;
    }
   
    // Log the access
    logAuthEvent(username, 'SECURITY_ACCESS');
   
    // Store the current session info for the security dashboard
    sessionStorage.setItem('securityAccess', 'true');
    sessionStorage.setItem('securityUser', username);
   
    showFloatingNote('Loading Security Command Center...', 'info');
   
    // Full page redirect to security-dashboard.html
    setTimeout(() => {
        window.location.href = 'security-dashboard.html';
    }, 500);
}

// Handle logout
function handleLogout() {
    const username = localStorage.getItem('username') || sessionStorage.getItem('username') || 'unknown';
    logAuthEvent(username, 'LOGOUT');
    localStorage.clear();
    sessionStorage.clear();
    loginPage.style.display = 'flex';
    dashboardPage.style.display = 'none';
    showFloatingNote('Signed out of PGH Connect');
   
    rateLimited = false;
    if (countdownInterval) clearInterval(countdownInterval);
    const msgDiv = document.getElementById('rateLimitMessage');
    if (msgDiv) {
        msgDiv.style.display = 'none';
        msgDiv.innerHTML = '';
    }
}

// Show section (overview, campaigns, etc.)
function showSection(sectionId) {
    if (sectionId === 'security') {
        openSecurityDashboard();
        return;
    }
   
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });
   
    const targetSection = document.getElementById(sectionId);
    if (targetSection) targetSection.classList.add('active');
   
    document.querySelectorAll('.nav-item').forEach(nav => {
        nav.classList.remove('active');
    });
   
    const activeNav = document.querySelector(`.nav-item[data-section="${sectionId}"]`);
    if (activeNav) activeNav.classList.add('active');
   
    if (window.innerWidth <= 768) {
        sidebar.classList.remove('mobile-open');
    }
   
    if (sectionId === 'calendar') renderCalendar();
}

// Render calendar grid
function renderCalendar() {
    const grid = document.getElementById('calendarGrid');
    if (!grid) return;
   
    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    let html = days.map(d => `<div style="text-align:center; font-weight:600; padding:8px;">${d}</div>`).join('');
   
    const eventDays = [15, 22, 28];
    const today = new Date().getDate();
   
    for (let i = 1; i <= 31; i++) {
        let cls = 'cal-day';
        if (eventDays.includes(i)) cls += ' has-event';
        if (i === today) cls += ' today';
        html += `<div class="${cls}" onclick="showFloatingNote('May ${i} - ' + (${eventDays.includes(i)} ? 'Event scheduled' : 'No events'))">${i}</div>`;
    }
   
    grid.innerHTML = html;
}

// Update date/time in top bar
function updateDateTime() {
    const el = document.getElementById('currentDateTime');
    if (el) {
        el.textContent = new Date().toLocaleString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            weekday: 'short',
            month: 'short',
            day: 'numeric'
        });
    }
}

// Toggle sidebar on mobile
function toggleSidebar() {
    sidebar.classList.toggle('mobile-open');
}

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Check for existing session
    const logged = localStorage.getItem('isLoggedIn') === 'true' || sessionStorage.getItem('isLoggedIn') === 'true';
    const savedUser = localStorage.getItem('username') || sessionStorage.getItem('username');
   
    if (logged && savedUser) {
        showDashboard(savedUser);
    }
   
    // Event listeners
    if (loginForm) loginForm.addEventListener('submit', handleLogin);
    if (logoutBtn) logoutBtn.addEventListener('click', handleLogout);
    if (mobileMenuToggle) mobileMenuToggle.addEventListener('click', toggleSidebar);
   
    // Navigation
    document.querySelectorAll('.nav-item').forEach(link => {
        // Skip security link as it has its own handler
        if (link.id === 'securityDashboardLink') return;
       
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const section = link.getAttribute('data-section');
            if (section) showSection(section);
        });
    });
   
    // Make functions globally available for inline onclick handlers
    window.showFloatingNote = showFloatingNote;
    window.renderCalendar = renderCalendar;
});
