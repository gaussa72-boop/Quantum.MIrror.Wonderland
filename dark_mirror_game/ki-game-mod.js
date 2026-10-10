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
  let engineResult=null,serverBlueprint=null;
  const calls={
   world:["/api/ki-game-mod/world",{theme:prompt,regions:4}],
   quest:["/api/ki-game-mod/quest",{theme:prompt,level:10}],
   npc:["/api/ki-game-mod/npc",{role:"mirror guide",level:10}],
   combat:["/api/ki-game-mod/combat",{theme:prompt,level:10}],
   boss:["/api/ki-game-mod/boss",{level:20}],
   loot:["/api/ki-game-mod/loot",{level:10,rarity:"epic"}],
   dialogue:["/api/ki-game-mod/events",{type:"dialogue",data:{npc:{personality:"mysterious"},message:prompt}}],
   factions:["/api/ki-game-mod/factions/"+encodeURIComponent("Hüter des Prismas"),{delta:5}],
   events:["/api/ki-game-mod/director/event",{theme:prompt,level:10}],
   balance:["/api/ki-game-mod/events",{type:"balance",data:{player:{level:10,deaths:2,kills:5}}}],
   analyze:["/api/ki-game-mod/events",{type:"analyze",data:{player:{level:10,deaths:2,kills:5},quests:[],inventory:[]}}]
  };
  try{
   if(name==="memory"){
    const response=await fetch("/api/ki-game-mod/memory");
    if(response.ok)engineResult=await response.json();
   }else if(calls[name]){
    const [url,body]=calls[name];
    const response=await fetch(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
    if(response.ok)engineResult=await response.json();
    else data.engine_error="HTTP "+response.status;
   }
  }catch(_error){data.engine_error="Game-Mod-Backend nicht erreichbar";}
  try{
   const response=await fetch("/api/generator/blueprint",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({prompt,kind:"mod",target:"web",quality:"1080p_balanced"})});
   if(response.ok)serverBlueprint=await response.json();
  }catch(_error){data.blueprint_status="Blueprint-API nicht erreichbar";}
  data.backend={status:engineResult?"KI-Game-Mod-Engine verbunden":"lokaler Fallback",engine:engineResult,blueprint:serverBlueprint};
  data.status=engineResult?"Backend verbunden":"Lokaler Entwurf";
  drafts.unshift(data);
  if(out){
   const lines=t.fields.map(f=>"• "+f+": "+data.items[f]).join("\n");
   const engineText=engineResult?"\n\nKI-GAME-MOD-ENGINE\n"+JSON.stringify(engineResult,null,2):"\n\nGame-Mod-Backend nicht erreichbar; lokale Vorlage bleibt verfügbar.";
   const blueprintText=serverBlueprint?"\n\nSERVER-BLUEPRINT\n"+JSON.stringify(serverBlueprint.blueprint,null,2):"";
   out.textContent=t.title+"\n"+lines+"\n\n"+data.items["Anpassung an deine Idee"]+engineText+blueprintText;
  }
 };
 window.exportDraft=function(){const data=drafts[0]||{module:"Dark Mirror AI Game Studio",items:{},note:"Bitte zuerst ein Modul auswählen."};const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:"application/json"}));const a=document.createElement("a");a.href=url;a.download="dark-mirror-game-draft.json";a.click();URL.revokeObjectURL(url);};
})();