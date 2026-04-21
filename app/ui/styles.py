HEAD_HTML = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #F4F5FA;
  --surface: #FFFFFF;
  --surface2: #F0F2F8;
  --border: #E4E7F0;
  --border2: #CDD2E0;
  --text: #1A1D2E;
  --text2: #64708A;
  --text3: #9DA8C0;
  --accent: #4361EE;
  --accent-lt: #EEF1FE;
  --success: #0E9F6E;
  --success-lt: #E8F8F3;
  --warning: #C27803;
  --warning-lt: #FFF8E7;
  --danger: #E02424;
  --danger-lt: #FEF2F2;
  --shadow: 0 1px 3px rgba(0,0,0,.07),0 1px 2px rgba(0,0,0,.04);
  --shadow-md: 0 4px 12px rgba(0,0,0,.1);
  --r: 10px;
  --r-sm: 6px;
  --r-lg: 14px;
  --font: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --sidebar-w: 220px;
  --nav-h: 58px;
}
[data-dark] {
  --bg: #0D1117;
  --surface: #161B22;
  --surface2: #21262D;
  --border: #30363D;
  --border2: #484F58;
  --text: #E6EDF3;
  --text2: #8B949E;
  --text3: #6E7681;
  --accent: #7C8FFC;
  --accent-lt: #1A1F3A;
  --success: #3FB950;
  --success-lt: #0D2119;
  --warning: #D29922;
  --warning-lt: #2A1F0A;
  --danger: #F85149;
  --danger-lt: #2D1A1A;
}

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--font);font-size:14px;color:var(--text);background:var(--bg);-webkit-font-smoothing:antialiased}
button{font-family:var(--font);cursor:pointer;border:none;background:none}
input,select,textarea{font-family:var(--font);font-size:14px;color:var(--text)}
a{text-decoration:none}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--border2);border-radius:10px}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}

#taskflow-app{display:flex;height:100vh;overflow:hidden;position:relative}

#sidebar{
  width:var(--sidebar-w);flex-shrink:0;
  background:var(--surface);border-right:1px solid var(--border);
  display:flex;flex-direction:column;overflow-y:auto;
  transition:transform .25s ease;z-index:50;
}
.sb-logo{
  padding:16px 18px;font-size:15px;font-weight:600;
  border-bottom:1px solid var(--border);
  color:var(--accent);display:flex;align-items:center;gap:9px;
  flex-shrink:0;letter-spacing:-.3px;
}
.sb-sec{padding:16px 14px 5px;font-size:11px;font-weight:600;color:var(--text3);text-transform:uppercase;letter-spacing:.7px}
.sb-item{
  display:flex;align-items:center;gap:9px;padding:8px 10px;
  border-radius:var(--r-sm);margin:2px 8px;cursor:pointer;
  color:var(--text2);font-size:13.5px;transition:background .12s,color .12s;
}
.sb-item:hover{background:var(--bg);color:var(--text)}
.sb-item.active{background:var(--accent-lt);color:var(--accent);font-weight:500}
.sb-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.sb-fill{flex:1}
.sb-bottom{padding:10px 8px;border-top:1px solid var(--border)}

#sb-overlay{position:fixed;inset:0;background:rgba(0,0,0,.4);z-index:40;display:none}

#main{flex:1;min-width:0;display:flex;flex-direction:column;overflow:hidden}

#topbar{background:var(--surface);border-bottom:1px solid var(--border);flex-shrink:0;z-index:20}
.tb1{display:flex;align-items:center;gap:10px;padding:10px 16px;border-bottom:1px solid var(--border)}
.proj-title{font-size:15px;font-weight:600;letter-spacing:-.3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sp{flex:1}
.tb2{display:flex;align-items:center;padding:4px 16px;gap:2px;overflow-x:auto}
.tb2::-webkit-scrollbar{height:0}
.vtab{
  padding:6px 13px;font-size:13px;cursor:pointer;
  color:var(--text2);border-radius:var(--r-sm);
  display:flex;align-items:center;gap:5px;white-space:nowrap;
  transition:background .12s,color .12s;user-select:none;
}
.vtab:hover{background:var(--surface2);color:var(--text)}
.vtab.active{color:var(--accent);font-weight:500;border-bottom:2px solid var(--accent);border-radius:0}

.btn{
  padding:6px 12px;border:1px solid var(--border2);border-radius:var(--r-sm);
  font-size:13px;background:var(--surface);color:var(--text);
  display:inline-flex;align-items:center;gap:5px;white-space:nowrap;
  transition:background .12s,border-color .12s;cursor:pointer;
}
.btn:hover{background:var(--surface2);border-color:var(--border)}
.btn-accent{background:var(--accent);color:#fff;border-color:transparent;font-weight:500}
.btn-accent:hover{opacity:.88;background:var(--accent)}
.btn-sm{padding:4px 9px;font-size:12px}
.btn-icon{padding:6px;border-radius:var(--r-sm)}
.btn-danger{color:var(--danger);border-color:var(--danger)}
.btn-danger:hover{background:var(--danger-lt)}

.sbox,.sel,.fi,.fs,.fta{
  padding:7px 11px;border:1px solid var(--border);border-radius:var(--r-sm);
  background:var(--surface2);color:var(--text);
  transition:border-color .12s;outline:none;
}
.sbox:focus,.sel:focus,.fi:focus,.fs:focus,.fta:focus{border-color:var(--accent);background:var(--surface)}
.sbox{width:150px}
.fta{min-height:80px;resize:vertical;width:100%;display:block}
.fi,.fs{width:100%;display:block}

#content{flex:1;overflow-y:auto;overflow-x:hidden;position:relative}

.pb{font-size:11.5px;padding:2px 8px;border-radius:5px;font-weight:500;flex-shrink:0}
.p-low{background:#ECFDF5;color:#065F46}
.p-medium{background:#FFFBEB;color:#92400E}
.p-high{background:#FFF7ED;color:#9A3412}
.p-critical{background:#FEF2F2;color:#991B1B}
[data-dark] .p-low{background:#064E3B;color:#6EE7B7}
[data-dark] .p-medium{background:#451A03;color:#FCD34D}
[data-dark] .p-high{background:#431407;color:#FDBA74}
[data-dark] .p-critical{background:#450A0A;color:#FCA5A5}
.lbl-badge{font-size:11px;padding:2px 7px;border-radius:4px;background:var(--accent-lt);color:var(--accent)}

.avs{display:flex}
.av{
  width:22px;height:22px;border-radius:50%;font-size:9px;font-weight:600;
  display:flex;align-items:center;justify-content:center;
  border:2px solid var(--surface);flex-shrink:0;margin-left:-5px;
}
.av:first-child{margin-left:0}

.board{display:flex;gap:14px;padding:16px;align-items:flex-start;min-height:100%}
.board-col{
  width:270px;flex-shrink:0;
  background:var(--surface);border:1px solid var(--border);
  border-radius:var(--r-lg);display:flex;flex-direction:column;
  max-height:calc(100vh - 130px);box-shadow:var(--shadow);
}
.col-hdr{
  padding:11px 14px;border-bottom:1px solid var(--border);
  display:flex;align-items:center;gap:9px;
  font-weight:600;font-size:13.5px;flex-shrink:0;
}
.col-cnt{
  font-size:11px;font-weight:500;background:var(--surface2);
  border:1px solid var(--border);border-radius:10px;
  padding:1px 8px;color:var(--text2);margin-left:auto;
}
.col-tasks{
  padding:8px;overflow-y:auto;display:flex;
  flex-direction:column;gap:7px;flex:1;min-height:60px;
}
.col-tasks.dov{background:var(--accent-lt);border-radius:var(--r-sm)}
.tc{
  background:var(--surface);border:1px solid var(--border);
  border-radius:var(--r);padding:11px 13px;cursor:pointer;
  user-select:none;box-shadow:var(--shadow);
  transition:border-color .12s,box-shadow .12s,transform .12s;
}
.tc:hover{border-color:var(--border2);box-shadow:var(--shadow-md);transform:translateY(-1px)}
.tc.dragging{opacity:.35;transform:scale(.97)}
.t-ttl{font-size:13.5px;font-weight:500;margin-bottom:8px;line-height:1.45;color:var(--text)}
.t-meta{display:flex;align-items:center;gap:5px;flex-wrap:wrap}
.t-due{font-size:11px;color:var(--text3);margin-left:auto;white-space:nowrap}
.t-due.ov{color:var(--danger);font-weight:600}
.pgw{height:3px;background:var(--border);border-radius:2px;margin-top:9px;overflow:hidden}
.pgb{height:100%;border-radius:2px;background:var(--success);transition:width .3s}
.col-add{
  width:100%;padding:8px 14px;text-align:left;font-size:13px;
  color:var(--text3);border-top:1px solid var(--border);
  flex-shrink:0;border-radius:0 0 var(--r-lg) var(--r-lg);
  transition:color .12s,background .12s;
}
.col-add:hover{color:var(--accent);background:var(--accent-lt)}

.ltbl{width:100%;border-collapse:collapse;min-width:700px}
.ltbl th{
  text-align:left;padding:10px 14px;font-size:12px;font-weight:600;
  color:var(--text2);border-bottom:1px solid var(--border);
  cursor:pointer;user-select:none;white-space:nowrap;
  position:sticky;top:0;background:var(--surface);z-index:2;
}
.ltbl th:hover{color:var(--text)}
.ltbl td{padding:9px 14px;border-bottom:1px solid var(--border);vertical-align:middle;font-size:13.5px}
.ltbl tr{cursor:pointer}
.ltbl tr:hover td{background:var(--surface2)}
.ltbl td.ov{color:var(--danger);font-weight:600}
.list-wrap{overflow-x:auto;height:100%}

.gwrap{overflow:auto;height:100%;-webkit-overflow-scrolling:touch}
.ginner{display:inline-block;min-width:100%}
.ghdr{display:flex;position:sticky;top:0;z-index:6;background:var(--surface);border-bottom:1px solid var(--border)}
.gncol{
  width:220px;flex-shrink:0;padding:9px 14px;
  font-size:12px;font-weight:600;color:var(--text2);
  position:sticky;left:0;z-index:8;
  background:var(--surface);border-right:1px solid var(--border);
}
.gtl-h{flex:1;position:relative;height:36px;min-width:800px;overflow:hidden}
.grow{display:flex;border-bottom:1px solid var(--border);height:44px}
.grow:hover{background:var(--surface2)}
.gname{
  width:220px;flex-shrink:0;padding:0 14px;
  border-right:1px solid var(--border);
  display:flex;align-items:center;gap:8px;overflow:hidden;
  position:sticky;left:0;z-index:4;
  background:var(--surface);transition:background .12s;font-size:13.5px;
}
.grow:hover .gname{background:var(--surface2)}
.gname-txt{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.gtl{flex:1;position:relative;min-width:800px;overflow:hidden}
.gbar{
  position:absolute;height:24px;top:10px;border-radius:5px;
  cursor:pointer;display:flex;align-items:center;padding:0 9px;
  font-size:11.5px;overflow:hidden;white-space:nowrap;font-weight:500;
  color:#fff;transition:opacity .15s;
}
.gbar:hover{opacity:.82}
.gtoday-ln{position:absolute;top:0;bottom:0;width:2px;pointer-events:none;z-index:5;background:var(--danger)}
.gdl{
  position:absolute;font-size:10px;color:var(--text3);
  height:36px;display:flex;flex-direction:column;
  justify-content:space-around;padding:2px 5px;
  border-right:1px solid var(--border);overflow:hidden;white-space:nowrap;
}
.gdl.gdl-month{color:var(--text2);font-weight:600;font-size:11px}

.cal-wrap{padding:16px}
.cal-nav{display:flex;align-items:center;gap:12px;margin-bottom:14px}
.cal-title{font-size:16px;font-weight:600;letter-spacing:-.3px}
.cal-g{display:grid;grid-template-columns:repeat(7,1fr);border:1px solid var(--border);border-radius:var(--r-lg);overflow:hidden}
.cal-dh{padding:8px 6px;font-size:11.5px;font-weight:600;color:var(--text2);background:var(--surface2);text-align:center;border-bottom:1px solid var(--border)}
.cal-day{min-height:90px;background:var(--surface);padding:7px;cursor:pointer;border-right:1px solid var(--border);border-bottom:1px solid var(--border);transition:background .1s}
.cal-day:hover{background:var(--surface2)}
.cal-day.today{background:var(--accent-lt)}
.cal-day.other{opacity:.4}
.cal-day:nth-child(7n){border-right:none}
.cal-dn{font-size:12.5px;font-weight:500;margin-bottom:4px}
.cal-day.today .cal-dn{color:var(--accent);font-weight:700}
.cal-t{font-size:11px;padding:2px 5px;border-radius:3px;margin-bottom:2px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}

.dash-wrap{padding:16px}
.stats-g{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:18px}
.stat-c{background:var(--surface);border:1px solid var(--border);border-radius:var(--r-lg);padding:18px;box-shadow:var(--shadow)}
.stat-l{font-size:12px;color:var(--text2);margin-bottom:7px;font-weight:500}
.stat-v{font-size:28px;font-weight:600;letter-spacing:-.5px}
.charts-g{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.chart-c{background:var(--surface);border:1px solid var(--border);border-radius:var(--r-lg);padding:18px;box-shadow:var(--shadow)}
.chart-t{font-size:13.5px;font-weight:600;margin-bottom:14px;letter-spacing:-.2px}
.prow{display:flex;align-items:center;gap:10px;margin-bottom:10px;font-size:13px}
.prow-name{min-width:80px;color:var(--text2);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.prow-bw{flex:1;height:7px;background:var(--surface2);border-radius:4px;overflow:hidden}
.prow-b{height:100%;border-radius:4px;transition:width .4s ease}
.prow-v{min-width:36px;text-align:right;color:var(--text2);font-size:12px}

#modal-ov{
  position:fixed;inset:0;background:rgba(0,0,0,.5);
  z-index:100;display:flex;align-items:center;justify-content:center;padding:16px;
}
#tmodal{
  background:var(--surface);border-radius:var(--r-lg);
  border:1px solid var(--border);width:100%;max-width:500px;
  max-height:90vh;overflow-y:auto;padding:22px;box-shadow:var(--shadow-md);
}
.m-hdr{display:flex;align-items:center;justify-content:space-between;margin-bottom:18px}
.m-ttl{font-size:16px;font-weight:600;letter-spacing:-.3px}
.fg{margin-bottom:15px}
.fl{display:block;font-size:12.5px;font-weight:600;color:var(--text2);margin-bottom:6px;letter-spacing:.1px}
.fr2{display:grid;grid-template-columns:1fr 1fr;gap:13px}
.m-foot{display:flex;gap:8px;justify-content:flex-end;margin-top:18px;padding-top:16px;border-top:1px solid var(--border)}
.prog-lbl{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px}
input[type=range]{width:100%;accent-color:var(--accent);cursor:pointer}

#aip{
  position:fixed;right:0;top:0;bottom:0;width:320px;
  background:var(--surface);border-left:1px solid var(--border);
  z-index:80;display:flex;flex-direction:column;
  box-shadow:-4px 0 20px rgba(0,0,0,.08);
  transform:translateX(100%);transition:transform .25s ease;
}
#aip.open{transform:translateX(0)}
.ai-hdr{padding:14px 16px;border-bottom:1px solid var(--border);font-weight:600;font-size:14px;display:flex;align-items:center;justify-content:space-between;flex-shrink:0;gap:8px}
.ai-key-row{padding:10px 14px;border-bottom:1px solid var(--border);flex-shrink:0}
.ai-key-inp{width:100%;padding:7px 10px;border:1px solid var(--border);border-radius:var(--r-sm);background:var(--surface2);color:var(--text);font-size:12px}
.ai-quick{padding:8px 12px;display:flex;gap:6px;flex-wrap:wrap;border-bottom:1px solid var(--border);flex-shrink:0}
.ai-qb{font-size:11.5px;padding:4px 10px;border:1px solid var(--border);border-radius:20px;cursor:pointer;background:var(--surface2);color:var(--text2);transition:all .12s}
.ai-qb:hover{background:var(--accent-lt);color:var(--accent);border-color:var(--accent)}
.ai-msgs{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:9px}
.ai-msg{padding:11px 13px;border-radius:var(--r);font-size:13px;line-height:1.55}
.ai-msg.user{background:var(--accent-lt);color:var(--accent);margin-left:20px;font-weight:500}
.ai-msg.ai{background:var(--surface2);color:var(--text);margin-right:20px}
.ai-msg.loading{color:var(--text3);font-style:italic}
.ai-in-row{padding:12px 14px;border-top:1px solid var(--border);display:flex;gap:8px;flex-shrink:0}
.ai-in{flex:1;padding:8px 12px;border:1px solid var(--border);border-radius:var(--r-sm);background:var(--surface2);color:var(--text);font-size:13px}
.ai-in:focus{outline:none;border-color:var(--accent)}

#mobile-nav{display:none;position:fixed;bottom:0;left:0;right:0;background:var(--surface);border-top:1px solid var(--border);z-index:60;height:var(--nav-h)}
.mnav{display:flex;height:100%}
.mnav-item{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;font-size:11px;color:var(--text2);cursor:pointer;transition:color .12s;padding:4px 0}
.mnav-item svg{transition:transform .15s}
.mnav-item.active{color:var(--accent)}
.mnav-item.active svg{transform:scale(1.1)}
.mnav-item span{font-weight:500;font-size:10.5px}

@media (max-width:1023px){.stats-g{grid-template-columns:repeat(2,1fr)}.charts-g{grid-template-columns:1fr}}
@media (max-width:767px){
  :root{--sidebar-w:240px}
  #sidebar{position:fixed;top:0;bottom:0;left:0;transform:translateX(-100%);transition:transform .25s ease;z-index:50}
  #sidebar.open{transform:translateX(0)}
  #mobile-nav{display:block}
  body{padding-bottom:var(--nav-h)}
  #main{height:calc(100vh - var(--nav-h));margin-bottom:0}
  #content{height:calc(100vh - var(--nav-h) - 95px)}
  .tb2{display:none}
  .sbox{width:120px}
  .stats-g{grid-template-columns:repeat(2,1fr)}
  .board{padding:10px 8px;gap:10px}
  .board-col{width:250px}
  .fr2{grid-template-columns:1fr}
  #tmodal{position:fixed;bottom:0;left:0;right:0;max-width:100%;border-radius:var(--r-lg) var(--r-lg) 0 0;padding:20px 16px;max-height:92vh}
  #modal-ov{padding:0;align-items:flex-end}
  #aip{width:100%}
  .proj-title{font-size:13.5px}
  .cal-day{min-height:60px}
  .cal-t{display:none}
}
@media (max-width:480px){.stats-g{grid-template-columns:1fr 1fr}.board-col{width:230px}.btn span{display:none}}

@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.fade-in{animation:fadeIn .2s ease forwards}
@keyframes spin{to{transform:rotate(360deg)}}
.spin{animation:spin 1s linear infinite;display:inline-block}
</style>
"""

AUTH_OVERRIDE_CSS = """
<style>
body { background: var(--bg) !important; overflow: auto; }
.nicegui-content { padding: 0 !important; max-width: none !important; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
</style>
"""

APP_OVERRIDE_CSS = """
<style>
html, body { height: 100%; overflow: hidden !important; margin: 0; padding: 0; }
body { background: var(--bg) !important; }
.nicegui-content { padding: 0 !important; max-width: none !important; height: 100%; display: block; }
</style>
"""
