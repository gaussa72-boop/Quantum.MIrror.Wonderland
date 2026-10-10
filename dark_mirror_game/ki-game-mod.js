(() => {
 const templates={
 world:{title:"World Generator",fields:["Weltname","Biom","Gefahr","Geheimnis","Regel"],values:["Mirrorfall","Kristallwald und zerbrochene Sternenebenen","Instabile Portale und wandernde Schatten","Ein vergessener Shard steuert die Jahreszeiten","Spiegelentscheidungen verändern Wege und Begegnungen"]},
 quest:{title:"Quest Generator",fields:["Titel","Auftrag","Schritte","Konflikt","Belohnung"],values:["Die fünf Echos","Finde die verlorenen Erinnerungsfragmente","Spur untersuchen → NPC befragen → Portal öffnen","Ein Verbündeter bewacht unwissentlich das letzte Fragment","Zugang zum verborgenen Mirror Gate"]},
 npc:{title:"NPC Generator",fields:["Name","Rolle","Motivation","Geheimnis","Reaktion"],values:["Lyra Vey","Kartografin der Zwischenwelten","Verlorene Gebiete wieder verbinden","Sie erinnert sich an alternative Versionen der Welt","Reagiert auf gesammelte Shards und den Realm-Zustand"]},
 combat:{title:"Combat AI",fields:["Kampfstil","Verhalten","Telegraph","Konter","Skalierung"],values:["Adaptiver Wächter","Wechselt zwischen Distanz- und Nahkampf","Leuchtende Markierung vor starken Angriffen","Ausweichen öffnet ein Zeitfenster","Begrenzt und fair skalierend"]},
 boss:{title:"Boss AI",fields:["Boss","Phase 1","Phase 2","Schwäche","Siegbedingung"],values:["Der Spiegelkönig","Langsame Raumkontrolle und Projektilmuster","Spiegelt Spielerbewegungen mit Verzögerung","Angriffe gegen den Spiegelkern unterbrechen die Phase","Kern in drei Öffnungsfenstern aktivieren"]},
 loot:{title:"Loot Generator",fields:["Item","Seltenheit","Effekt","Fundort","Trade-off"],values:["Prisma der Erinnerung","Episch","Zeigt kurz den nächsten Shard","Versteckte Kammer hinter dem Mirror Gate","Verbraucht Energie bei jedem Hinweis"]},
 dialogue:{title:"Dialogue Engine",fields:["Stimme","Einstieg","Wahl A","Wahl B","Konsequenz"],values:["Ruhig, rätselhaft, empathisch","Du trägst eine Erinnerung, die nicht deine ist.","Nach dem Weg fragen","Das Geheimnis des Spiegels offenlegen","Antwort ändert Vertrauen und Questpfad"]},
 factions:{title:"Factions & Reputation",fields:["Fraktion","Ziel","Ruf +","Ruf −","Folge"],values:["Die Hüter des Prismas","Shards vor dem Zerfall schützen","Heile ein Portal","Stiehl ein Erinnerungsartefakt","Neue Händler, Dialoge und Gebietszugänge"]},
 events:{title:"Dynamic Event Director",fields:["Ereignis","Auslöser","Ablauf","Spielerwirkung","Sicherheitsregel"],values:["Sternenregen","Lange Erkundungsphase ohne Fortschritt","Vorwarnung → Shard-Sturm → Ruhephase","Neue Ressourcen erscheinen, Wege verändern sich kurz","Keine unlösbaren Blockaden; Event ist wiederholbar"]},
 memory:{title:"Game Memory",fields:["Speicherpunkt","Beobachtung","Präferenz","Folge","Datenschutz"],values:["Session Memory","Gesammelte Shards, besuchte Gebiete und Queststatus","Aus Erkundungsverhalten lokal abgeleitet","Hinweise passen sich dem Spielstand an","Nur im Browser; keine Übertragung an einen Server"]},
 balance:{title:"Adaptive Balance",fields:["Signal","Anpassung","Grenze","Fairness","Ziel"],values:["Häufige Fehlversuche","Hinweise klarer machen und Checkpoints anbieten","Änderungen bleiben begrenzt","Keine versteckte Bestrafung","Herausforderung erhalten, Frust reduzieren"]},
 analyze:{title:"Game Analyzer",fields:["Stärken","Risiko","Verbesserung","Test","Ergebnis"],values:["Klare Sammel- und Gate-Ziele","Lange Wege und unklare Quest-Hinweise","Lesbare Marker, Checkpoints und Quest-Log","Mobil/Desktop-Steuerung und Realm-Wechsel testen","Testfälle vor Veröffentlichung abhaken"]}
 };
 const drafts=[];const out=document.getElementById("output");
 window.runModule=async function(name){
  const t=templates[name]||templates.world;
  const prompt=(document.getElementById("studioPrompt")?.value.trim())||(document.getElementById("worldPrompt")?.value.trim())||"Dark Mirror Wonderland";
  const data={module:t.title,prompt,createdAt:new Date().toISOString(),status:"Entwurf",items:{}};
  t.fields.forEach((f,i)=>data.items[f]=t.values[i]);
  data.items["Anpassung an deine Idee"]="Kontext: "+prompt+". Vor dem Einsatz im Spiel prüfen und anpassen.";
  let serverBlueprint=null;
  try{
   const response=await fetch("/api/generator/blueprint",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({prompt,kind:"mod",target:"web",quality:"1080p_balanced"})});
   if(response.ok){serverBlueprint=await response.json();data.status="Backend verbunden";data.backend={pipeline_version:serverBlueprint.pipeline_version,stages:serverBlueprint.stages,blueprint:serverBlueprint.blueprint};}
   else{data.status="Lokaler Entwurf – Backend meldet HTTP "+response.status;}
  }catch(_error){data.status="Lokaler Entwurf – Backend nicht erreichbar";}
  drafts.unshift(data);
  if(out){
   const lines=t.fields.map(f=>"• "+f+": "+data.items[f]).join("\\n");
   const backendText=serverBlueprint?"\\n\\nSERVER-BLUEPRINT\\n"+JSON.stringify(serverBlueprint.blueprint,null,2):"\\n\\nBackend nicht verbunden; lokale Vorlage bleibt verfügbar.";
   out.textContent=t.title+"\\n"+lines+"\\n\\n"+data.items["Anpassung an deine Idee"]+backendText;
  }
 }; 
 window.exportDraft=function(){const data=drafts[0]||{module:"Dark Mirror AI Game Studio",items:{},note:"Bitte zuerst ein Modul auswählen."};const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:"application/json"}));const a=document.createElement("a");a.href=url;a.download="dark-mirror-game-draft.json";a.click();URL.revokeObjectURL(url);};
})();