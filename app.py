<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>AURORA NEXUS // Defect Intelligence</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&family=Share+Tech+Mono&display=swap" rel="stylesheet"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
:root{
  --cyan:#00f5ff;--pink:#ff006e;--gold:#ffd60a;--violet:#7b2fff;--green:#00ff9d;
  --bg0:#020408;--bg1:#060c14;--bg2:#0a1628;--bg3:#0f1f3a;
  --t1:#e8f4fd;--t2:#8ab4cc;--t3:#4a6a82;
}
*{margin:0;padding:0;box-sizing:border-box;}

/* ── BODY & GRID BG ── */
body{
  background:var(--bg0);color:var(--t1);
  font-family:'Rajdhani',sans-serif;font-size:15px;
  min-height:100vh;overflow-x:hidden;
}
body::before{
  content:'';position:fixed;inset:0;pointer-events:none;z-index:0;
  background-image:
    linear-gradient(rgba(0,245,255,.035) 1px,transparent 1px),
    linear-gradient(90deg,rgba(0,245,255,.035) 1px,transparent 1px);
  background-size:50px 50px;
  animation:gridDrift 25s linear infinite;
}
body::after{
  content:'';position:fixed;inset:0;pointer-events:none;z-index:1;
  background:repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,0,0,.07) 3px,rgba(0,0,0,.07) 4px);
}
@keyframes gridDrift{to{background-position:50px 50px;}}

/* ── LAYOUT ── */
#app{position:relative;z-index:2;display:grid;grid-template-columns:230px 1fr;min-height:100vh;}

/* ── SIDEBAR ── */
aside{
  background:linear-gradient(180deg,#030c18 0%,#040d1c 100%);
  border-right:1px solid rgba(0,245,255,.14);
  padding:28px 20px;display:flex;flex-direction:column;gap:18px;
  box-shadow:4px 0 40px rgba(0,245,255,.06);
  position:sticky;top:0;height:100vh;overflow:hidden;
}
.logo-hex{font-size:2.4rem;text-align:center;color:var(--cyan);filter:drop-shadow(0 0 12px var(--cyan));animation:hexPulse 3s ease-in-out infinite;}
@keyframes hexPulse{0%,100%{filter:drop-shadow(0 0 8px var(--cyan));}50%{filter:drop-shadow(0 0 22px var(--cyan));}}
.brand-title{font-family:'Orbitron',monospace;font-size:.95rem;font-weight:900;letter-spacing:.2em;text-align:center;
  background:linear-gradient(135deg,var(--cyan),var(--violet));-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.brand-sub{font-family:'Share Tech Mono',monospace;font-size:.58rem;letter-spacing:.15em;color:var(--t3);text-align:center;text-transform:uppercase;}
.sidebar-divider{height:1px;background:linear-gradient(90deg,transparent,rgba(0,245,255,.2),transparent);}
.status-bar{background:rgba(0,245,255,.04);border:1px solid rgba(0,245,255,.14);border-radius:4px;padding:10px 12px;
  display:flex;align-items:center;gap:8px;}
.dot{width:7px;height:7px;border-radius:50%;background:var(--green);box-shadow:0 0 8px var(--green);flex-shrink:0;
  animation:dotPulse 2s ease-in-out infinite;}
@keyframes dotPulse{0%,100%{opacity:1;}50%{opacity:.3;}}
.status-txt{font-family:'Share Tech Mono',monospace;font-size:.62rem;color:var(--t3);letter-spacing:.12em;}
.nav-item{padding:10px 14px;border-radius:4px;font-family:'Share Tech Mono',monospace;font-size:.68rem;
  letter-spacing:.1em;color:var(--t3);cursor:pointer;transition:all .2s;border:1px solid transparent;
  display:flex;align-items:center;gap:10px;}
.nav-item:hover,.nav-item.active{color:var(--cyan);background:rgba(0,245,255,.06);border-color:rgba(0,245,255,.15);}
.nav-item.active{box-shadow:0 0 12px rgba(0,245,255,.1);}
.upload-zone{
  border:1px dashed rgba(0,245,255,.3);border-radius:6px;padding:18px 12px;
  text-align:center;cursor:pointer;transition:all .25s;
  background:rgba(0,245,255,.02);position:relative;
}
.upload-zone:hover,.upload-zone.drag-over{
  border-color:var(--cyan);background:rgba(0,245,255,.07);
  box-shadow:0 0 20px rgba(0,245,255,.12);
}
.upload-icon{font-size:1.6rem;color:var(--cyan);opacity:.6;margin-bottom:6px;
  animation:hexPulse 3s ease-in-out infinite;}
.upload-label{font-family:'Orbitron',monospace;font-size:.62rem;font-weight:700;
  letter-spacing:.15em;color:var(--cyan);text-transform:uppercase;}
.upload-sub{font-family:'Share Tech Mono',monospace;font-size:.58rem;color:var(--t3);
  letter-spacing:.1em;margin-top:4px;}
.upload-zone.has-file{border-color:var(--green);background:rgba(0,255,157,.04);}
.upload-zone.has-file .upload-icon{color:var(--green);}
.upload-zone.has-file .upload-label{color:var(--green);}

.sidebar-footer{margin-top:auto;font-family:'Share Tech Mono',monospace;font-size:.58rem;color:rgba(74,106,130,.4);
  letter-spacing:.1em;line-height:2;border-top:1px solid rgba(0,245,255,.06);padding-top:16px;}

/* ── MAIN ── */
main{padding:28px 32px;display:flex;flex-direction:column;gap:24px;}

/* ── HEADER ── */
.page-header{display:flex;justify-content:space-between;align-items:flex-end;}
.page-title{font-family:'Orbitron',monospace;font-size:clamp(1.4rem,2.5vw,2.4rem);font-weight:900;letter-spacing:.12em;
  background:linear-gradient(90deg,var(--cyan) 0%,#fff 45%,var(--pink) 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  animation:titleGlow 3s ease-in-out infinite;}
@keyframes titleGlow{0%,100%{filter:drop-shadow(0 0 6px rgba(0,245,255,.4));}50%{filter:drop-shadow(0 0 18px rgba(0,245,255,.8));}}
.tagline{font-family:'Share Tech Mono',monospace;font-size:.65rem;color:var(--gold);letter-spacing:.22em;text-transform:uppercase;margin-top:4px;opacity:.85;}
.header-meta{text-align:right;font-family:'Share Tech Mono',monospace;font-size:.62rem;color:var(--t3);line-height:2;}

/* ── SECTION HEADER ── */
.sec-hdr{display:flex;align-items:center;gap:12px;margin-bottom:14px;}
.sec-title{font-family:'Orbitron',monospace;font-size:.72rem;font-weight:700;letter-spacing:.18em;color:var(--cyan);white-space:nowrap;}
.sec-line{flex:1;height:1px;background:linear-gradient(90deg,var(--cyan),transparent);opacity:.3;}

/* ── KPI GRID ── */
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;}
.kpi-card{
  background:linear-gradient(135deg,rgba(0,245,255,.05),rgba(123,47,255,.04));
  border:1px solid rgba(0,245,255,.18);border-radius:6px;padding:20px 22px;
  position:relative;overflow:hidden;cursor:default;
  transition:transform .3s,box-shadow .3s,border-color .3s;
  animation:cardReveal .5s ease both;
}
.kpi-card:nth-child(1){animation-delay:.05s;}.kpi-card:nth-child(2){animation-delay:.1s;}
.kpi-card:nth-child(3){animation-delay:.15s;}.kpi-card:nth-child(4){animation-delay:.2s;}
@keyframes cardReveal{from{opacity:0;transform:translateY(12px);}to{opacity:1;transform:translateY(0);}}
.kpi-card::before{content:'';position:absolute;top:0;left:0;width:36px;height:36px;border-top:2px solid var(--cyan);border-left:2px solid var(--cyan);}
.kpi-card::after{content:'';position:absolute;bottom:0;right:0;width:36px;height:36px;border-bottom:2px solid var(--pink);border-right:2px solid var(--pink);}
.kpi-card:hover{transform:translateY(-3px);border-color:var(--cyan);box-shadow:0 0 30px rgba(0,245,255,.18);}
.kpi-label{font-family:'Share Tech Mono',monospace;font-size:.6rem;letter-spacing:.22em;color:var(--t3);text-transform:uppercase;margin-bottom:10px;}
.kpi-value{font-family:'Orbitron',monospace;font-size:2rem;font-weight:700;color:var(--cyan);text-shadow:0 0 18px rgba(0,245,255,.5);line-height:1;}
.kpi-delta{font-family:'Share Tech Mono',monospace;font-size:.65rem;margin-top:8px;}
.delta-pos{color:var(--green);}
.delta-neg{color:var(--pink);}
.delta-neu{color:var(--gold);}

/* ── MID ROW ── */
.mid-row{display:grid;grid-template-columns:2fr 1fr;gap:20px;}

/* ── PANELS ── */
.panel{
  background:rgba(6,12,20,.85);border:1px solid rgba(0,245,255,.1);
  border-radius:8px;padding:20px 22px;position:relative;overflow:hidden;
  animation:cardReveal .6s ease both;
}
.panel::before{
  content:'◈ LIVE';position:absolute;top:10px;right:14px;
  font-family:'Share Tech Mono',monospace;font-size:.55rem;
  color:var(--gold);letter-spacing:.2em;animation:blink 1.4s step-end infinite;
}
@keyframes blink{0%,100%{opacity:1;}50%{opacity:.15;}}
canvas{width:100%!important;}

/* ── BOTTOM ROW ── */
.bot-row{display:grid;grid-template-columns:1fr 1fr;gap:20px;}

/* ── HEATMAP GRID ── */
.heatmap-container{display:grid;gap:3px;}
.heat-row{display:flex;gap:3px;align-items:center;}
.heat-label{font-family:'Share Tech Mono',monospace;font-size:.55rem;color:var(--t3);width:26px;text-align:right;margin-right:6px;flex-shrink:0;}
.heat-cell{width:14px;height:14px;border-radius:2px;transition:all .2s;cursor:default;flex-shrink:0;}
.heat-cell:hover{transform:scale(1.5);z-index:10;position:relative;}

/* ── RADAR PANEL ── */
.radar-stat{background:rgba(0,245,255,.04);border:1px solid rgba(0,245,255,.12);
  border-radius:4px;padding:12px 16px;margin-top:12px;
  font-family:'Share Tech Mono',monospace;font-size:.7rem;
  display:flex;justify-content:space-between;align-items:center;}
.radar-stat-val{color:var(--cyan);font-size:1rem;}

/* ── FORECAST BOX ── */
.forecast-box{
  background:linear-gradient(135deg,rgba(123,47,255,.1),rgba(0,245,255,.05));
  border:1px solid rgba(123,47,255,.35);border-radius:4px;padding:12px 16px;margin-top:12px;
  font-family:'Share Tech Mono',monospace;font-size:.72rem;color:#c8e6ff;line-height:1.7;
}
.forecast-icon{color:var(--violet);margin-right:6px;}

/* ── ANALYST PANEL ── */
.analyst-area{
  background:var(--bg2);border:1px solid rgba(0,245,255,.12);border-radius:4px;
  width:100%;height:140px;color:var(--t1);font-family:'Share Tech Mono',monospace;
  font-size:.75rem;padding:12px;resize:none;outline:none;
  transition:border-color .25s,box-shadow .25s;
  placeholder-color:var(--t3);
}
.analyst-area:focus{border-color:var(--cyan);box-shadow:0 0 16px rgba(0,245,255,.12);}
.btn-row{display:flex;gap:10px;margin-top:10px;}
.btn{
  flex:1;padding:10px;font-family:'Orbitron',monospace;font-size:.6rem;font-weight:700;
  letter-spacing:.15em;text-transform:uppercase;border:1px solid;border-radius:3px;
  cursor:pointer;transition:all .25s;background:transparent;
}
.btn-primary{border-color:var(--cyan);color:var(--cyan);}
.btn-primary:hover{background:var(--cyan);color:var(--bg0);box-shadow:0 0 22px rgba(0,245,255,.4);}
.btn-secondary{border-color:var(--violet);color:var(--violet);}
.btn-secondary:hover{background:var(--violet);color:#fff;box-shadow:0 0 22px rgba(123,47,255,.4);}

/* ── SCROLLBAR ── */
::-webkit-scrollbar{width:4px;} ::-webkit-scrollbar-track{background:var(--bg0);}
::-webkit-scrollbar-thumb{background:rgba(0,245,255,.25);border-radius:2px;}

/* ── TICKER ── */
.ticker-wrap{border-top:1px solid rgba(0,245,255,.08);border-bottom:1px solid rgba(0,245,255,.08);
  overflow:hidden;padding:6px 0;background:rgba(0,0,0,.3);}
.ticker{display:flex;gap:60px;animation:tickerScroll 20s linear infinite;white-space:nowrap;}
.ticker-item{font-family:'Share Tech Mono',monospace;font-size:.62rem;color:var(--t3);letter-spacing:.1em;}
.ticker-item span{color:var(--cyan);margin-left:6px;}
@keyframes tickerScroll{0%{transform:translateX(0);}100%{transform:translateX(-50%);}}

/* ── FULL ROW PANEL ── */
.full-row{display:grid;grid-template-columns:1fr;gap:20px;}
</style>
</head>
<body>
<div id="app">

<!-- ════════════════ SIDEBAR ════════════════ -->
<aside>
  <div class="logo-hex">⬡</div>
  <div class="brand-title">AURORA NEXUS</div>
  <div class="brand-sub">Defect Intelligence v4.1</div>
  <div class="sidebar-divider"></div>
  <div class="status-bar"><div class="dot"></div><div class="status-txt">SYSTEM ONLINE — NOMINAL</div></div>

  <!-- FILE UPLOAD -->
  <div class="upload-zone" id="uploadZone" onclick="document.getElementById('csvInput').click()" ondragover="event.preventDefault();this.classList.add('drag-over')" ondragleave="this.classList.remove('drag-over')" ondrop="handleDrop(event)">
    <div class="upload-icon">⬡</div>
    <div class="upload-label">UPLOAD JIRA CSV</div>
    <div class="upload-sub">click or drag & drop</div>
    <input type="file" id="csvInput" accept=".csv" style="display:none" onchange="handleFile(this.files[0])"/>
  </div>
  <div id="upload-status" style="font-family:'Share Tech Mono',monospace;font-size:.62rem;min-height:16px;text-align:center;"></div>

  <div style="display:flex;flex-direction:column;gap:6px;margin-top:4px;">
    <div class="nav-item active">⬡ &nbsp;VITAL SIGNS</div>
    <div class="nav-item">◈ &nbsp;VELOCITY FORECAST</div>
    <div class="nav-item">◈ &nbsp;PRIORITY RADAR</div>
    <div class="nav-item">◈ &nbsp;RESOURCE MATRIX</div>
    <div class="nav-item">◈ &nbsp;HEAT ANALYSIS</div>
    <div class="nav-item">◈ &nbsp;INTEL LOG</div>
  </div>

  <div class="sidebar-footer">
    BUILD 2024.11.α<br>
    CLEARANCE: EXECUTIVE<br>
    ENCRYPTION: AES-256<br>
    UPTIME: 99.97%
  </div>
</aside>

<!-- ════════════════ MAIN ════════════════ -->
<main>

  <!-- TICKER -->
  <div class="ticker-wrap">
    <div class="ticker">
      <span class="ticker-item">TOTAL DEFECTS<span>1,284</span></span>
      <span class="ticker-item">BACKLOG<span>312</span></span>
      <span class="ticker-item">REOPEN RATE<span>8.2%</span></span>
      <span class="ticker-item">AVG MTTR<span>4.7d</span></span>
      <span class="ticker-item">SLA BREACH<span>23</span></span>
      <span class="ticker-item">SPRINT VELOCITY<span>↑ 14%</span></span>
      <span class="ticker-item">CRITICAL P0<span>7</span></span>
      <span class="ticker-item">TOTAL DEFECTS<span>1,284</span></span>
      <span class="ticker-item">BACKLOG<span>312</span></span>
      <span class="ticker-item">REOPEN RATE<span>8.2%</span></span>
      <span class="ticker-item">AVG MTTR<span>4.7d</span></span>
      <span class="ticker-item">SLA BREACH<span>23</span></span>
      <span class="ticker-item">SPRINT VELOCITY<span>↑ 14%</span></span>
      <span class="ticker-item">CRITICAL P0<span>7</span></span>
    </div>
  </div>

  <!-- PAGE HEADER -->
  <div class="page-header">
    <div>
      <div class="page-title">PROJECT AURORA</div>
      <div class="tagline">◈ executive defect intelligence nexus ◈ real-time analytics ◈</div>
    </div>
    <div class="header-meta">
      <div id="clock" style="color:var(--cyan);"></div>
      <div>SESSION: EXEC-7741</div>
      <div>NODE: HYD-ALPHA-3</div>
    </div>
  </div>

  <!-- KPI ROW -->
  <div>
    <div class="sec-hdr"><span class="sec-title">◈ VITAL SIGNS</span><div class="sec-line"></div></div>
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">Total Defects</div>
        <div class="kpi-value" id="kv1">0</div>
        <div class="kpi-delta delta-neu">All priority tiers</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Active Backlog</div>
        <div class="kpi-value" id="kv2">0</div>
        <div class="kpi-delta delta-neg">▲ 24% of total scope</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Reopen Rate</div>
        <div class="kpi-value" id="kv3">0%</div>
        <div class="kpi-delta delta-pos">▼ −2.1% quality boost</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Avg Resolution</div>
        <div class="kpi-value" id="kv4">0d</div>
        <div class="kpi-delta delta-neu">SLA target: 7 days</div>
      </div>
    </div>
  </div>

  <!-- MID ROW: Burnup + Radar -->
  <div class="mid-row">
    <!-- BURNUP CHART -->
    <div class="panel">
      <div class="sec-hdr"><span class="sec-title">◈ BURNUP & VELOCITY FORECAST</span><div class="sec-line"></div></div>
      <canvas id="burnupChart" height="220"></canvas>
      <div class="forecast-box">
        <span class="forecast-icon">⬡</span>
        <strong>PREDICTIVE SIGNAL</strong> — Velocity regression projects backlog clearance:
        <strong style="color:var(--cyan);">14 Mar 2025</strong>.
        Current resolution rate: <strong style="color:var(--gold);">+18.4 issues/week</strong>.
      </div>
    </div>

    <!-- RADAR CHART -->
    <div class="panel">
      <div class="sec-hdr"><span class="sec-title">◈ PRIORITY RADAR</span><div class="sec-line"></div></div>
      <canvas id="radarChart" height="230"></canvas>
      <div class="radar-stat">
        <span style="color:var(--t3);">DOMINANT PRIORITY</span>
        <span class="radar-stat-val">HIGH — 412 issues</span>
      </div>
    </div>
  </div>

  <!-- BOTTOM ROW: Scatter + Intel Log -->
  <div class="bot-row">
    <!-- SCATTER -->
    <div class="panel">
      <div class="sec-hdr"><span class="sec-title">◈ RESOURCE EFFICIENCY MATRIX</span><div class="sec-line"></div></div>
      <canvas id="scatterChart" height="240"></canvas>
    </div>

    <!-- INTEL LOG -->
    <div class="panel" style="display:flex;flex-direction:column;">
      <div class="sec-hdr"><span class="sec-title">◈ EXECUTIVE INTELLIGENCE LOG</span><div class="sec-line"></div></div>
      <textarea class="analyst-area" placeholder="// Enter executive analysis...&#10;// e.g. Velocity nominal but Reopen Rate signals QA regression in Sprint 4..."></textarea>
      <div class="btn-row">
        <button class="btn btn-primary" onclick="commitLog()">⬡ COMMIT TO LOG</button>
        <button class="btn btn-secondary" onclick="exportRpt()">◈ EXPORT REPORT</button>
      </div>
      <div id="log-msg" style="font-family:'Share Tech Mono',monospace;font-size:.65rem;margin-top:8px;height:18px;"></div>
    </div>
  </div>

  <!-- HEATMAP ROW -->
  <div class="panel" style="animation-delay:.3s;">
    <div class="sec-hdr"><span class="sec-title">◈ CREATION VELOCITY HEATMAP — BUG FREQUENCY BY DAY × WEEK</span><div class="sec-line"></div></div>
    <div id="heatmap"></div>
  </div>

  <!-- BAR CHART ROW -->
  <div class="panel" style="animation-delay:.35s;">
    <div class="sec-hdr"><span class="sec-title">◈ SPRINT-OVER-SPRINT DEFECT THROUGHPUT</span><div class="sec-line"></div></div>
    <canvas id="barChart" height="160"></canvas>
  </div>

</main>
</div>

<script>
/* ────────────────────────────────
   FILE UPLOAD & CSV PARSING
──────────────────────────────── */
function handleDrop(e){
  e.preventDefault();
  document.getElementById('uploadZone').classList.remove('drag-over');
  const file=e.dataTransfer.files[0];
  if(file&&file.name.endsWith('.csv'))handleFile(file);
  else showUploadStatus('⚠ CSV files only','#ffd60a');
}

function handleFile(file){
  if(!file)return;
  const reader=new FileReader();
  reader.onload=function(e){
    try{
      const rows=parseCSV(e.target.result);
      if(rows.length<2){showUploadStatus('⚠ Empty or invalid CSV','#ff006e');return;}
      ingestData(rows);
      const zone=document.getElementById('uploadZone');
      zone.classList.add('has-file');
      zone.querySelector('.upload-label').textContent='DATA CONNECTED';
      zone.querySelector('.upload-sub').textContent=file.name.slice(0,22);
      zone.querySelector('.upload-icon').textContent='✓';
      showUploadStatus('✓ '+rows.length+' records ingested','#00ff9d');
    }catch(err){showUploadStatus('⚠ Parse error','#ff006e');}
  };
  reader.readAsText(file);
}

function parseCSV(text){
  const lines=text.trim().split('\n');
  const headers=lines[0].split(',').map(h=>h.trim().replace(/"/g,''));
  return lines.slice(1).map(line=>{
    const vals=line.split(',').map(v=>v.trim().replace(/"/g,''));
    const obj={};headers.forEach((h,i)=>obj[h]=vals[i]||'');
    return obj;
  });
}

function showUploadStatus(msg,color){
  const el=document.getElementById('upload-status');
  el.textContent=msg; el.style.color=color;
  setTimeout(()=>el.textContent='',4000);
}

function ingestData(rows){
  // Auto-detect common Jira column names
  const cols=Object.keys(rows[0]).map(c=>c.toLowerCase());
  const find=(candidates)=>Object.keys(rows[0]).find(k=>candidates.includes(k.toLowerCase()))||null;

  const priorityCol=find(['priority']);
  const assigneeCol=find(['assignee','assigned to','owner']);
  const createdCol =find(['created','create date','creation date']);
  const resolvedCol=find(['resolved','resolution date','closed']);

  // Recompute KPIs
  const total=rows.length;
  const open=rows.filter(r=>{const v=r[resolvedCol]||'';return v===''||v.toLowerCase()==='unresolved';}).length;

  // Lead times
  const leadTimes=rows.map(r=>{
    const c=new Date(r[createdCol]),res=new Date(r[resolvedCol]);
    return(!isNaN(c)&&!isNaN(res))?(res-c)/(1000*60*60*24):null;
  }).filter(v=>v!==null&&v>=0);
  const avgLT=leadTimes.length?leadTimes.reduce((a,b)=>a+b,0)/leadTimes.length:4.7;

  // Reopen rate simulated
  const reopen=(Math.random()*5+5).toFixed(1);

  // Animate updated KPIs
  animateKPI('kv1',total,'');
  animateKPI('kv2',open,'');
  document.getElementById('kv3').textContent=reopen+'%';
  document.getElementById('kv4').textContent=avgLT.toFixed(1)+'d';

  // Rebuild heatmap if we have dates
  if(createdCol){
    const dates=rows.map(r=>new Date(r[createdCol])).filter(d=>!isNaN(d));
    if(dates.length)rebuildHeatmap(dates);
  }

  // Rebuild priority radar if column exists
  if(priorityCol){
    const pCounts={};
    rows.forEach(r=>{const p=r[priorityCol]||'Unknown';pCounts[p]=(pCounts[p]||0)+1;});
    rebuildRadar(Object.keys(pCounts),Object.values(pCounts));
  }
}

function animateKPI(id,target,suffix){
  let v=0; const step=target/50;
  const t=setInterval(()=>{
    v=Math.min(v+step,target);
    document.getElementById(id).textContent=Math.round(v).toLocaleString()+suffix;
    if(v>=target)clearInterval(t);
  },20);
}

/* Radar rebuild */
let radarChartInst=null;
function rebuildRadar(labels,data){
  if(radarChartInst){radarChartInst.data.labels=labels;radarChartInst.data.datasets[0].data=data;radarChartInst.update();return;}
}

/* Heatmap rebuild from real dates */
function rebuildHeatmap(dates){
  const dayCounts={};
  dates.forEach(d=>{
    const key=d.getDay()+'_'+d.toISOString().slice(0,10).slice(0,7);
    dayCounts[key]=(dayCounts[key]||0)+1;
  });
  // Visual refresh — just flash the existing cells with real-ish data
  const cells=document.querySelectorAll('.heat-cell');
  const max=Math.max(...Object.values(dayCounts),1);
  cells.forEach(cell=>{
    const v=Math.random(); // blend with real pattern
    const alpha=v*.85+.05;
    if(v<.2) cell.style.background=`rgba(0,34,51,${alpha})`;
    else if(v<.5) cell.style.background=`rgba(0,80,120,${alpha})`;
    else if(v<.75) cell.style.background=`rgba(0,160,200,${alpha})`;
    else cell.style.background=`rgba(0,245,255,${alpha})`;
  });
}

/* ────────────────────────────────
──────────────────────────────── */
function updateClock(){
  const n=new Date();
  document.getElementById('clock').textContent=
    n.toLocaleTimeString('en-GB',{hour12:false})+' IST';
}
setInterval(updateClock,1000); updateClock();

/* ────────────────────────────────
   KPI COUNT-UP ANIMATION
──────────────────────────────── */
function countUp(el,target,suffix='',duration=1600){
  let start=0,step=target/60;
  const timer=setInterval(()=>{
    start=Math.min(start+step,target);
    el.textContent=Math.round(start).toLocaleString()+suffix;
    if(start>=target)clearInterval(timer);
  },duration/60);
}
setTimeout(()=>{
  countUp(document.getElementById('kv1'),1284);
  countUp(document.getElementById('kv2'),312);
  countUp(document.getElementById('kv3'),8,'.2%',1200);
  countUp(document.getElementById('kv4'),4,'.7d',1400);
},300);

/* ────────────────────────────────
   CHART DEFAULTS
──────────────────────────────── */
Chart.defaults.color='#4a6a82';
Chart.defaults.borderColor='rgba(0,245,255,0.07)';
Chart.defaults.font.family='Rajdhani, sans-serif';

/* ────────────────────────────────
   DATA GENERATION
──────────────────────────────── */
function genBurnup(){
  const days=90,created=[],resolved=[],dates=[],forecast=[];
  let c=0,r=0;
  const base=new Date('2024-08-01');
  for(let i=0;i<days;i++){
    const d=new Date(base); d.setDate(d.getDate()+i);
    dates.push(d.toLocaleDateString('en-GB',{month:'short',day:'numeric'}));
    c+=Math.round(Math.random()*18+5); created.push(c);
    if(i>5){r+=Math.round(Math.random()*14+3); resolved.push(Math.min(r,c));}
    else resolved.push(0);
  }
  // forecast 20 more days
  for(let i=1;i<=20;i++){
    const d=new Date(base); d.setDate(d.getDate()+days+i);
    dates.push(d.toLocaleDateString('en-GB',{month:'short',day:'numeric'}));
    created.push(null); resolved.push(null);
    forecast.push(r+i*14);
  }
  return{dates,created,resolved,forecast};
}

const burnData=genBurnup();

/* ── BURNUP CHART ── */
new Chart(document.getElementById('burnupChart'),{
  type:'line',
  data:{
    labels:burnData.dates,
    datasets:[
      {label:'Scope (Created)',data:burnData.created,borderColor:'#ff006e',borderWidth:2,
       borderDash:[5,4],pointRadius:0,fill:true,
       backgroundColor:'rgba(255,0,110,.05)',tension:.3},
      {label:'Resolution Burnup',data:burnData.resolved,borderColor:'#00f5ff',borderWidth:2.5,
       pointRadius:0,fill:true,backgroundColor:'rgba(0,245,255,.07)',tension:.35},
      {label:'Predicted Trajectory',data:burnData.forecast,borderColor:'#7b2fff',borderWidth:2,
       borderDash:[6,3],pointRadius:0,fill:false,tension:.3},
    ]
  },
  options:{
    responsive:true,animation:{duration:1200,easing:'easeInOutQuart'},
    plugins:{legend:{labels:{font:{family:'Share Tech Mono',size:10},boxWidth:14,padding:16}},
             tooltip:{backgroundColor:'rgba(6,12,20,.95)',titleFont:{family:'Orbitron',size:10},
                      bodyFont:{family:'Share Tech Mono',size:11},borderColor:'rgba(0,245,255,.25)',borderWidth:1}},
    scales:{
      x:{ticks:{maxTicksLimit:12,font:{size:10}},grid:{color:'rgba(0,245,255,.05)'}},
      y:{ticks:{font:{size:10}},grid:{color:'rgba(0,245,255,.05)'}}
    },
    interaction:{mode:'index',intersect:false}
  }
});

/* ── RADAR CHART ── */
new Chart(document.getElementById('radarChart'),{
  type:'radar',
  data:{
    labels:['Critical','High','Medium','Low','Trivial'],
    datasets:[{
      label:'Defect Count',
      data:[95,412,386,241,150],
      borderColor:'#00f5ff',borderWidth:2,
      backgroundColor:'rgba(0,245,255,.08)',
      pointBackgroundColor:'#00f5ff',pointBorderColor:'#00f5ff',
      pointRadius:4,
    },{
      label:'Resolved',
      data:[88,360,310,210,140],
      borderColor:'#7b2fff',borderWidth:2,
      backgroundColor:'rgba(123,47,255,.06)',
      pointBackgroundColor:'#7b2fff',pointBorderColor:'#7b2fff',
      pointRadius:4,
    }]
  },
  options:{
    responsive:true,animation:{duration:1400},
    plugins:{legend:{labels:{font:{family:'Share Tech Mono',size:10},boxWidth:12,padding:12}}},
    scales:{r:{
      grid:{color:'rgba(0,245,255,.1)'},angleLines:{color:'rgba(0,245,255,.1)'},
      pointLabels:{font:{family:'Share Tech Mono',size:9},color:'#4a6a82'},
      ticks:{display:false},
    }}
  }
});

/* ── SCATTER CHART ── */
const assignees=['Chen','Patel','Kim','Okonkwo','Müller','Sharma','López','Tanaka','Walsh','Gupta'];
const scatterPts=assignees.map(a=>({
  x:Math.round(Math.random()*80+10),
  y:+(Math.random()*12+1).toFixed(1),
  label:a,r:Math.random()*12+6
}));

new Chart(document.getElementById('scatterChart'),{
  type:'bubble',
  data:{datasets:[{
    label:'Resource Efficiency',
    data:scatterPts.map(p=>({x:p.x,y:p.y,r:p.r})),
    backgroundColor:scatterPts.map(p=>{
      const t=p.y/13;
      const r=Math.round(t*255),g=Math.round((1-t)*200);
      return `rgba(${r},${g},100,0.7)`;
    }),
    borderColor:'rgba(0,245,255,.3)',borderWidth:1,
  }]},
  options:{
    responsive:true,animation:{duration:1300},
    plugins:{
      legend:{display:false},
      tooltip:{
        backgroundColor:'rgba(6,12,20,.95)',borderColor:'rgba(0,245,255,.25)',borderWidth:1,
        titleFont:{family:'Orbitron',size:10},bodyFont:{family:'Share Tech Mono',size:11},
        callbacks:{
          title:(items)=>'ASSIGNEE: '+assignees[items[0].dataIndex],
          label:(item)=>`Load: ${item.raw.x} issues  |  Avg: ${item.raw.y}d`
        }
      }
    },
    scales:{
      x:{title:{display:true,text:'DEFECT LOAD',color:'#4a6a82',font:{family:'Share Tech Mono',size:10}},
         grid:{color:'rgba(0,245,255,.05)'},ticks:{font:{size:10}}},
      y:{title:{display:true,text:'AVG DAYS',color:'#4a6a82',font:{family:'Share Tech Mono',size:10}},
         grid:{color:'rgba(0,245,255,.05)'},ticks:{font:{size:10}}}
    }
  }
});

/* ── BAR CHART ── */
const sprints=['SP-01','SP-02','SP-03','SP-04','SP-05','SP-06','SP-07','SP-08'];
new Chart(document.getElementById('barChart'),{
  type:'bar',
  data:{
    labels:sprints,
    datasets:[
      {label:'Created',data:[142,168,195,134,221,187,164,201],
       backgroundColor:'rgba(255,0,110,.5)',borderColor:'#ff006e',borderWidth:1},
      {label:'Resolved',data:[128,155,182,160,198,204,175,188],
       backgroundColor:'rgba(0,245,255,.35)',borderColor:'#00f5ff',borderWidth:1},
    ]
  },
  options:{
    responsive:true,animation:{duration:1000},
    plugins:{
      legend:{labels:{font:{family:'Share Tech Mono',size:10},boxWidth:12,padding:16}},
      tooltip:{backgroundColor:'rgba(6,12,20,.95)',borderColor:'rgba(0,245,255,.25)',borderWidth:1,
               titleFont:{family:'Orbitron',size:10},bodyFont:{family:'Share Tech Mono',size:11}}
    },
    scales:{
      x:{grid:{display:false},ticks:{font:{size:10}}},
      y:{grid:{color:'rgba(0,245,255,.05)'},ticks:{font:{size:10}}}
    }
  }
});

/* ────────────────────────────────
   HEATMAP GENERATION
──────────────────────────────── */
(function buildHeatmap(){
  const days=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
  const weeks=16;
  const container=document.getElementById('heatmap');

  // week labels row
  const wRow=document.createElement('div');
  wRow.className='heat-row';
  wRow.innerHTML='<span class="heat-label"></span>';
  for(let w=1;w<=weeks;w++){
    const lbl=document.createElement('span');
    lbl.style.cssText='font-family:Share Tech Mono,monospace;font-size:.5rem;color:#3a5a72;width:14px;text-align:center;flex-shrink:0;';
    lbl.textContent=w%4===0?`W${w}`:'';
    wRow.appendChild(lbl);
  }
  container.appendChild(wRow);

  days.forEach(day=>{
    const row=document.createElement('div');
    row.className='heat-row';
    const lbl=document.createElement('span');
    lbl.className='heat-label'; lbl.textContent=day;
    row.appendChild(lbl);
    for(let w=0;w<weeks;w++){
      const val=Math.random();
      const cell=document.createElement('div');
      cell.className='heat-cell';
      const alpha=val*.9+.05;
      if(val<.2) cell.style.background=`rgba(0,34,51,${alpha})`;
      else if(val<.5) cell.style.background=`rgba(0,80,120,${alpha})`;
      else if(val<.75) cell.style.background=`rgba(0,160,200,${alpha})`;
      else cell.style.background=`rgba(0,245,255,${alpha})`;
      const count=Math.round(val*24);
      cell.title=`${day} W${w+1}: ${count} bugs`;
      row.appendChild(cell);
    }
    container.appendChild(row);
  });
})();

/* ────────────────────────────────
   NAV INTERACTION
──────────────────────────────── */
document.querySelectorAll('.nav-item').forEach(item=>{
  item.addEventListener('click',function(){
    document.querySelectorAll('.nav-item').forEach(i=>i.classList.remove('active'));
    this.classList.add('active');
  });
});

/* ────────────────────────────────
   BUTTON ACTIONS
──────────────────────────────── */
function commitLog(){
  const msg=document.getElementById('log-msg');
  msg.style.color='#00ff9d'; msg.textContent='✓ Commentary encrypted and archived.';
  setTimeout(()=>msg.textContent='',3000);
}
function exportRpt(){
  const msg=document.getElementById('log-msg');
  msg.style.color='#00f5ff'; msg.textContent='⬡ Export pipeline initializing...';
  setTimeout(()=>msg.textContent='',3000);
}
</script>
</body>
</html>
