/**
 * CLG Vermoegenschutz - Contact Form JavaScript
 * Handles form submission, validation, error handling, and API communication.
 * Supports both localhost and SSLIP.io testing environments.
 */

(function() {
    "use strict";

     // === CONFIG ===
     const API_BASE_URL = detectApiBaseUrl();

     document.addEventListener('DOMContentLoaded', function() {
         const form = document.getElementById('contactForm');
         const statusDiv = document.getElementById('formStatus');
         const submitBtn = document.querySelector('.btn-submit');

         if (!form || !statusDiv || !submitBtn) return;

         form.addEventListener('submit', async function(e) {
              e.preventDefault();

              // Disable button and show loading state
             submitBtn.disabled = true;
             submitBtn.textContent = 'Wird gesendet...';
             setStatus(statusDiv, '', '');

              // Collect form data
             const name = document.getElementById('name').value.trim();
             const email = document.getElementById('email').value.trim();
             const phone = document.getElementById('phone').value.trim();
             const assetsRange = document.getElementById('assets_range')?.value || '';
             const message = document.getElementById('message').value.trim();

              // Validation
             if (name.length < 2) {
                 setStatus(statusDiv, 'Bitte geben Sie Ihren vollen Namen ein (min. 2 Zeichen).', 'error');
                 resetButton(submitBtn);
                 return;
              }

             if (!isValidEmail(email)) {
                 setStatus(statusDiv, 'Bitte geben Sie eine gueltige E-Mail-Adresse ein.', 'error');
                 resetButton(submitBtn);
                 return;
              }

              // Submit to API
             try {
                 const data = await submitLead({
                     name: name,
                     email: email,
                     phone: phone,
                     assets_range: assetsRange,
                     message: message
                  });

                  if (data && data.status === 'success') {
                      setStatus(
                          statusDiv,
                          `Vielen Dank, ${escapeHtml(name)}! Wir haben Ihre Anfrage erhalten und melden uns innerhalb von 24 Stunden.`,
                          'success'
                      );
                      form.reset();
                   } else {
                       setStatus(statusDiv, 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es spaeter erneut.', 'error');
                   }
               } catch (error) {
                   console.error('Submission failed:', error);
                   setStatus(
                       statusDiv,
                       'Verbindung fehlgeschlagen. Bitte pruefen Sie Ihre Internetverbindung und versuchen Sie es erneut.',
                       'error'
                   );
               } finally {
                   resetButton(submitBtn);
               }
           });
       });

     // === API FUNCTIONS ===
     async function submitLead(data) {
         const response = await fetch(`${API_BASE_URL}/api/leads/submit`, {
             method: 'POST',
             headers: {
                 'Content-Type': 'application/json'
              },
             body: JSON.stringify(data)
          });

         return await response.json();
      }

     // === DETECTION ===
     function detectApiBaseUrl() {
          const hostname = window.location.hostname;

          // If running on SSLIP domain, use that domain's backend
         if (hostname.includes('.sslip.io')) {
              const ipMatch = hostname.match(/^(.+)\.sslip\.io$/);
             if (ipMatch) {
                  return `http://${ipMatch[1]}:8000`;
               }
          }

          // Default: use local API path
         return '/api';
      }

     // === HELPERS ===
     function isValidEmail(email) {
         return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
      }

     function escapeHtml(text) {
          const div = document.createElement('div');
          div.textContent = text;
          return div.innerHTML || text;
       }

     function setStatus(element, message, type) {
          if (!element) return;
         element.className = `form-status form-status-${type}`;
         element.style.display = 'block';
         element.innerHTML = `<p>${escapeHtml(message)}</p>`;

          // Auto-hide success after 8 seconds
         if (type === 'success') {
              setTimeout(() => { element.style.display = 'none'; }, 8000);
           }
       }

     function resetButton(btn) {
          btn.disabled = false;
         btn.textContent = 'Beratung anfragen';
      }

})();
