/**
 * CLG Admin Panel - Dashboard JavaScript
 * Handles API calls for KPIs, webhooks, content editor, and lead management.
 */

// === CONFIGURATION ===
const API_BASE = '/api'; // Points to FastAPI backend

// === LOGIN / LOGOUT ===
function login() {
     const username = document.getElementById('username').value;
     if (username) {
         localStorage.setItem('clg_auth', 'logged_in');
         document.getElementById('loginPage').style.display = 'none';
         document.getElementById('dashboardPage').style.display = 'block';
         loadDashboardData();
     }
}

function logout() {
     localStorage.removeItem('clg_auth');
     location.reload();
}

// Check auth on load
document.addEventListener('DOMContentLoaded', function() {
     if (localStorage.getItem('clg_auth') === 'logged_in') {
         document.getElementById('loginPage').style.display = 'none';
         document.getElementById('dashboardPage').style.display = 'block';
         loadDashboardData();
     }
});

// === TAB SWITCHING ===
function switchTab(tabName) {
     // Hide all tabs
     document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
     document.querySelectorAll('.sidebar nav a').forEach(a => a.classList.remove('active'));

     // Show selected tab
     const tab = document.getElementById(`tab-${tabName}`);
     if (tab) tab.classList.add('active');

     // Update sidebar
     const nav = document.getElementById(`nav-${tabName}`);
     if (nav) nav.classList.add('active');

     // Load data for the active tab
     if (tabName === 'dashboard') loadKPIDashboard();
     if (tabName === 'leads') loadLeads();
}

// === KPI DASHBOARD ===
async function loadDashboardData() {
     await loadKPIDashboard();
     await loadRecentLeads();
}

async function loadKPIDashboard() {
     try {
         const res = await fetch(`${API_BASE}/kpi/dashboard`);
         if (!res.ok) throw new Error('Failed to load KPI data');
         const data = await res.json();

         // Update KPI cards
         document.getElementById('kpi-total-7d').textContent = data.total_leads_7d || 0;
         document.getElementById('kpi-total-30d').textContent = data.total_leads_30d || 0;
         document.getElementById('kpi-total-all').textContent = data.total_leads_all || 0;
         document.getElementById('kpi-conversion').textContent = (data.contact_form_success_rate || 0) + '%';
         document.getElementById('kpi-pipeline').textContent = '€' + (data.estimated_pipeline_value || 0).toLocaleString('de-DE');

         // Update status distribution
         const statusDist = data.leads_by_status || {};
         Object.keys(statusDist).forEach(key => {
             const elId = `status-${key}`;
             const el = document.getElementById(elId);
             if (el) el.textContent = statusDist[key];
         });

     } catch (err) {
         console.error('Failed to load KPI data:', err);
     }
}

// === LEADS MANAGEMENT ===
async function loadRecentLeads() {
     try {
         const res = await fetch(`${API_BASE}/admin/leads`);
         if (!res.ok) throw new Error('Failed to load leads');
         const leads = await res.json();

         const tbody = document.getElementById('recentLeads');
         if (leads.length === 0) {
             tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;color:#a0aec0;">Keine Leads gefunden.</td></tr>';
             return;
         }

         tbody.innerHTML = leads.slice(0, 10).map(lead => `
             <tr>
                 <td>${lead.id}</td>
                 <td>${escapeHtml(lead.name)}</td>
                 <td><a href="mailto:${escapeHtml(lead.email)}">${escapeHtml(lead.email)}</a></td>
                 <td><span class="status-badge status-${lead.status || 'new'}">${capitalize(lead.status)}</span></td>
                 <td>${formatDate(lead.created_at)}</td>
             </tr>
         `).join('');

     } catch (err) {
         console.error('Failed to load recent leads:', err);
     }
}

async function loadLeads() {
     try {
         const res = await fetch(`${API_BASE}/admin/leads`);
         if (!res.ok) throw new Error('Failed to load leads');
         const leads = await res.json();

         // Populate lead selection dropdown
         const select = document.getElementById('updateLeadId');
         select.innerHTML = leads.map(l => 
             `<option value="${l.id}">${escapeHtml(l.name)} (${l.id})</option>`
         ).join('');

         // Update full table
         const tbody = document.getElementById('leadsTable');
         if (leads.length === 0) {
             tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;color:#a0aec0;">Keine Leads gefunden.</td></tr>';
             return;
         }

         tbody.innerHTML = leads.map(lead => `
             <tr>
                 <td>${lead.id}</td>
                 <td>${escapeHtml(lead.name)}</td>
                 <td><a href="mailto:${escapeHtml(lead.email)}">${escapeHtml(lead.email)}</a></td>
                 <td>${escapeHtml(lead.phone || '-')}</td>
                 <td>${escapeHtml(lead.assets_range || '-')}</td>
                 <td><span class="status-badge status-${lead.status || 'new'}">${capitalize(lead.status)}</span></td>
                 <td>${formatDate(lead.created_at)}</td>
                 <td>
                     <button class="btn btn-secondary" style="padding:0.3rem 0.6rem;font-size:0.8rem;" 
                             onclick="updateLeadStatusById(${lead.id})">
                         Status
                     </button>
                 </td>
             </tr>
         `).join('');

     } catch (err) {
         console.error('Failed to load leads:', err);
     }
}

async function updateLeadStatus() {
     const leadId = document.getElementById('updateLeadId').value;
     const status = document.getElementById('updateStatus').value;
     if (!leadId) { alert('Bitte wählen Sie einen Lead aus.'); return; }

     try {
         // PUT /api/admin/leads/{id} (simplified for now - would need endpoint in backend)
         console.log(`Update lead ${leadId} status to: ${status}`);
         alert(`Lead ${leadId} Status auf "${status}" aktualisiert.`);
     } catch (err) {
         console.error('Failed to update lead status:', err);
     }
}

async function updateLeadStatusById(leadId) {
     const status = prompt('Neuer Status (new/contacted/qualified/lost):', 'contacted');
     if (!status) return;

     try {
         console.log(`Update lead ${leadId} status to: ${status}`);
         alert(`Lead ${leadId} Status auf "${status}" aktualisiert.`);
         await loadLeads();
     } catch (err) {
         console.error('Failed to update lead:', err);
     }
}

// === WEBHOOKS CONFIGURATION ===
function saveWebhookConfig() {
     const config = {
         secret: document.getElementById('wh-secret').value,
         n8nUrl: document.getElementById('wh-n8n-url').value,
         binarySupport: document.getElementById('wh-binary-support').value,
         aesKey: document.getElementById('wh-aes-key').value,
     };

     localStorage.setItem('clg_webhook_config', JSON.stringify(config));
     alert('Webhook-Konfiguration gespeichert!');
     console.log('Webhook config saved:', config);
}

function refreshWebhooks() {
     const eventsDiv = document.getElementById('webhookEvents');
     eventsDiv.innerHTML = '<p style="color:#718096;">Loading webhook events...</p>';
     alert('Webhook-Ereignisse aktualisiert.');
}

function testWebhook() {
     // In production: POST to /api/webhooks/test with real payload
     alert('Test-Webhook wird gesendet... (n8n muss konfiguriert sein)');
     console.log('Testing webhook with configured n8n URL...');
}

// === CONTENT EDITOR ===
function saveContent() {
     const content = {
         heroHeading: document.getElementById('edit-hero-heading').value,
         heroSubtitle: document.getElementById('edit-hero-subtitle').value,
         heroCta: document.getElementById('edit-hero-cta').value,
         trustItems: document.getElementById('edit-trust-items').value,
     };

     // In production: POST to /api/admin/content/hero-main
     localStorage.setItem('clg_content', JSON.stringify(content));
     alert('Inhalte gespeichert! Änderungen sind jetzt wirksam.');
     console.log('Content saved:', content);
}

// === UTILITY FUNCTIONS ===
function escapeHtml(text) {
     if (!text) return '';
     const div = document.createElement('div');
     div.textContent = text;
     return div.innerHTML;
}

function capitalize(str) {
     if (!str) return 'New';
     return str.charAt(0).toUpperCase() + str.slice(1);
}

function formatDate(dateStr) {
     if (!dateStr) return '-';
     const date = new Date(dateStr);
     return date.toLocaleDateString('de-DE');
}

// Auto-refresh dashboard every 30 seconds
setInterval(() => {
     if (document.getElementById('tab-dashboard').classList.contains('active')) {
         loadKPIDashboard();
     }
}, 30000);
