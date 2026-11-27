/* Aurealis Vision Layer v1 — optional, progressive-enhancement holographic UI.
 * No camera/sensor permissions, no external dependencies, no page takeover.
 * Hologram effects are a screen simulation, not a physical holographic display.
 */
(() => {
  "use strict";
  if (window.__AUREALIS_VISION__) return;
  window.__AUREALIS_VISION__ = true;
  const reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const mobile = window.matchMedia && window.matchMedia("(max-width: 700px)").matches;
  const style = document.createElement("style");
  style.id = "aurealis-vision-style";
  style.textContent = `
    :root{--av-cyan:#79eaff;--av-violet:#a78bfa;--av-gold:#e8cf8d}
    body.av-holo{isolation:isolate}
    body.av-holo:after{content:"";position:fixed;inset:0;z-index:2147483000;pointer-events:none;
      background:linear-gradient(115deg,transparent 0%,rgba(121,234,255,.025) 46%,rgba(167,139,250,.045) 52%,transparent 100%),
      repeating-linear-gradient(0deg,rgba(121,234,255,.018) 0 1px,transparent 1px 5px);
      mix-blend-mode:screen}
    body.av-holo .av-depth{transform:perspective(1200px) translateZ(0);transition:transform .25s ease,filter .25s ease}
    body.av-holo .av-depth:hover{filter:drop-shadow(0 0 12px rgba(121,234,255,.13))}
    #av-launch{position:fixed;right:18px;bottom:18px;z-index:2147483001;border:1px solid rgba(121,234,255,.65);
      border-radius:999px;padding:11px 15px;background:rgba(8,15,30,.88);backdrop-filter:blur(18px);
      color:#e9faff;font:700 12px/1.2 system-ui;letter-spacing:.12em;box-shadow:0 0 24px rgba(80,190,255,.18);cursor:pointer}
    #av-panel{position:fixed;right:18px;bottom:68px;z-index:2147483001;width:min(290px,calc(100vw - 36px));
      padding:16px;border:1px solid rgba(121,234,255,.42);border-radius:16px;background:rgba(7,13,27,.94);
      color:#eaf4ff;font:13px/1.5 system-ui;backdrop-filter:blur(24px);box-shadow:0 12px 50px #0009}
    #av-panel[hidden]{display:none}#av-panel button{border:1px solid #52748c;border-radius:10px;padding:9px 11px;background:#10243a;color:#eaf4ff;cursor:pointer}
    #av-panel .av-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
    #av-panel p{margin:7px 0;color:#b9cadc}#av-panel strong{color:var(--av-cyan)}
    #av-canvas{position:fixed;inset:0;width:100%;height:100%;z-index:2147482999;pointer-events:none;opacity:.42}
    @media(prefers-reduced-motion:reduce){body.av-holo .av-depth{transition:none}#av-canvas{display:none}}
  `;
  document.head.appendChild(style);
  const canvas = document.createElement("canvas"); canvas.id = "av-canvas"; canvas.setAttribute("aria-hidden","true");
  const ctx = canvas.getContext("2d",{alpha:true});
  if (ctx && !reduced) document.body.appendChild(canvas);
  const launch = document.createElement("button"); launch.id="av-launch"; launch.type="button";
  launch.textContent="AUREALIS ◈"; launch.setAttribute("aria-expanded","false"); launch.setAttribute("aria-controls","av-panel");
  const panel = document.createElement("section"); panel.id="av-panel"; panel.hidden=true; panel.setAttribute("aria-label","Aurealis Vision Einstellungen");
  panel.innerHTML='<strong>AUREALIS VISION</strong><p>Immersive Tiefenebene für kompatible Bildschirme. Keine Kamera- oder Sensorfreigabe erforderlich.</p><div class="av-row"><button type="button" data-mode="holo">Hologramm-Look</button><button type="button" data-mode="ambient">Kosmischer Raum</button><button type="button" data-mode="off">Aus</button></div><p id="av-status" aria-live="polite">Modus: Standard</p>';
  document.body.append(launch,panel);
  const status=panel.querySelector("#av-status");
  let mode="off",w=0,h=0,dpr=1,particles=[];
  function resize(){if(!ctx)return;dpr=Math.min(window.devicePixelRatio||1,2);w=innerWidth;h=innerHeight;canvas.width=Math.floor(w*dpr);canvas.height=Math.floor(h*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);particles=Array.from({length:mobile?18:38},()=>({x:Math.random()*w,y:Math.random()*h,r:.5+Math.random()*1.6,v:.08+Math.random()*.24,a:.15+Math.random()*.55}));}
  function draw(){if(!ctx||mode==="off"||document.hidden)return;ctx.clearRect(0,0,w,h);for(const p of particles){p.y-=p.v;if(p.y<0){p.y=h;p.x=Math.random()*w;}ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fillStyle='rgba(121,234,255,'+p.a+')';ctx.fill();}if(!reduced)requestAnimationFrame(draw);}
  function setMode(next){mode=next;document.body.classList.toggle("av-holo",mode==="holo");canvas.style.opacity=mode==="ambient"?".65":".3";status.textContent="Modus: "+(mode==="holo"?"Hologramm-Simulation":mode==="ambient"?"Kosmischer Raum":"Standard");if(mode!=="off"&&!reduced)draw();}
  launch.addEventListener("click",()=>{panel.hidden=!panel.hidden;launch.setAttribute("aria-expanded",String(!panel.hidden));});
  panel.addEventListener("click",e=>{const b=e.target.closest("[data-mode]");if(b)setMode(b.dataset.mode);});
  document.addEventListener("keydown",e=>{if(e.key==="Escape"&&!panel.hidden){panel.hidden=true;launch.setAttribute("aria-expanded","false");}});
  if(ctx){resize();addEventListener("resize",resize,{passive:true});}
  if(reduced){panel.querySelector('[data-mode="ambient"]').disabled=true;status.textContent="Reduzierte Bewegung aktiv — Animationen deaktiviert.";}
  document.documentElement.dataset.aurealisVision="1";
})();
