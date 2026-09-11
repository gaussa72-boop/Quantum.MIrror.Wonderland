const $ = (id) => document.getElementById(id);
const status = $('status');
const prompt = $('prompt');
const payload = () => ({
  prompt: prompt.value.trim(), kind: $('kind').value, target: $('target').value,
  quality: $('quality').value, target_fps: Number($('fps').value),
  ray_tracing: $('rt').checked, hdr: $('hdr').checked,
  upscaling: $('upscale').checked, assets: $('assets').checked, tests: $('tests').checked
});
const setBusy = (busy, text) => { $('plan').disabled = busy; $('generate').disabled = busy; status.textContent = text; };
const esc = (s) => String(s).replace(/[&<>\"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','\\"':'&quot;',"'":'&#39;'}[c]));

$('plan').addEventListener('click', async () => {
  if (prompt.value.trim().length < 3) { prompt.focus(); return; }
  setBusy(true, '● plane …');
  try {
    const r = await fetch('/api/generator/plan', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload())});
    const data = await r.json(); if (!r.ok) throw new Error(data.error || 'Plan konnte nicht erstellt werden.');
    $('empty').hidden = true; $('result').hidden = false; $('planbox').hidden = false;
    $('badge').textContent = `${data.project.kind.toUpperCase()} · ${data.project.target.toUpperCase()}`;
    $('name').textContent = data.design.prompt.split(/\s+/).slice(0,5).join(' ');
    $('description').textContent = 'Generationsplan für Dunkle Spiegel.';
    $('planbox').innerHTML = `<b>Rendering:</b> ${esc(data.visual.resolution)} · ${data.visual.target_fps} FPS Ziel · HDR ${data.visual.hdr?'ON':'OFF'} · RT ${data.visual.ray_tracing?'ON':'OFF'}<br><b>Pipeline:</b> ${esc(data.design.systems.join(' · '))}<br><b>Assets:</b> LOD ${data.asset_pipeline.lod?'ON':'OFF'} · Streaming ${data.asset_pipeline.texture_streaming?'ON':'OFF'} · Build-Isolation ${data.quality.build_isolation_required?'erforderlich':'optional'}`;
    status.textContent = '● plan bereit';
  } catch (e) { status.textContent = '● fehler'; alert(e.message); }
  finally { setBusy(false, status.textContent); }
});

$('generate').addEventListener('click', async () => {
  if (prompt.value.trim().length < 3) { prompt.focus(); return; }
  setBusy(true, '● generiere …');
  try {
    const r = await fetch('/api/generator/generate', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload())});
    const data = await r.json(); if (!r.ok) throw new Error(data.error || 'Generierung fehlgeschlagen.');
    $('empty').hidden = true; $('result').hidden = false; $('planbox').hidden = false;
    $('badge').textContent = `${data.kind.toUpperCase()} · ${data.target.toUpperCase()} · ${data.quality}`;
    $('name').textContent = data.name; $('description').textContent = data.description;
    $('download').href = data.download;
    $('files').innerHTML = data.files.map(x => `<li><code>${esc(x)}</code></li>`).join('');
    $('steps').innerHTML = (data.next_steps || []).map(x => `<li>${esc(x)}</li>`).join('');
    $('tests').innerHTML = (data.test_plan || []).map(x => `<li>${esc(x)}</li>`).join('');
    $('planbox').innerHTML = `<b>Qualität:</b> ${esc(data.quality)} · <b>FPS-Ziel:</b> ${data.target_fps} · <b>Render:</b> ${esc(data.render_profile.resolution ? data.render_profile.resolution.join('×') : 'auto')} · <b>Adaptive Quality:</b> ON`;
    status.textContent = '● fertig';
  } catch (e) { status.textContent = '● fehler'; alert(e.message); }
  finally { $('plan').disabled = false; $('generate').disabled = false; }
});
