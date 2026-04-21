LOGO_SVG = """<svg width="22" height="22" viewBox="0 0 20 20" fill="none">
  <rect x="1" y="1" width="8" height="8" rx="2" fill="currentColor"/>
  <rect x="11" y="1" width="8" height="8" rx="2" fill="currentColor" opacity=".6"/>
  <rect x="1" y="11" width="8" height="8" rx="2" fill="currentColor" opacity=".6"/>
  <rect x="11" y="11" width="8" height="8" rx="2" fill="currentColor" opacity=".3"/>
</svg>"""

LOGIN_HTML = """
<div style="min-height:100vh;width:100%;display:flex;align-items:center;justify-content:center;background:var(--bg);font-family:var(--font)">
  <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--r-lg);padding:36px;width:100%;max-width:380px;box-shadow:var(--shadow-md)">

    <div style="display:flex;align-items:center;gap:10px;margin-bottom:32px;color:var(--accent)">
      <svg width="26" height="26" viewBox="0 0 20 20" fill="none">
        <rect x="1" y="1" width="8" height="8" rx="2" fill="currentColor"/>
        <rect x="11" y="1" width="8" height="8" rx="2" fill="currentColor" opacity=".6"/>
        <rect x="1" y="11" width="8" height="8" rx="2" fill="currentColor" opacity=".6"/>
        <rect x="11" y="11" width="8" height="8" rx="2" fill="currentColor" opacity=".3"/>
      </svg>
      <span style="font-size:18px;font-weight:600;letter-spacing:-.3px">TaskFlow</span>
    </div>

    <h1 style="font-size:20px;font-weight:600;margin-bottom:5px;letter-spacing:-.4px;color:var(--text)">Willkommen zurück</h1>
    <p style="font-size:13px;color:var(--text2);margin-bottom:26px">Melde dich an, um fortzufahren</p>

    <div class="fg">
      <label class="fl">E-Mail</label>
      <input class="fi" type="email" id="login-email" placeholder="name@beispiel.de" autocomplete="email"
             onkeydown="if(event.key==='Enter')document.getElementById('login-password').focus()">
    </div>
    <div class="fg">
      <label class="fl">Passwort</label>
      <input class="fi" type="password" id="login-password" placeholder="••••••••" autocomplete="current-password"
             onkeydown="if(event.key==='Enter')doLogin()">
    </div>

    <div id="login-error" style="display:none;padding:10px 12px;background:var(--danger-lt);color:var(--danger);border-radius:var(--r-sm);font-size:13px;margin-bottom:16px;border:1px solid rgba(224,36,36,.15)"></div>

    <button class="btn btn-accent" id="login-btn" style="width:100%;justify-content:center;padding:10px 16px;font-size:14px"
            onclick="doLogin()">
      Einloggen
    </button>

    <p style="text-align:center;margin-top:22px;font-size:13px;color:var(--text2)">
      Noch kein Konto? <a href="/register" style="color:var(--accent);font-weight:500">Registrieren</a>
    </p>
  </div>
</div>
"""

LOGIN_JS = """
window.doLogin = async function() {
  const email = document.getElementById('login-email').value.trim();
  const password = document.getElementById('login-password').value;
  const btn = document.getElementById('login-btn');

  window.showLoginError('');
  document.getElementById('login-error').style.display = 'none';

  if (!email || !password) {
    window.showLoginError('Bitte E-Mail und Passwort eingeben.');
    return;
  }

  btn.disabled = true;
  btn.textContent = 'Einloggen…';

  try {
    const resp = await fetch('/api/auth/login', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({email, password})
    });
    const data = await resp.json();
    if (data.success) {
      window.location.href = '/todos';
    } else {
      window.showLoginError(data.error || 'Fehler beim Einloggen');
    }
  } catch(e) {
    window.showLoginError('Verbindungsfehler. Bitte erneut versuchen.');
  }

  btn.disabled = false;
  btn.textContent = 'Einloggen';
};

window.showLoginError = function(msg) {
  const el = document.getElementById('login-error');
  el.textContent = msg;
  el.style.display = msg ? 'block' : 'none';
};
"""

REGISTER_HTML = """
<div style="min-height:100vh;width:100%;display:flex;align-items:center;justify-content:center;background:var(--bg);font-family:var(--font);padding:24px 0">
  <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--r-lg);padding:36px;width:100%;max-width:420px;box-shadow:var(--shadow-md)">

    <div style="display:flex;align-items:center;gap:10px;margin-bottom:32px;color:var(--accent)">
      <svg width="26" height="26" viewBox="0 0 20 20" fill="none">
        <rect x="1" y="1" width="8" height="8" rx="2" fill="currentColor"/>
        <rect x="11" y="1" width="8" height="8" rx="2" fill="currentColor" opacity=".6"/>
        <rect x="1" y="11" width="8" height="8" rx="2" fill="currentColor" opacity=".6"/>
        <rect x="11" y="11" width="8" height="8" rx="2" fill="currentColor" opacity=".3"/>
      </svg>
      <span style="font-size:18px;font-weight:600;letter-spacing:-.3px">TaskFlow</span>
    </div>

    <h1 style="font-size:20px;font-weight:600;margin-bottom:5px;letter-spacing:-.4px;color:var(--text)">Konto erstellen</h1>
    <p style="font-size:13px;color:var(--text2);margin-bottom:26px">Kostenlos registrieren und loslegen</p>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:13px">
      <div class="fg">
        <label class="fl">Vorname</label>
        <input class="fi" type="text" id="reg-firstname" placeholder="Max" autocomplete="given-name">
      </div>
      <div class="fg">
        <label class="fl">Nachname</label>
        <input class="fi" type="text" id="reg-lastname" placeholder="Muster" autocomplete="family-name">
      </div>
    </div>
    <div class="fg">
      <label class="fl">E-Mail</label>
      <input class="fi" type="email" id="reg-email" placeholder="name@beispiel.de" autocomplete="email">
    </div>
    <div class="fg">
      <label class="fl">Passwort</label>
      <input class="fi" type="password" id="reg-password" placeholder="Mindestens 8 Zeichen" autocomplete="new-password">
    </div>
    <div class="fg">
      <label class="fl">Passwort wiederholen</label>
      <input class="fi" type="password" id="reg-password2" placeholder="Passwort bestätigen" autocomplete="new-password"
             onkeydown="if(event.key==='Enter')doRegister()">
    </div>

    <div id="reg-error" style="display:none;padding:10px 12px;background:var(--danger-lt);color:var(--danger);border-radius:var(--r-sm);font-size:13px;margin-bottom:16px;border:1px solid rgba(224,36,36,.15)"></div>

    <button class="btn btn-accent" id="reg-btn" style="width:100%;justify-content:center;padding:10px 16px;font-size:14px"
            onclick="doRegister()">
      Registrieren
    </button>

    <p style="text-align:center;margin-top:22px;font-size:13px;color:var(--text2)">
      Bereits ein Konto? <a href="/login" style="color:var(--accent);font-weight:500">Einloggen</a>
    </p>
  </div>
</div>
"""

REGISTER_JS = """
window.doRegister = async function() {
  const firstname = document.getElementById('reg-firstname').value.trim();
  const lastname  = document.getElementById('reg-lastname').value.trim();
  const email     = document.getElementById('reg-email').value.trim();
  const password  = document.getElementById('reg-password').value;
  const password2 = document.getElementById('reg-password2').value;
  const btn = document.getElementById('reg-btn');

  window.showRegError('');

  if (!firstname || !lastname || !email || !password) {
    window.showRegError('Bitte alle Felder ausfüllen.');
    return;
  }
  if (password.length < 8) {
    window.showRegError('Das Passwort muss mindestens 8 Zeichen lang sein.');
    return;
  }
  if (password !== password2) {
    window.showRegError('Die Passwörter stimmen nicht überein.');
    return;
  }

  btn.disabled = true;
  btn.textContent = 'Registrieren…';

  try {
    const resp = await fetch('/api/auth/register', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({firstname, lastname, email, password})
    });
    const data = await resp.json();
    if (data.success) {
      window.location.href = '/todos';
    } else {
      window.showRegError(data.error || 'Fehler bei der Registrierung');
    }
  } catch(e) {
    window.showRegError('Verbindungsfehler. Bitte erneut versuchen.');
  }

  btn.disabled = false;
  btn.textContent = 'Registrieren';
};

window.showRegError = function(msg) {
  const el = document.getElementById('reg-error');
  el.textContent = msg;
  el.style.display = msg ? 'block' : 'none';
};
"""

TODO_APP_HTML = """
<div id="taskflow-app">

  <aside id="sidebar">
    <div class="sb-logo">
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <rect x="1" y="1" width="8" height="8" rx="2" fill="currentColor"/>
        <rect x="11" y="1" width="8" height="8" rx="2" fill="currentColor" opacity=".6"/>
        <rect x="1" y="11" width="8" height="8" rx="2" fill="currentColor" opacity=".6"/>
        <rect x="11" y="11" width="8" height="8" rx="2" fill="currentColor" opacity=".3"/>
      </svg>
      TaskFlow
    </div>

    <div class="sb-sec">Ansichten</div>
    <div class="sb-item" id="sb-board" onclick="setView('board')">
      <svg width="15" height="15" viewBox="0 0 15 15" fill="none"><rect x="1" y="1" width="5" height="13" rx="1.5" stroke="currentColor" stroke-width="1.4"/><rect x="9" y="1" width="5" height="9" rx="1.5" stroke="currentColor" stroke-width="1.4"/></svg>
      Board
    </div>
    <div class="sb-item" id="sb-list" onclick="setView('list')">
      <svg width="15" height="15" viewBox="0 0 15 15" fill="none"><line x1="3" y1="4.5" x2="12" y2="4.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><line x1="3" y1="7.5" x2="12" y2="7.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><line x1="3" y1="10.5" x2="9" y2="10.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>
      Liste
    </div>
    <div class="sb-item" id="sb-gantt" onclick="setView('gantt')">
      <svg width="15" height="15" viewBox="0 0 15 15" fill="none"><rect x="1" y="3" width="9" height="3.5" rx="1.5" fill="currentColor" opacity=".7"/><rect x="4" y="8.5" width="10" height="3.5" rx="1.5" fill="currentColor" opacity=".7"/></svg>
      Zeitplan
    </div>
    <div class="sb-item" id="sb-calendar" onclick="setView('calendar')">
      <svg width="15" height="15" viewBox="0 0 15 15" fill="none"><rect x="1" y="2.5" width="13" height="11" rx="1.5" stroke="currentColor" stroke-width="1.4"/><line x1="1" y1="6.5" x2="14" y2="6.5" stroke="currentColor" stroke-width="1.4"/><line x1="4.5" y1="1" x2="4.5" y2="4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><line x1="10.5" y1="1" x2="10.5" y2="4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>
      Kalender
    </div>
    <div class="sb-item" id="sb-dashboard" onclick="setView('dashboard')">
      <svg width="15" height="15" viewBox="0 0 15 15" fill="none"><rect x="1" y="8" width="3.5" height="6" rx="1" fill="currentColor" opacity=".7"/><rect x="5.75" y="5" width="3.5" height="9" rx="1" fill="currentColor" opacity=".7"/><rect x="10.5" y="1" width="3.5" height="13" rx="1" fill="currentColor" opacity=".7"/></svg>
      Dashboard
    </div>

    <div class="sb-sec">Listen</div>
    <div id="sb-lists"></div>

    <div class="sb-fill"></div>
    <div class="sb-bottom">
      <div class="sb-item" onclick="toggleAI()">
        <svg width="15" height="15" viewBox="0 0 15 15" fill="none"><circle cx="7.5" cy="7.5" r="6" stroke="currentColor" stroke-width="1.4"/><path d="M5.5 6.5C5.5 5.4 6.4 4.5 7.5 4.5s2 .9 2 2c0 .9-.5 1.6-1.3 1.9L8 10H7L6.7 8.4C6 8.1 5.5 7.4 5.5 6.5Z" fill="currentColor"/><circle cx="7.5" cy="11.5" r=".9" fill="currentColor"/></svg>
        KI-Assistent
      </div>
      <div class="sb-item" onclick="toggleDark()">
        <svg id="dark-ico" width="15" height="15" viewBox="0 0 15 15" fill="none"><path d="M7.5 1a6.5 6.5 0 1 0 6.5 6.5A6.5 6.5 0 0 0 7.5 1Zm0 11.5A5 5 0 1 1 12.5 7.5 5 5 0 0 1 7.5 12.5Z" fill="currentColor" opacity=".4"/><path d="M7.5 3v9a4.5 4.5 0 0 0 0-9Z" fill="currentColor"/></svg>
        <span id="dark-lbl">Dark Mode</span>
      </div>
      <div class="sb-item" style="color:var(--danger)" onclick="doLogout()">
        <svg width="15" height="15" viewBox="0 0 15 15" fill="none"><path d="M6 2H3a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><path d="M10 10l3-2.5L10 5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/><line x1="13" y1="7.5" x2="6" y2="7.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>
        Abmelden
      </div>
    </div>
  </aside>

  <div id="sb-overlay" onclick="closeSidebar()"></div>

  <div id="main">
    <div id="topbar">
      <div class="tb1">
        <button class="btn btn-icon" id="menu-btn" onclick="toggleSidebar()" style="display:none">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><line x1="2" y1="5" x2="14" y2="5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><line x1="2" y1="8" x2="14" y2="8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><line x1="2" y1="11" x2="14" y2="11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
        </button>
        <span class="proj-title" id="topbar-title">TaskFlow</span>
        <div class="sp"></div>
        <input class="sbox" id="srch" placeholder="Suchen…" oninput="S.query=this.value;render()">
        <select class="sel" style="width:auto" onchange="S.filterPriority=this.value;render()">
          <option value="all">Alle</option>
          <option value="critical">Kritisch</option>
          <option value="high">Hoch</option>
          <option value="medium">Mittel</option>
          <option value="low">Niedrig</option>
        </select>
        <button class="btn" onclick="toggleAI()" title="KI-Assistent">
          <svg width="14" height="14" viewBox="0 0 15 15" fill="none"><circle cx="7.5" cy="7.5" r="6" stroke="currentColor" stroke-width="1.4"/><path d="M5.5 6.5C5.5 5.4 6.4 4.5 7.5 4.5s2 .9 2 2c0 .9-.5 1.6-1.3 1.9L8 10H7L6.7 8.4C6 8.1 5.5 7.4 5.5 6.5Z" fill="currentColor"/><circle cx="7.5" cy="11.5" r=".9" fill="currentColor"/></svg>
          <span>KI</span>
        </button>
        <button class="btn btn-accent" onclick="openModal(null)">
          <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><line x1="6.5" y1="1" x2="6.5" y2="12" stroke="white" stroke-width="1.6" stroke-linecap="round"/><line x1="1" y1="6.5" x2="12" y2="6.5" stroke="white" stroke-width="1.6" stroke-linecap="round"/></svg>
          <span>Aufgabe</span>
        </button>
      </div>
      <div class="tb2" id="vtabs">
        <div class="vtab active" data-v="board" onclick="setView('board')">Board</div>
        <div class="vtab" data-v="list" onclick="setView('list')">Liste</div>
        <div class="vtab" data-v="gantt" onclick="setView('gantt')">Zeitplan</div>
        <div class="vtab" data-v="calendar" onclick="setView('calendar')">Kalender</div>
        <div class="vtab" data-v="dashboard" onclick="setView('dashboard')">Dashboard</div>
      </div>
    </div>
    <div id="content"></div>
  </div>

  <div id="modal-ov" style="display:none" onclick="if(event.target===this)closeModal()">
    <div id="tmodal"></div>
  </div>

  <div id="aip">
    <div class="ai-hdr">
      <div style="display:flex;align-items:center;gap:8px">
        <svg width="16" height="16" viewBox="0 0 15 15" fill="none" style="color:var(--accent)"><circle cx="7.5" cy="7.5" r="6" stroke="currentColor" stroke-width="1.4"/><path d="M5.5 6.5C5.5 5.4 6.4 4.5 7.5 4.5s2 .9 2 2c0 .9-.5 1.6-1.3 1.9L8 10H7L6.7 8.4C6 8.1 5.5 7.4 5.5 6.5Z" fill="currentColor"/><circle cx="7.5" cy="11.5" r=".9" fill="currentColor"/></svg>
        KI-Assistent
      </div>
      <button class="btn btn-sm" onclick="toggleAI()">✕</button>
    </div>
    <div class="ai-key-row">
      <div style="font-size:11.5px;color:var(--text2);margin-bottom:5px;font-weight:500">Anthropic API Key</div>
      <input class="ai-key-inp" type="password" id="ai-key-in" placeholder="sk-ant-…" oninput="saveApiKey(this.value)">
    </div>
    <div class="ai-quick">
      <button class="ai-qb" onclick="aiAsk('Analysiere die Aufgaben und schlage Priorisierungen vor.')">Priorisieren</button>
      <button class="ai-qb" onclick="aiAsk('Welche Aufgaben sind überfällig oder gefährdet?')">Risiken</button>
      <button class="ai-qb" onclick="aiAsk('Erstelle eine kurze Projektzusammenfassung.')">Status</button>
      <button class="ai-qb" onclick="aiAsk('Gib mir Produktivitätstipps.')">Tipps</button>
    </div>
    <div class="ai-msgs" id="ai-msgs"></div>
    <div class="ai-in-row">
      <input class="ai-in" id="ai-in" placeholder="Frage stellen…" onkeydown="if(event.key==='Enter')aiSend()">
      <button class="btn btn-accent" onclick="aiSend()">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M1 7L13 1L7 13L6 8L1 7Z" stroke="white" stroke-width="1.4" stroke-linejoin="round"/></svg>
      </button>
    </div>
  </div>

  <nav id="mobile-nav">
    <div class="mnav">
      <div class="mnav-item" id="mn-board" onclick="setView('board')">
        <svg width="18" height="18" viewBox="0 0 15 15" fill="none"><rect x="1" y="1" width="5" height="13" rx="1.5" stroke="currentColor" stroke-width="1.4"/><rect x="9" y="1" width="5" height="9" rx="1.5" stroke="currentColor" stroke-width="1.4"/></svg>
        <span>Board</span>
      </div>
      <div class="mnav-item" id="mn-list" onclick="setView('list')">
        <svg width="18" height="18" viewBox="0 0 15 15" fill="none"><line x1="3" y1="4.5" x2="12" y2="4.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><line x1="3" y1="7.5" x2="12" y2="7.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><line x1="3" y1="10.5" x2="9" y2="10.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>
        <span>Liste</span>
      </div>
      <div class="mnav-item" id="mn-gantt" onclick="setView('gantt')">
        <svg width="18" height="18" viewBox="0 0 15 15" fill="none"><rect x="1" y="3" width="9" height="3.5" rx="1.5" fill="currentColor" opacity=".7"/><rect x="4" y="8.5" width="10" height="3.5" rx="1.5" fill="currentColor" opacity=".7"/></svg>
        <span>Zeitplan</span>
      </div>
      <div class="mnav-item" id="mn-calendar" onclick="setView('calendar')">
        <svg width="18" height="18" viewBox="0 0 15 15" fill="none"><rect x="1" y="2.5" width="13" height="11" rx="1.5" stroke="currentColor" stroke-width="1.4"/><line x1="1" y1="6.5" x2="14" y2="6.5" stroke="currentColor" stroke-width="1.4"/><line x1="4.5" y1="1" x2="4.5" y2="4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><line x1="10.5" y1="1" x2="10.5" y2="4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>
        <span>Kalender</span>
      </div>
      <div class="mnav-item" id="mn-dashboard" onclick="setView('dashboard')">
        <svg width="18" height="18" viewBox="0 0 15 15" fill="none"><rect x="1" y="8" width="3.5" height="6" rx="1" fill="currentColor" opacity=".7"/><rect x="5.75" y="5" width="3.5" height="9" rx="1" fill="currentColor" opacity=".7"/><rect x="10.5" y="1" width="3.5" height="13" rx="1" fill="currentColor" opacity=".7"/></svg>
        <span>Stats</span>
      </div>
    </div>
  </nav>

</div>
"""

TODO_APP_JS = """
const TODAY = new Date();
const TODAY_STR = TODAY.toISOString().split('T')[0];
const AV_CLR = {MH:'#4361EE',JF:'#7C3AED',AB:'#D85A30',LK:'#0E9F6E',TS:'#C27803'};
const BCKT_CLR = {Backlog:'#8B949E','To-Do':'#4361EE','In Progress':'#C27803',Done:'#0E9F6E'};
const BCKT_DOT = {Backlog:'#9DA8C0','To-Do':'#4361EE','In Progress':'#F59E0B',Done:'#10B981'};
const PRIO_LBL = {low:'Niedrig',medium:'Mittel',high:'Hoch',critical:'Kritisch'};
const LIST_COLORS = ['#4361EE','#7C3AED','#0E9F6E','#C27803','#D85A30','#E91E63','#0284C7','#7C2D12'];

const S = {
  view: 'board',
  query: '',
  filterPriority: 'all',
  filterListId: null,
  showAI: false,
  aiMsgs: [{role:'ai',text:'Hallo! Ich bin dein KI-Assistent. Ich kenne alle deine Aufgaben und kann helfen bei Priorisierung, Risikoanalyse und Projektplanung.'}],
  calDate: new Date(),
  sortCol: 'dueDate',
  sortDir: 1,
  dragId: null,
  tasks: [],
  lists: [],
};

function loadData() {
  S.tasks = window.__TODOS__ ? JSON.parse(JSON.stringify(window.__TODOS__)) : [];
  S.lists = window.__LISTS__ ? JSON.parse(JSON.stringify(window.__LISTS__)) : [];
  if (S.lists.length > 0) S.filterListId = S.lists[0].id;
  const dk = localStorage.getItem('tf_dark');
  if (dk === '1') document.documentElement.setAttribute('data-dark','');
  const ak = localStorage.getItem('tf_apikey');
  if (ak) { setTimeout(()=>{ const el=document.getElementById('ai-key-in'); if(el) el.value=ak; },100); }
}

function saveApiKey(v) { try { localStorage.setItem('tf_apikey', v); } catch(e){} }

function isOv(t) { return t.dueDate && t.dueDate < TODAY_STR && t.bucket !== 'Done'; }
function fmtD(s) { if(!s) return ''; const d=new Date(s+'T00:00:00'); return d.toLocaleDateString('de-DE',{day:'2-digit',month:'2-digit',year:'numeric'}); }
function fmtS(s) { if(!s) return ''; const d=new Date(s+'T00:00:00'); return d.toLocaleDateString('de-DE',{day:'2-digit',month:'2-digit'}); }
function esc(s) { return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function listColor(id) { return LIST_COLORS[Math.abs(id) % LIST_COLORS.length]; }

function filtered() {
  return S.tasks.filter(t => {
    if (S.filterListId !== null && t.listId !== S.filterListId) return false;
    if (S.filterPriority !== 'all' && t.priority !== S.filterPriority) return false;
    if (S.query) {
      const q = S.query.toLowerCase();
      if (!t.title.toLowerCase().includes(q) && !(t.labels||[]).join(' ').toLowerCase().includes(q)) return false;
    }
    return true;
  });
}

function avHtml(assignees) {
  return (assignees||[]).map(a => `<div class="av" style="background:${AV_CLR[a]||'#888'};color:#fff" title="${a}">${a}</div>`).join('');
}

function taskCard(t) {
  const ov = isOv(t);
  return `<div class="tc" draggable="true" id="tc${t.id}"
    ondragstart="dragStart(${t.id})" ondragend="dragEnd()"
    onclick="openModal(${t.id})">
    <div class="t-ttl">${esc(t.title)}</div>
    <div class="t-meta">
      <span class="pb p-${t.priority}">${PRIO_LBL[t.priority]}</span>
      ${(t.labels||[]).slice(0,2).map(l=>`<span class="lbl-badge">${esc(l)}</span>`).join('')}
      ${t.dueDate?`<span class="t-due${ov?' ov':''}">${fmtS(t.dueDate)}</span>`:''}
      ${(t.assignees||[]).length?`<div class="avs">${avHtml(t.assignees)}</div>`:''}
    </div>
    ${t.progress>0?`<div class="pgw"><div class="pgb" style="width:${t.progress}%"></div></div>`:''}
  </div>`;
}

function renderBoard() {
  const buckets = ['Backlog','To-Do','In Progress','Done'];
  const tasks = filtered();
  const cols = buckets.map(b => {
    const bt = tasks.filter(t => t.bucket === b);
    return `<div class="board-col">
      <div class="col-hdr">
        <span class="sb-dot" style="background:${BCKT_DOT[b]}"></span>
        ${b}
        <span class="col-cnt">${bt.length}</span>
      </div>
      <div class="col-tasks" id="col-${b.replace(/ /g,'-')}"
        ondragover="event.preventDefault();this.classList.add('dov')"
        ondragleave="this.classList.remove('dov')"
        ondrop="drop('${b}',this)">
        ${bt.map(taskCard).join('')}
      </div>
      <button class="col-add" onclick="openModal(null,'${b}')">+ Aufgabe hinzufügen</button>
    </div>`;
  }).join('');
  document.getElementById('content').innerHTML = `<div class="board fade-in">${cols}</div>`;
}

function renderList() {
  const tasks = filtered().sort((a,b) => {
    let va=a[S.sortCol]||'', vb=b[S.sortCol]||'';
    return va<vb?-S.sortDir:va>vb?S.sortDir:0;
  });
  function th(col,lbl) { return `<th onclick="S.sortCol='${col}';S.sortDir*=-1;renderList()">${lbl}${S.sortCol===col?(S.sortDir>0?' ↑':' ↓'):''}</th>`; }
  document.getElementById('content').innerHTML = `<div class="list-wrap fade-in">
    <table class="ltbl">
      <thead><tr>${th('title','Aufgabe')}${th('startDate','Start')}${th('dueDate','Fälligkeit')}${th('bucket','Status')}${th('progress','Fortschritt')}${th('priority','Priorität')}</tr></thead>
      <tbody>${tasks.map(t => {
        const ov=isOv(t);
        return `<tr onclick="openModal(${t.id})">
          <td style="font-weight:500;max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${esc(t.title)}</td>
          <td style="white-space:nowrap">${fmtD(t.startDate)}</td>
          <td class="${ov?'ov':''}" style="white-space:nowrap">${fmtD(t.dueDate)}</td>
          <td><span style="display:inline-flex;align-items:center;gap:5px"><span class="sb-dot" style="background:${BCKT_DOT[t.bucket]}"></span>${esc(t.bucket)}</span></td>
          <td style="min-width:120px">
            <div style="display:flex;align-items:center;gap:7px">
              <div class="pgw" style="flex:1;height:5px"><div class="pgb" style="width:${t.progress}%"></div></div>
              <span style="font-size:11px;color:var(--text2);min-width:28px">${t.progress}%</span>
            </div>
          </td>
          <td><span class="pb p-${t.priority}">${PRIO_LBL[t.priority]}</span></td>
        </tr>`;
      }).join('')}</tbody>
    </table>
  </div>`;
}

function renderGantt() {
  const DAY_W = 14;
  const rStart = new Date(TODAY.getFullYear(), TODAY.getMonth() - 1, 1);
  const rEnd   = new Date(TODAY.getFullYear(), TODAY.getMonth() + 4, 1);
  const days   = Math.round((rEnd - rStart) / 864e5);
  const tlW    = days * DAY_W;
  const todayOff = Math.max(0, Math.round((TODAY - rStart) / 864e5)) * DAY_W;
  const tasks = filtered();

  let hdrs = '';
  let d = new Date(rStart);
  while (d < rEnd) {
    const off = Math.round((d - rStart) / 864e5) * DAY_W;
    if (d.getDate() === 1) {
      const mN = d.toLocaleDateString('de-DE',{month:'long',year:'numeric'});
      hdrs += `<div class="gdl gdl-month" style="left:${off}px;width:130px">${mN}</div>`;
    }
    if (d.getDay() === 1) {
      hdrs += `<div class="gdl" style="left:${off}px;width:${DAY_W*7}px;top:17px;height:19px">${fmtS(d.toISOString().split('T')[0])}</div>`;
    }
    d.setDate(d.getDate()+1);
  }

  const rows = tasks.map(t => {
    let bar = '';
    if (t.startDate && t.dueDate) {
      const s = new Date(t.startDate+'T00:00:00');
      const e = new Date(t.dueDate+'T00:00:00');
      const left = Math.round((s - rStart) / 864e5) * DAY_W;
      const w    = Math.max(Math.round((e - s) / 864e5) * DAY_W, DAY_W * 2);
      const bc   = BCKT_CLR[t.bucket] || '#888';
      bar = `<div class="gbar" style="left:${left}px;width:${w}px;background:${bc}" onclick="openModal(${t.id})" title="${esc(t.title)}">${esc(t.title)}</div>`;
    }
    return `<div class="grow">
      <div class="gname">
        <span class="pb p-${t.priority}" style="font-size:10px;padding:1px 5px">${t.priority[0].toUpperCase()}</span>
        <span class="gname-txt">${esc(t.title)}</span>
      </div>
      <div class="gtl" style="width:${tlW}px">
        ${bar}
        <div class="gtoday-ln" style="left:${todayOff}px"></div>
      </div>
    </div>`;
  }).join('');

  document.getElementById('content').innerHTML = `<div class="gwrap fade-in">
    <div class="ginner" style="min-width:${220+tlW}px">
      <div class="ghdr">
        <div class="gncol">Aufgabe</div>
        <div class="gtl-h" style="width:${tlW}px;min-width:${tlW}px;position:relative;overflow:hidden">
          ${hdrs}
          <div class="gtoday-ln" style="left:${todayOff}px"></div>
        </div>
      </div>
      ${rows}
    </div>
  </div>`;
}

function renderCalendar() {
  const y = S.calDate.getFullYear(), m = S.calDate.getMonth();
  const first = new Date(y,m,1), last = new Date(y,m+1,0);
  const startWd = (first.getDay()+6)%7;
  const tasks = filtered();
  const byDate = {};
  tasks.forEach(t => { if(t.dueDate) byDate[t.dueDate] = (byDate[t.dueDate]||[]).concat(t); });
  const days = ['Mo','Di','Mi','Do','Fr','Sa','So'];
  let cells = '';
  const total = startWd + last.getDate();
  const rows = Math.ceil(total/7);
  for (let i=0; i<rows*7; i++) {
    const dayN = i - startWd + 1;
    const isThis = dayN>=1 && dayN<=last.getDate();
    const dateObj = new Date(y, m, dayN);
    const ds = dateObj.toISOString().split('T')[0];
    const isT = ds === TODAY_STR;
    const dt = byDate[ds] || [];
    cells += `<div class="cal-day${!isThis?' other':''}${isT?' today':''}">
      <div class="cal-dn">${isThis?dayN:''}</div>
      ${dt.slice(0,3).map(t=>`<div class="cal-t" style="background:${BCKT_CLR[t.bucket]}22;color:${BCKT_CLR[t.bucket]}" onclick="event.stopPropagation();openModal(${t.id})">${esc(t.title)}</div>`).join('')}
      ${dt.length>3?`<div style="font-size:10px;color:var(--text3)">+${dt.length-3}</div>`:''}
    </div>`;
  }
  const mName = S.calDate.toLocaleDateString('de-DE',{month:'long',year:'numeric'});
  document.getElementById('content').innerHTML = `<div class="cal-wrap fade-in">
    <div class="cal-nav">
      <button class="btn btn-sm" onclick="S.calDate=new Date(S.calDate.getFullYear(),S.calDate.getMonth()-1,1);renderCalendar()">‹</button>
      <span class="cal-title">${mName}</span>
      <button class="btn btn-sm" onclick="S.calDate=new Date(S.calDate.getFullYear(),S.calDate.getMonth()+1,1);renderCalendar()">›</button>
      <button class="btn btn-sm" onclick="S.calDate=new Date();renderCalendar()">Heute</button>
    </div>
    <div class="cal-g">
      ${days.map(d=>`<div class="cal-dh">${d}</div>`).join('')}
      ${cells}
    </div>
  </div>`;
}

function renderDashboard() {
  const tasks = S.tasks.filter(t => S.filterListId === null || t.listId === S.filterListId);
  const done = tasks.filter(t=>t.bucket==='Done').length;
  const inp  = tasks.filter(t=>t.bucket==='In Progress').length;
  const ov   = tasks.filter(isOv).length;
  const avgP = tasks.length ? Math.round(tasks.reduce((a,t)=>a+t.progress,0)/tasks.length) : 0;
  const buckets = ['Backlog','To-Do','In Progress','Done'];
  const prioColors = {critical:'#E02424',high:'#C27803',medium:'#4361EE',low:'#10B981'};
  const byP = ['critical','high','medium','low'].map(p=>({p,c:tasks.filter(t=>t.priority===p).length}));
  document.getElementById('content').innerHTML = `<div class="dash-wrap fade-in">
    <div class="stats-g">
      <div class="stat-c"><div class="stat-l">Alle Aufgaben</div><div class="stat-v">${tasks.length}</div></div>
      <div class="stat-c"><div class="stat-l">Abgeschlossen</div><div class="stat-v" style="color:var(--success)">${done}</div></div>
      <div class="stat-c"><div class="stat-l">In Bearbeitung</div><div class="stat-v" style="color:var(--warning)">${inp}</div></div>
      <div class="stat-c"><div class="stat-l">Überfällig</div><div class="stat-v" style="color:var(--danger)">${ov}</div></div>
    </div>
    <div class="charts-g">
      <div class="chart-c">
        <div class="chart-t">Fortschritt nach Status</div>
        ${buckets.map(b=>{const bt=tasks.filter(t=>t.bucket===b);const p=bt.length?Math.round(bt.reduce((a,t)=>a+t.progress,0)/bt.length):0;return`<div class="prow"><span class="prow-name">${b}</span><div class="prow-bw"><div class="prow-b" style="width:${p}%;background:${BCKT_CLR[b]}"></div></div><span class="prow-v">${p}%</span></div>`;}).join('')}
      </div>
      <div class="chart-c">
        <div class="chart-t">Verteilung nach Priorität</div>
        ${byP.map(({p,c})=>{const pct=tasks.length?Math.round(c/tasks.length*100):0;return`<div class="prow"><span class="prow-name">${PRIO_LBL[p]}</span><div class="prow-bw"><div class="prow-b" style="width:${pct}%;background:${prioColors[p]}"></div></div><span class="prow-v">${c}</span></div>`;}).join('')}
      </div>
      <div class="chart-c">
        <div class="chart-t">Gesamtfortschritt</div>
        <div style="display:flex;align-items:center;gap:20px;margin-top:8px">
          <svg width="90" height="90" viewBox="0 0 90 90">
            <circle cx="45" cy="45" r="36" fill="none" stroke="var(--surface2)" stroke-width="10"/>
            <circle cx="45" cy="45" r="36" fill="none" stroke="var(--success)" stroke-width="10"
              stroke-linecap="round"
              stroke-dasharray="${2*Math.PI*36}" stroke-dashoffset="${2*Math.PI*36*(1-avgP/100)}"
              transform="rotate(-90 45 45)"/>
            <text x="45" y="50" text-anchor="middle" font-size="18" font-weight="600" fill="var(--text)" font-family="DM Sans,sans-serif">${avgP}%</text>
          </svg>
          <div>
            <div style="font-size:13px;color:var(--text2);margin-bottom:6px">Ø aller Aufgaben</div>
            <div style="font-size:14px;font-weight:500">${done} / ${tasks.length} fertig</div>
            <div style="font-size:12px;color:var(--text3);margin-top:4px">${ov} überfällig</div>
          </div>
        </div>
      </div>
      <div class="chart-c">
        <div class="chart-t">Überfällige Aufgaben</div>
        ${tasks.filter(isOv).length===0
          ?'<div style="font-size:13px;color:var(--text3);padding:12px 0">Keine überfälligen Aufgaben!</div>'
          :tasks.filter(isOv).slice(0,5).map(t=>`<div style="display:flex;align-items:center;gap:9px;padding:7px 0;border-bottom:1px solid var(--border);cursor:pointer" onclick="openModal(${t.id})">
            <span class="pb p-${t.priority}" style="font-size:10.5px">${PRIO_LBL[t.priority]}</span>
            <span style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:13px">${esc(t.title)}</span>
            <span style="color:var(--danger);font-size:11.5px;font-weight:600">${fmtS(t.dueDate)}</span>
          </div>`).join('')
        }
      </div>
    </div>
  </div>`;
}

function render() {
  const map = {board:renderBoard,list:renderList,gantt:renderGantt,calendar:renderCalendar,dashboard:renderDashboard};
  (map[S.view]||renderBoard)();
  document.querySelectorAll('.vtab').forEach(t => t.classList.toggle('active', t.dataset.v===S.view));
  document.querySelectorAll('.mnav-item').forEach(t => t.classList.toggle('active', t.id==='mn-'+S.view));
  ['board','list','gantt','calendar','dashboard'].forEach(v => {
    const el = document.getElementById('sb-'+v);
    if (el) el.classList.toggle('active', v===S.view);
  });
}

function setView(v) { S.view=v; render(); closeSidebar(); }

function renderLists() {
  const el = document.getElementById('sb-lists');
  if (!el) return;
  const titleEl = document.getElementById('topbar-title');
  const activeList = S.lists.find(l => l.id === S.filterListId);
  if (titleEl && activeList) titleEl.textContent = activeList.name;

  el.innerHTML = S.lists.map(l => `
    <div class="sb-item${S.filterListId===l.id?' active':''}" onclick="selectList(${l.id})" style="${S.filterListId===l.id?'color:var(--accent)':''}">
      <span class="sb-dot" style="background:${listColor(l.id)}"></span>
      <span style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${esc(l.name)}</span>
    </div>
  `).join('') + `
    <div class="sb-item" style="color:var(--accent)" onclick="promptNewList()">
      <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><line x1="6.5" y1="1" x2="6.5" y2="12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><line x1="1" y1="6.5" x2="12" y2="6.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
      Neue Liste
    </div>
  `;
}

function selectList(id) {
  S.filterListId = id;
  renderLists();
  render();
  closeSidebar();
}

async function promptNewList() {
  const name = prompt('Name der neuen Liste:');
  if (!name || !name.trim()) return;
  try {
    const resp = await fetch('/api/lists', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({name: name.trim()})
    });
    const list = await resp.json();
    S.lists.push(list);
    selectList(list.id);
  } catch(e) { alert('Fehler beim Erstellen der Liste'); }
}

function dragStart(id) {
  S.dragId = id;
  setTimeout(()=>{ const el=document.getElementById('tc'+id); if(el) el.classList.add('dragging'); },0);
}
function dragEnd() {
  if (S.dragId) { const el=document.getElementById('tc'+S.dragId); if(el) el.classList.remove('dragging'); }
  document.querySelectorAll('.col-tasks').forEach(c=>c.classList.remove('dov'));
  S.dragId = null;
}
async function drop(bucket, el) {
  el.classList.remove('dov');
  if (!S.dragId) return;
  const t = S.tasks.find(x => x.id === S.dragId);
  if (t && t.bucket !== bucket) {
    t.bucket = bucket;
    try {
      await fetch(`/api/todos/${t.id}`, {
        method: 'PUT',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(t)
      });
    } catch(e) { console.error('Fehler beim Aktualisieren:', e); }
  }
  S.dragId = null;
  render();
}

function openModal(id, bucket) {
  let t = id ? S.tasks.find(x=>x.id===id) : null;
  const isNew = !t;
  if (!t) t = {id:null,title:'',desc:'',bucket:bucket||'To-Do',priority:'medium',progress:0,startDate:TODAY_STR,dueDate:'',labels:[],assignees:[]};
  document.getElementById('tmodal').innerHTML = `
    <div class="m-hdr">
      <span class="m-ttl">${isNew?'Neue Aufgabe erstellen':'Aufgabe bearbeiten'}</span>
      <button class="btn btn-sm" onclick="closeModal()">✕</button>
    </div>
    <div class="fg"><label class="fl">Titel *</label><input class="fi" id="f-title" value="${esc(t.title)}" placeholder="Aufgabentitel…"></div>
    <div class="fg"><label class="fl">Beschreibung</label><textarea class="fta" id="f-desc">${esc(t.desc||'')}</textarea></div>
    <div class="fr2">
      <div class="fg"><label class="fl">Status</label><select class="fs" id="f-bucket">
        ${['Backlog','To-Do','In Progress','Done'].map(b=>`<option${b===t.bucket?' selected':''}>${b}</option>`).join('')}
      </select></div>
      <div class="fg"><label class="fl">Priorität</label><select class="fs" id="f-priority">
        ${['low','medium','high','critical'].map(p=>`<option value="${p}"${p===t.priority?' selected':''}>${PRIO_LBL[p]}</option>`).join('')}
      </select></div>
    </div>
    <div class="fr2">
      <div class="fg"><label class="fl">Startdatum</label><input class="fi" type="date" id="f-start" value="${t.startDate||''}"></div>
      <div class="fg"><label class="fl">Fälligkeitsdatum</label><input class="fi" type="date" id="f-due" value="${t.dueDate||''}"></div>
    </div>
    <div class="fg">
      <div class="prog-lbl">
        <label class="fl" style="margin:0">Fortschritt</label>
        <span id="prog-val" style="font-size:13px;font-weight:600;color:var(--accent)">${t.progress}%</span>
      </div>
      <input type="range" min="0" max="100" step="5" value="${t.progress}" oninput="document.getElementById('prog-val').textContent=this.value+'%'" id="f-progress">
    </div>
    <div class="fg"><label class="fl">Labels (kommagetrennt)</label><input class="fi" id="f-labels" value="${esc((t.labels||[]).join(', '))}"></div>
    <div class="m-foot">
      ${!isNew?`<button class="btn btn-danger" onclick="deleteTask(${t.id})" style="margin-right:auto">Löschen</button>`:''}
      <button class="btn" onclick="closeModal()">Abbrechen</button>
      <button class="btn btn-accent" id="modal-save-btn" onclick="saveTask(${id||'null'})">Speichern</button>
    </div>`;
  document.getElementById('modal-ov').style.display='flex';
}

function closeModal() { document.getElementById('modal-ov').style.display='none'; }

async function saveTask(id) {
  const g = i => (document.getElementById(i)?.value||'').trim();
  const taskData = {
    title:     g('f-title') || 'Neue Aufgabe',
    desc:      g('f-desc'),
    bucket:    g('f-bucket'),
    priority:  g('f-priority'),
    progress:  parseInt(document.getElementById('f-progress')?.value || '0'),
    startDate: g('f-start'),
    dueDate:   g('f-due'),
    labels:    g('f-labels').split(',').map(s=>s.trim()).filter(Boolean),
    assignees: [],
    listId:    S.filterListId,
  };

  const btn = document.getElementById('modal-save-btn');
  if (btn) { btn.disabled = true; btn.textContent = 'Speichern…'; }

  try {
    if (id) {
      const resp = await fetch(`/api/todos/${id}`, {
        method: 'PUT',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(taskData)
      });
      const updated = await resp.json();
      const i = S.tasks.findIndex(x => x.id === id);
      if (i >= 0) S.tasks[i] = updated;
    } else {
      const resp = await fetch('/api/todos', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(taskData)
      });
      const created = await resp.json();
      S.tasks.push(created);
    }
    closeModal();
    render();
  } catch(e) {
    alert('Fehler beim Speichern: ' + e.message);
    if (btn) { btn.disabled = false; btn.textContent = 'Speichern'; }
  }
}

async function deleteTask(id) {
  if (!confirm('Aufgabe wirklich löschen?')) return;
  try {
    await fetch(`/api/todos/${id}`, {method: 'DELETE'});
    S.tasks = S.tasks.filter(t => t.id !== id);
    closeModal();
    render();
  } catch(e) { alert('Fehler beim Löschen'); }
}

async function doLogout() {
  await fetch('/api/auth/logout', {method: 'POST'});
  window.location.href = '/login';
}

function toggleAI() {
  S.showAI = !S.showAI;
  document.getElementById('aip').classList.toggle('open', S.showAI);
  if (S.showAI) renderAIMsgs();
}
function renderAIMsgs() {
  const el = document.getElementById('ai-msgs');
  if (!el) return;
  el.innerHTML = S.aiMsgs.map(m=>`<div class="ai-msg ${m.role}">${m.text.replace(/\\n/g,'<br>').replace(/\\*\\*(.*?)\\*\\*/g,'<strong>$1</strong>')}</div>`).join('');
  el.scrollTop = el.scrollHeight;
}
function aiSend() {
  const el = document.getElementById('ai-in');
  if (!el) return;
  const v = el.value.trim();
  if (!v) return;
  el.value = '';
  aiAsk(v);
}
async function aiAsk(msg) {
  const apiKey = (document.getElementById('ai-key-in')||{}).value || localStorage.getItem('tf_apikey') || '';
  S.aiMsgs.push({role:'user',text:msg});
  if (!S.showAI) toggleAI();
  else renderAIMsgs();
  const taskSummary = S.tasks.map(t=>`- ${t.title} [${t.bucket}, ${t.priority}, ${t.progress}%, Fällig:${t.dueDate||'–'}${isOv(t)?' ÜBERFÄLLIG':''}]`).join('\\n');
  S.aiMsgs.push({role:'ai loading',text:'Analysiere…'});
  renderAIMsgs();
  try {
    if (!apiKey) throw new Error('Kein API Key. Bitte oben eintragen.');
    const resp = await fetch('https://api.anthropic.com/v1/messages', {
      method:'POST',
      headers:{
        'Content-Type':'application/json',
        'x-api-key':apiKey,
        'anthropic-version':'2023-06-01',
        'anthropic-dangerous-direct-browser-access':'true'
      },
      body:JSON.stringify({
        model:'claude-sonnet-4-20250514',max_tokens:1000,
        system:`Du bist ein KI-Assistent für Projektmanagement. Aktuelle Aufgaben:\\n${taskSummary}\\n\\nAntworte auf Deutsch, präzise und hilfreich.`,
        messages:S.aiMsgs.filter(m=>m.role==='user'||m.role==='ai').map(m=>({role:m.role==='ai'?'assistant':'user',content:m.text}))
      })
    });
    const data = await resp.json();
    const text = data.content?.map(c=>c.text||'').join('') || 'Keine Antwort erhalten.';
    S.aiMsgs.pop();
    S.aiMsgs.push({role:'ai',text});
  } catch(e) {
    S.aiMsgs.pop();
    S.aiMsgs.push({role:'ai',text:`Fehler: ${e.message}`});
  }
  renderAIMsgs();
}

function toggleDark() {
  const dark = document.documentElement.hasAttribute('data-dark');
  if (dark) {
    document.documentElement.removeAttribute('data-dark');
    document.getElementById('dark-lbl').textContent = 'Dark Mode';
    try { localStorage.setItem('tf_dark','0'); } catch(e){}
  } else {
    document.documentElement.setAttribute('data-dark','');
    document.getElementById('dark-lbl').textContent = 'Light Mode';
    try { localStorage.setItem('tf_dark','1'); } catch(e){}
  }
}

function toggleSidebar() {
  const sb = document.getElementById('sidebar');
  const ov = document.getElementById('sb-overlay');
  const open = sb.classList.toggle('open');
  ov.style.display = open ? 'block' : 'none';
}
function closeSidebar() {
  document.getElementById('sidebar').classList.remove('open');
  document.getElementById('sb-overlay').style.display = 'none';
}

function setupResponsive() {
  const mq = window.matchMedia('(max-width: 767px)');
  function upd(m) {
    const menuBtn = document.getElementById('menu-btn');
    if (menuBtn) menuBtn.style.display = m.matches ? 'flex' : 'none';
  }
  mq.addEventListener('change', upd);
  upd(mq);
}

function initApp() {
  if (!document.getElementById('taskflow-app')) {
    setTimeout(initApp, 50);
    return;
  }
  loadData();
  setupResponsive();
  renderLists();
  render();
  if (document.documentElement.hasAttribute('data-dark')) {
    const lbl = document.getElementById('dark-lbl');
    if (lbl) lbl.textContent = 'Light Mode';
  }
}
setTimeout(initApp, 100);

window.setView = setView;
window.openModal = openModal;
window.closeModal = closeModal;
window.saveTask = saveTask;
window.deleteTask = deleteTask;
window.drop = drop;
window.dragStart = dragStart;
window.dragEnd = dragEnd;
window.toggleAI = toggleAI;
window.aiSend = aiSend;
window.toggleDark = toggleDark;
window.toggleSidebar = toggleSidebar;
window.closeSidebar = closeSidebar;
window.selectList = selectList;
window.promptNewList = promptNewList;
window.doLogout = doLogout;
window.renderCalendar = renderCalendar;
window.S = S;
"""
