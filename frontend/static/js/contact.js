/**
 * CLG Vermögensschutz - Contact Form JavaScript
 * Handles form submission, validation, error handling, and API communication.
 */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contactForm');
    const statusDiv = document.getElementById('formStatus');
    const submitBtn = document.querySelector('.btn-submit');

    if (!form || !statusDiv) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Disable button during submission
        submitBtn.disabled = true;
        submitBtn.textContent = 'Wird gesendet...';
        statusDiv.className = 'form-status';
        statusDiv.style.display = 'none';

        // Collect form data
        const formData = new FormData(form);
        const data = {
            name: formData.get('name'),
            email: formData.get('email'),
            phone: formData.get('phone') || '',
            assets_range: formData.get('assets_range') || '',
            message: formData.get('message') || ''
        };

        // Basic validation
        if (!data.name || data.name.length < 2) {
            showStatus('Bitte geben Sie Ihren Namen ein (min. 2 Zeichen).', 'error');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Beratung anfragen';
            return;
        }

        if (!isValidEmail(data.email)) {
            showStatus('Bitte geben Sie eine gültige E-Mail-Adresse ein.', 'error');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Beratung anfragen';
            return;
        }

        try {
            // Determine API base URL (local or sslip.io)
            const apiUrl = getApiBaseUrl();
            console.log('Submitting to:', `${apiUrl}/leads/submit`);

            const response = await fetch(`${apiUrl}/leads/submit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                const result = await response.json();
                console.log('Lead submitted:', result);
                showStatus(
                    `Vielen Dank, ${data.name}! Wir haben Ihre Anfrage erhalten und melden uns innerhalb von 24 Stunden.`,
                    'success'
                );
                form.reset();
            } else {
                const errorData = await response.json().catch(() => ({}));
                const message = errorData.detail || 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.';
                showStatus(message, 'error');
            }
        } catch (error) {
            console.error('Submission failed:', error);
            showStatus(
                'Verbindung fehlgeschlagen. Bitte prüfen Sie Ihre Internetverbindung und versuchen Sie es erneut.',
                'error'
            );
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Beratung anfragen';
        }
    });
});

/**
 * Validate email format
 */
function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

/**
 * Determine API base URL based on current hostname
 */
function getApiBaseUrl() {
    const hostname = window.location.hostname;

    // For sslip.io testing: replace with your actual IP
    if (hostname.includes('sslip.io')) {
        return 'https://YOUR_IP.sslip.io'; // TODO: Replace YOUR_IP with actual IP
    }

    // Default to local backend
    return '/api';
}

/**
 * Show status message for the contact form
 */
function showStatus(message, type) {
    const statusDiv = document.getElementById('formStatus');
    if (!statusDiv) return;

    statusDiv.className = `form-status ${type}`;
    statusDiv.style.display = 'block';
    statusDiv.innerHTML = `<p>${escapeHtml(message)}</p>`;

    // Auto-hide success messages after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            statusDiv.style.display = 'none';
        }, 8000);
    }
}

/**
 * Escape HTML to prevent XSS in status messages
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

console.log('CLG Vermögensschutz Contact Form initialized.');