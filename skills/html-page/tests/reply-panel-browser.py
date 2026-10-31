#!/usr/bin/env python3
"""Exercise the real reader/reply service in Aside, without terminal input.

Run directly with Python 3 and the Aside CLI. The harness uses a synthetic
Codex identity and Store.receive, not a live model or a claimed native callback.
All browser tabs and the isolated loopback service are closed on completion.
"""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time

BRIDGE_PATH = Path(__file__).resolve().parents[1] / "scripts/reply-bridge.py"
SPEC = importlib.util.spec_from_file_location("reply_bridge", BRIDGE_PATH)
bridge = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bridge)

FIXTURE = """<!doctype html><html lang="ko"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="darkreader-lock"><style>:root{color-scheme:light dark}body{margin:0;font:15px/1.8 system-ui}article{max-width:860px;margin:35px auto;padding:0 28px}h1{font-size:28px}section{padding:18px 0}textarea{display:block;width:100%;height:60px}label{display:inline-block;padding:10px}</style>
<article><h1>리더와 하단 회신 검증</h1><p>선택한 내용과 메모는 같은 자료의 원래 대화로 돌아갑니다.</p>
<section data-item="R1"><h2>R1. 보관 기간</h2><label><input type="radio" name="retention" value="30일">30일 보관</label><label><input type="radio" name="retention" value="90일">90일 보관</label><textarea aria-label="보관 기간 메모"></textarea></section>
__PARAGRAPHS__
<section data-item="R2"><h2>R2. 마지막 검토 항목</h2><label><input type="checkbox" value="원래 대화 확인">원래 대화 확인</label></section></article>
<script>
addEventListener('message', event => {
  if(event.source !== parent) return;
  if(event.data?.type === 'reader-qa-heading') {
    if(event.data.action==='add'){const h=document.createElement('h3');h.id='dynamic-heading';h.textContent='추가 제목 <태그>';document.querySelector('article').append(h);}
    if(event.data.action==='hide')document.getElementById('dynamic-heading').hidden=true;
    if(event.data.action==='clear')document.querySelectorAll('h1,h2,h3').forEach(h=>h.remove());
    return;
  }
  if(event.data?.type !== 'reader-qa-measure') return;
  const last = document.querySelector('[data-item="R2"] input').getBoundingClientRect();
  const root = document.getElementById('nested-scroll') || document.scrollingElement;
  parent.postMessage({type:'reader-qa-measurement',height:innerHeight,scroll:root.scrollTop,lastBottom:last.bottom,space:document.querySelector('.html-reply-end-space')?.offsetHeight||0,focused:document.activeElement.textContent},'*');
});
</script></html>""".replace("__PARAGRAPHS__", "".join(f"<p>원문 {i}. 마지막 항목도 입력창에 가리지 않고 조작할 수 있어야 합니다.</p>" for i in range(14)))

QUESTION_FIXTURE = '''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:30px;font:16px/1.8 system-ui}fieldset{margin:24px 0;padding:16px}label{display:block;padding:8px}textarea{display:block;width:90%;height:70px}input,select,textarea{accent-color:#666}</style>
<h1>실제 검토 질문</h1><section data-item="GROUP"><h2>검토 결정</h2>
<fieldset data-item="C1"><legend>C1. 연결 방식</legend><label><input id="c1-origin" type="radio" name="C1" value="원래 대화">원래 대화</label><label><input id="c1-later" type="radio" name="C1" value="아직 결정하지 않음">아직 결정하지 않음</label><label for="c1-note">연결 의견</label><textarea id="c1-note"></textarea></fieldset>
<fieldset data-item="C2"><legend>C2. 확인할 기능</legend><label><input id="c2-draft" name="C2" type="checkbox" value="초안 보존">초안 보존</label><label><input id="c2-mobile" name="C2" type="checkbox" value="모바일">모바일</label><label><input id="c2-none" name="C2" data-reply-exclusive type="checkbox" value="없음">없음</label></fieldset>
<fieldset data-item="C3"><legend>C3. 직접 의견</legend><label for="c3-answer">직접 의견</label><textarea id="c3-answer" data-reply-answer></textarea></fieldset>
<details id="closed-question" data-item="C4"><summary>접힌 질문</summary><fieldset><legend>C4. 복수 선택</legend><label for="c4-multiple">검증 환경</label><select id="c4-multiple" multiple><option value="Codex">Codex</option><option value="GJC">GJC</option><option value="Claude">Claude</option></select></fieldset></details>
<button id="toggle-conditional" type="button" onclick="document.getElementById('conditional').hidden=!document.getElementById('conditional').hidden">조건 질문 토글</button>
<fieldset id="conditional" data-item="C5" hidden><legend>C5. 조건 질문</legend><label><input id="c5-check" type="checkbox" value="조건 확인">조건 확인</label></fieldset></section>
<button id="disable-written" type="button" onclick="document.getElementById('c3-answer').disabled=!document.getElementById('c3-answer').disabled">글 답변 활성 토글</button>
<button id="style-written" type="button" onclick="let s=document.querySelector('[data-item=C3]');s.style.display=s.style.display==='none'?'':'none'">글 질문 표시 토글</button>
<button id="readonly-written" type="button" onclick="for(const id of ['c3-answer','c1-note'])document.getElementById(id).readOnly=!document.getElementById(id).readOnly">읽기 전용 토글</button>
<button id="mount-options" type="button" onclick="document.getElementById('c4-multiple').innerHTML='<option value=Codex>Codex</option><option value=GJC>GJC</option><option value=Claude>Claude</option>'">선택지 로드</button>
<script>if(location.search.includes('late-options'))document.getElementById('c4-multiple').replaceChildren();</script>
<script>addEventListener('message',event=>{if(event.source!==parent||event.data?.type!=='question-qa-measure')return;parent.postMessage({type:'question-qa-result',focus:document.activeElement.id,caret:document.activeElement.selectionStart,scroll:document.scrollingElement.scrollTop,details:document.getElementById('closed-question').open,selected:[...document.getElementById('c4-multiple').selectedOptions].map(o=>o.value),conditional:document.getElementById('c5-check').checked},'*');});</script></html>'''


def main():
    root = Path(tempfile.mkdtemp(prefix="reply-reader-browser-"))
    source = root / "fixture.html"
    source.write_text(FIXTURE)
    store = bridge.Store(root / "state")
    source.write_text(source.read_text().replace('<meta name="darkreader-lock">', '<meta name="html-reply-context" content="목적: 회신 연결 검증&#10;이전 결정: 원래 대화 유지&#10;이번 변경: 맥락과 이동">\n<meta name="darkreader-lock">', 1))
    artifact = store.register(source, "B 리더 실제 회신 검증", "codex", "reader-browser-origin", "isolated-browser-test", "격리된 원래 대화 검증")
    nested_source = root / "nested.html"
    nested_source.write_text(FIXTURE.replace('<article>', '<style>html,body{height:100%;overflow:hidden}#nested-scroll{height:100%;overflow:auto}</style><div id="nested-scroll"><article>', 1).replace('</article>', '</article></div>', 1))
    nested_artifact = store.register(nested_source, "중첩 스크롤 검증", "codex", "reader-browser-origin", "isolated-browser-test", "격리된 원래 대화 검증")
    question_source = root / "questions.html"
    question_source.write_text(QUESTION_FIXTURE)
    question_artifact = store.register(question_source, "실제 질문 탐색 검증", "codex", "reader-browser-origin", "isolated-browser-test")
    late_source = root / "late-questions.html"
    late_source.write_text(QUESTION_FIXTURE.replace("if(location.search.includes('late-options'))", "if(true)"))
    late_artifact = store.register(late_source, "지연 선택지 복원 검증", "codex", "reader-browser-origin", "isolated-browser-test")
    starters = [store.register(BRIDGE_PATH.parents[1] / "assets" / name, name, "codex", "reader-browser-origin", "isolated-browser-test") for name in ["template.html", "interactive-template.html"]]
    log = (root / "service.log").open("w")
    process = subprocess.Popen([sys.executable, str(BRIDGE_PATH), "--state-dir", str(store.root), "serve", "--preview"], stdout=log, stderr=log)
    try:
        for _ in range(60):
            info = bridge.running(store)
            if info and info["pid"] == process.pid:
                break
            if process.poll() is not None:
                raise RuntimeError("Reply service exited: " + (root / "service.log").read_text())
            time.sleep(0.05)
        else:
            raise RuntimeError("Reply service did not start")
        url = f'http://127.0.0.1:{info["port"]}/artifact/{artifact["id"]}'
        nested_url = f'http://127.0.0.1:{info["port"]}/artifact/{nested_artifact["id"]}'
        question_url = f'http://127.0.0.1:{info["port"]}/artifact/{question_artifact["id"]}'
        late_url = f'http://127.0.0.1:{info["port"]}/artifact/{late_artifact["id"]}'
        starter_urls = [f'http://127.0.0.1:{info["port"]}/artifact/{entry["id"]}/content' for entry in starters]
        received = []

        def receive_when_requested():
            # Only consume the second submission, after the browser cancels its
            # first frozen packet and writes the second memo to its real queue.
            deadline = time.monotonic() + 80
            while time.monotonic() < deadline:
                with store.connect() as db:
                    row = db.execute("SELECT payload FROM replies WHERE artifact=? AND state='held' ORDER BY created DESC LIMIT 1", (artifact["id"],)).fetchone()
                if row and json.loads(row["payload"])["text"] == "새 초안 두 번째":
                    received.append(store.receive(artifact["id"], "reader-browser-origin", 5))
                    return
                time.sleep(0.05)

        receiver = threading.Thread(target=receive_when_requested, daemon=True)
        receiver.start()
        code = r'''
var pg=await openTab(URL);
await pg._sendToTarget('Runtime.enable',{});
await pg._sendToTarget('Runtime.evaluate',{expression:"globalThis.replyReaderErrors=[];addEventListener('error',e=>replyReaderErrors.push(e.message));addEventListener('unhandledrejection',e=>replyReaderErrors.push(String(e.reason)))"});
try {
  var snap=await snapshot(pg,{interactive:true});console.log(snap.tree);
  function ref(tree,kind,label){var pattern=new RegExp(kind+' "'+label+'" \\[ref=([^\\]]+)\\]');var m=tree.match(pattern);if(!m)throw Error('Missing '+kind+' '+label);return m[1];}
  function assert(value,message){if(!value)throw Error(message);}
  async function grayscale(allowSemanticColors=false){return await pg.evaluate(allowSemanticColors=>{
    const chromatic=[];
    for(const e of document.querySelectorAll('body,body *')){
      const style=getComputedStyle(e);if(!e.getClientRects().length||style.visibility==='hidden')continue;
      if(allowSemanticColors&&(e.closest('#send,#session-open,#session-jump')||e.matches('.question-state,.heading-state[data-question-state="answered"],.heading-state[data-question-state="unanswered"],.answer-row .item-id,#review-complete,#review-pending,#outline-count,#next-question,#question-empty')))continue;
      for(const property of ['color','backgroundColor','borderTopColor','outlineColor','fill','stroke']){
        const value=style[property],match=value?.match(/^rgba?\(([\d.]+)[, ]+([\d.]+)[, ]+([\d.]+)(?:[, /]+([\d.]+))?\)$/);
        if(match&&Number(match[4]??1)>0&&Math.max(...match.slice(1,4).map(Number))-Math.min(...match.slice(1,4).map(Number))>1)chromatic.push({tag:e.tagName,id:e.id,property,value});
      }
    }
    return chromatic.slice(0,12);
  },allowSemanticColors);}
  var paletteThemes=[];
  for(var theme of ['light','dark']){
    await pg._sendToTarget('Emulation.setEmulatedMedia',{features:[{name:'prefers-color-scheme',value:theme}]});
    var colored=await grayscale(true);assert(colored.length===0,'Non-status reply UI is not achromatic '+JSON.stringify(colored));paletteThemes.push(theme);
  }
  var initial=await pg.evaluate(()=>({hidden:document.getElementById('selection-summary').hidden,disabled:document.getElementById('send').disabled,ratio:document.getElementById('document').clientWidth/innerWidth}));
  assert(initial.hidden&&initial.disabled&&initial.ratio>0.98,'Not a full-width empty reader');
  await pg.locator('#context-open').click();
  assert(await pg.evaluate(()=>document.getElementById('context-view').open&&document.getElementById('context-summary').textContent.includes('이전 결정: 원래 대화 유지')&&document.getElementById('context-conversation').textContent==='격리된 원래 대화 검증'),'Source context missing or inferred');
  var contextGeometries=[];
  for(var size of [[320,568],[390,500],[1440,900]]){
    await pg._sendToTarget('Emulation.setDeviceMetricsOverride',{width:size[0],height:size[1],deviceScaleFactor:1,mobile:false});
    var g=await pg.evaluate(()=>{var r=document.getElementById('context-view').getBoundingClientRect(),h=document.querySelector('header').getBoundingClientRect();return{width:innerWidth,height:innerHeight,left:r.left,right:r.right,top:r.top,bottom:r.bottom,overflow:document.documentElement.scrollWidth-innerWidth,headerHeight:h.height};});
    assert(g.left>=0&&g.right<=g.width&&g.top>=0&&g.bottom<=g.height&&g.overflow<=1&&g.headerHeight<100,'Context view overflows or steals reader height '+JSON.stringify(g));contextGeometries.push(g);
  }
  await pg._sendToTarget('Emulation.clearDeviceMetricsOverride',{});
  await pg.locator('#session-open').click();await sleep(80);
  assert(await pg.evaluate(()=>document.getElementById('session-status').textContent.includes('미리보기')&&!document.getElementById('session-open').disabled&&!document.getElementById('session-jump').disabled),'Preview focus is not explicitly blocked');
  var focusDenied=await pg.evaluate(async()=>{var meta=JSON.parse(document.getElementById('reply-meta').textContent),base='/artifact/'+meta.id;var noCSRF=await fetch(base+'/focus',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}),get=await fetch(base+'/focus');return{csrf:noCSRF.status,get:get.status};});
  assert(focusDenied.csrf===403&&focusDenied.get===404,'Focus endpoint allows unsafe GET or missing CSRF');
  await pg._sendToTarget('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});
  await pg._sendToTarget('Input.dispatchKeyEvent',{type:'keyUp',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});
  assert(await pg.evaluate(()=>!document.getElementById('context-view').open&&document.activeElement.id==='context-open'),'Context Escape/focus restoration failed');
  assert(await pg.evaluate(()=>!document.getElementById('outline').hidden&&document.querySelectorAll('#outline-list button').length===3),'Document outline missing');
  var rail=await pg.evaluate(()=>{var r=document.getElementById('outline-toggle').getBoundingClientRect();return{x:r.x+r.width/2,y:r.y+r.height/2};});
  await pg._sendToTarget('Input.dispatchMouseEvent',{type:'mouseMoved',x:rail.x,y:rail.y});await sleep(120);
  assert(await pg.evaluate(()=>!document.getElementById('outline-panel').hidden),'Hover did not reveal outline');
  await pg._sendToTarget('Input.dispatchMouseEvent',{type:'mouseMoved',x:10,y:100});await sleep(100);
  assert(await pg.evaluate(()=>document.getElementById('outline-panel').hidden),'Hover outline did not close on leave');
  await pg.locator(ref(snap.tree,'radio','90일 보관')).click();
  snap=await snapshot(pg,{interactive:true});
  await pg.locator(ref(snap.tree,'textbox','보관 기간 메모')).fill('항목 이유 & <한글>');
  await pg.locator('#message').fill('첫 응답 & <태그>');await sleep(250);
  await pg.locator('#summary-toggle').click();
  assert(await pg.evaluate(()=>document.getElementById('answers').textContent.includes('90일')&&document.getElementById('answers').textContent.includes('항목 이유 & <한글>')),'Structured answer not in summary');
  await pg.locator('#toggle').click();
  assert(await pg.evaluate(()=>document.getElementById('reply-dock').hidden&&parseFloat(getComputedStyle(document.getElementById('reader')).paddingBottom)===0),'Reader not reclaimed when dock collapsed');
  await pg.locator('#toggle').click();
  var stableUrl=pg.url();await pg.goto(stableUrl+'?restore=1',{waitUntil:'load'});snap=await snapshot(pg,{interactive:true});
  await pg.evaluate(()=>{globalThis.replyReaderErrors=[];addEventListener('error',e=>replyReaderErrors.push(e.message));addEventListener('unhandledrejection',e=>replyReaderErrors.push(String(e.reason)));});
  var restored=await pg.evaluate(()=>({memo:document.getElementById('message').value,summary:!document.getElementById('selection-summary').hidden,selected:document.getElementById('answers').textContent}));
  assert(restored.memo==='첫 응답 & <태그>'&&restored.summary&&restored.selected.includes('90일'),'Reload lost draft/summary');
  await pg.locator('#context-open').click();await pg.locator('#context-close').click();
  assert(await pg.evaluate(()=>document.getElementById('message').value==='첫 응답 & <태그>'&&document.getElementById('answers').textContent.includes('90일')),'Context view changed saved response');
  await pg.locator('#summary-toggle').click();
  snap=await snapshot(pg,{interactive:true});await pg.locator(ref(snap.tree,'checkbox','원래 대화 확인')).click();
  var geometries=[];
  for(var size of [[390,844],[768,900],[1440,900],[390,500],[844,390],[320,568]]){
    await pg._sendToTarget('Emulation.setDeviceMetricsOverride',{width:size[0],height:size[1],deviceScaleFactor:1,mobile:false});await sleep(100);
    await pg.locator('#outline-toggle').click();
    var outlineBounds=await pg.evaluate(()=>{var r=document.getElementById('outline-panel').getBoundingClientRect();return{left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:innerWidth,height:innerHeight};});
    assert(outlineBounds.left>=0&&outlineBounds.right<=outlineBounds.width&&outlineBounds.top>=0&&outlineBounds.bottom<=outlineBounds.height,'Outline is outside viewport '+JSON.stringify(outlineBounds));
    await pg._sendToTarget('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});
    await pg._sendToTarget('Input.dispatchKeyEvent',{type:'keyUp',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});
    for(var expanded of [false,true]){
      if(await pg.evaluate(()=>document.getElementById('summary-toggle').getAttribute('aria-expanded'))!==String(expanded))await pg.locator('#summary-toggle').click();
      await sleep(80);
      await pg.evaluate(()=>document.getElementById('send').scrollIntoView({block:'nearest'}));
      var g=await pg.evaluate(()=>{var f=document.getElementById('document').getBoundingClientRect(),d=document.getElementById('reply-dock').getBoundingClientRect(),s=document.getElementById('send').getBoundingClientRect(),r=document.getElementById('reader').getBoundingClientRect();return{width:innerWidth,overflow:document.documentElement.scrollWidth-innerWidth,frameBottom:f.bottom,dockTop:d.top,frameHeight:f.height,readerHeight:r.height,sendBottom:s.bottom,windowHeight:innerHeight,summary:document.getElementById('summary-toggle').getAttribute('aria-expanded')};});
      if(g.overflow>1)g.offenders=await pg.evaluate(()=>Array.from(document.querySelectorAll('body *')).filter(e=>e.getBoundingClientRect().right>innerWidth+1).map(e=>({id:e.id,tag:e.tagName,right:e.getBoundingClientRect().right})));
      assert(g.overflow<=1&&g.frameBottom>g.dockTop&&Math.abs(g.frameHeight-g.readerHeight)<=1&&g.sendBottom<g.windowHeight,'Reader is truncated behind floating composer '+JSON.stringify(g));geometries.push(g);
    }
  }
  await pg._sendToTarget('Emulation.clearDeviceMetricsOverride',{});
  if(await pg.evaluate(()=>document.getElementById('summary-toggle').getAttribute('aria-expanded'))==='true')await pg.locator('#summary-toggle').click();
  var passthrough=await pg.evaluate(()=>{var d=document.getElementById('reply-dock').getBoundingClientRect(),t=document.querySelector('.dock-top').getBoundingClientRect();return{side:document.elementFromPoint(20,d.top+80)?.id,gap:document.elementFromPoint(d.left+d.width/2,t.top+t.height/2)?.id,background:getComputedStyle(document.getElementById('reply-dock')).backgroundColor};});
  assert(passthrough.side==='document'&&passthrough.gap==='document'&&passthrough.background==='rgba(0, 0, 0, 0)','Invisible dock backing blocks source '+JSON.stringify(passthrough));
  await pg.locator('#outline-toggle').click();await pg.locator('#outline-list button[data-heading="2"]').click();await sleep(700);
  assert(await pg.evaluate(()=>document.querySelector('#outline-list [aria-current="location"]')?.firstElementChild.textContent)==='R2. 마지막 검토 항목','Outline navigation/active section incorrect');
  var sourceState=await pg.evaluate(()=>new Promise(resolve=>{function receive(event){if(event.source!==document.getElementById('document').contentWindow||event.data?.type!=='reader-qa-measurement')return;removeEventListener('message',receive);resolve(event.data);}addEventListener('message',receive);document.getElementById('document').contentWindow.postMessage({type:'reader-qa-measure'},'*');}));
  var sourceClearance=await pg.evaluate(()=>({top:document.getElementById('document').getBoundingClientRect().top,dock:document.getElementById('reply-dock').getBoundingClientRect().top}));
  assert(sourceState.scroll>0&&sourceState.space>200&&sourceState.lastBottom+sourceClearance.top<sourceClearance.dock,'End controls cannot scroll above composer '+JSON.stringify(sourceState));
  assert(sourceState.focused==='R2. 마지막 검토 항목','Outline did not move reading focus');
  await pg.locator('#outline-toggle').click();
  await pg._sendToTarget('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});
  await pg._sendToTarget('Input.dispatchKeyEvent',{type:'keyUp',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});
  assert(await pg.evaluate(()=>document.getElementById('outline-panel').hidden),'Escape did not close keyboard outline');
  await pg.locator('#message').click();
  var collapsedScreen=pwd+'/reader-dock-collapsed.png';await fs.writeFile(collapsedScreen,await pg.screenshot());
  var ime=await pg.evaluate(()=>{var e=document.getElementById('message');e.dispatchEvent(new CompositionEvent('compositionstart',{bubbles:true}));e.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',ctrlKey:true,isComposing:true,bubbles:true}));e.dispatchEvent(new CompositionEvent('compositionend',{bubbles:true}));return document.getElementById('status').dataset.state;});
  assert(ime==='draft','Composition submitted feedback');
  var draftColor=await pg.evaluate(()=>getComputedStyle(document.getElementById('status')).backgroundColor);
  await pg.locator('#send').click();await sleep(200);
  assert(await pg.evaluate(()=>document.getElementById('status').dataset.state)==='held','Real preview service did not store response');
  var heldColor=await pg.evaluate(()=>getComputedStyle(document.getElementById('status')).backgroundColor);
  assert(heldColor!==draftColor,'Stored/held state lacks distinct color');
  assert((await grayscale(true)).length===0,'Held state changes non-question palette');
  await pg.locator('#message').fill('새 초안 두 번째');await sleep(250);
  var frozen=await pg.evaluate(()=>document.getElementById('payload-text').value);
  assert(frozen.includes('첫 응답 &amp; &lt;태그&gt;')&&!frozen.includes('새 초안 두 번째'),'Pending response mutated');
  async function offlineCopy(clipboardAvailable){return await pg.evaluate(async clipboardAvailable=>{
    const meta=JSON.parse(document.getElementById('reply-meta').textContent),key='html-reply:'+meta.id;
    const readDraft=()=>JSON.parse(localStorage.getItem(key));
    const saved=readDraft(),packet=structuredClone(saved.pendingPacket||{id:saved.draftId,text:saved.text,quote:saved.quote,items:saved.items,sheet:saved.items.length?'':saved.sheet,location:saved.location});
    const originalFetch=globalThis.fetch,clipboard=Object.getOwnPropertyDescriptor(navigator,'clipboard'),execCommand=document.execCommand;
    let copied=null;
    globalThis.fetch=async()=>{throw new TypeError('Offline copy regression');};
    Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async text=>{if(!clipboardAvailable)throw Error('Clipboard unavailable');copied=text;}}});
    document.execCommand=()=>false;
    try {
      await document.getElementById('copy').onclick();
      return{meta:{id:meta.id,title:meta.title,agent:meta.agent,conversation:meta.conversation,conversation_label:meta.conversation_label,revision:meta.revision},packet,text:copied??document.getElementById('payload-text').value,memo:document.getElementById('message').value,preserved:JSON.stringify(readDraft())===JSON.stringify(saved),fallback:!document.getElementById('selection-summary').hidden&&document.getElementById('payload-preview').open,status:document.getElementById('draft-status').textContent};
    } finally {
      globalThis.fetch=originalFetch;document.execCommand=execCommand;
      if(clipboard)Object.defineProperty(navigator,'clipboard',clipboard);else delete navigator.clipboard;
    }
  },clipboardAvailable);}
  function assertOfflineContext(result){
    assert(result.preserved,'Offline copy changed saved editor or frozen payload');
    for(const value of [result.meta.title,result.meta.agent,result.meta.conversation,result.meta.conversation_label,result.meta.id,result.meta.revision.slice(0,12),result.packet.id,result.packet.text,result.packet.quote,result.packet.location])if(value)assert(result.text.includes(value),'Offline copy lost context '+value);
    for(const item of result.packet.items){
      for(const value of [item.id,item.label,item.memo,...item.values])if(value)assert(result.text.includes(value),'Offline copy lost question '+value);
      if(!item.values.length)assert(result.text.includes('- '+item.id+(item.label?' ('+item.label+')':'')+': 미선택'),'Offline copy omitted unanswered item '+item.id);
    }
  }
  var offlinePending=await offlineCopy(true);assertOfflineContext(offlinePending);
  assert(offlinePending.memo==='새 초안 두 번째'&&!offlinePending.text.includes('새 초안 두 번째'),'Offline copy used next draft instead of frozen submission');
  await pg.locator('#cancel').click();await sleep(150);await pg.locator('#send').click();
  for(var tick=0;tick<30;tick++){if(await pg.evaluate(()=>document.getElementById('status').dataset.state)==='received')break;await sleep(150);}
  assert(await pg.evaluate(()=>document.getElementById('status').dataset.state)==='received','Store.receive did not return actual queued reply');
  var receivedColor=await pg.evaluate(()=>getComputedStyle(document.getElementById('status')).backgroundColor);
  assert(receivedColor!==heldColor,'Received state looks the same as held');
  assert((await grayscale(true)).length===0,'Received state changes non-question palette');
  assert(await pg.evaluate(()=>document.getElementById('message').value)==='','Received memo not cleared');
  await pg.locator('#message').fill('복사 후에도 남을 초안');
  await pg.evaluate(()=>{Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async()=>{throw Error('Clipboard disabled in fallback test');}}});document.execCommand=()=>false;});
  await pg.locator('#copy').click();await sleep(150);
  var fallback=await pg.evaluate(()=>({summary:!document.getElementById('selection-summary').hidden,preview:document.getElementById('payload-preview').open,memo:document.getElementById('message').value,text:document.getElementById('payload-text').value,status:document.getElementById('draft-status').textContent}));
  assert(fallback.summary&&fallback.preview&&fallback.memo==='복사 후에도 남을 초안'&&fallback.text.includes('복사 후에도 남을 초안')&&fallback.status.includes('직접 복사'),'Copy fallback lost draft/selection');
  var offlineDraft=await offlineCopy(false);assertOfflineContext(offlineDraft);
  assert(offlineDraft.memo==='복사 후에도 남을 초안'&&offlineDraft.fallback&&offlineDraft.status.includes('직접 복사'),'Offline manual-copy fallback lost editor state');
  var screen=pwd+'/reader-dock-live.png';await fs.writeFile(screen,await pg.screenshot());
  var errors=await pg.evaluate(()=>globalThis.replyReaderErrors);assert(errors.length===0,'Unhandled runtime errors '+JSON.stringify(errors));
  await pg.goto(NESTED_URL,{waitUntil:'load'});await sleep(150);
  await pg.locator('#outline-toggle').click();await pg.locator('#outline-list button[data-heading="2"]').click();await sleep(700);
  var nestedState=await pg.evaluate(()=>new Promise(resolve=>{function receive(event){if(event.source!==document.getElementById('document').contentWindow||event.data?.type!=='reader-qa-measurement')return;removeEventListener('message',receive);resolve(event.data);}addEventListener('message',receive);document.getElementById('document').contentWindow.postMessage({type:'reader-qa-measure'},'*');}));
  var nestedDock=await pg.evaluate(()=>document.getElementById('reply-dock').getBoundingClientRect().top-document.getElementById('document').getBoundingClientRect().top);
  assert(nestedState.scroll>0&&nestedState.lastBottom<nestedDock,'Nested scroll end trapped behind composer '+JSON.stringify(nestedState));
  assert(await pg.evaluate(()=>document.querySelector('#outline-list [aria-current="location"]')?.firstElementChild.textContent)==='R2. 마지막 검토 항목','Nested scroll did not update active heading');
  await pg._sendToTarget('Input.dispatchMouseEvent',{type:'mouseMoved',x:20,y:760});
  await pg._sendToTarget('Input.dispatchMouseEvent',{type:'mouseWheel',x:20,y:760,deltaX:0,deltaY:-300});await sleep(200);
  var wheelState=await pg.evaluate(()=>new Promise(resolve=>{function receive(event){if(event.source!==document.getElementById('document').contentWindow||event.data?.type!=='reader-qa-measurement')return;removeEventListener('message',receive);resolve(event.data);}addEventListener('message',receive);document.getElementById('document').contentWindow.postMessage({type:'reader-qa-measure'},'*');}));
  assert(wheelState.scroll<nestedState.scroll,'Wheel beside composer did not reach source');
  await pg.evaluate(()=>document.getElementById('document').contentWindow.postMessage({type:'reader-qa-heading',action:'add'},'*'));await sleep(100);
  assert(await pg.evaluate(()=>document.querySelectorAll('#outline-list button').length===4&&document.querySelector('#outline-list button:last-child')!==null&&document.getElementById('outline-list').textContent.includes('추가 제목 <태그>')),'Dynamic heading not indexed safely');
  await pg.evaluate(()=>document.getElementById('document').contentWindow.postMessage({type:'reader-qa-heading',action:'hide'},'*'));await sleep(100);
  assert(await pg.evaluate(()=>document.querySelectorAll('#outline-list button').length)===3,'Hidden heading still indexed');
  await pg.evaluate(()=>document.getElementById('document').contentWindow.postMessage({type:'reader-qa-heading',action:'clear'},'*'));await sleep(100);
  assert(await pg.evaluate(()=>!document.getElementById('outline').hidden&&document.querySelectorAll('#outline-list button').length===0&&document.querySelectorAll('#outline-questions button').length===2),'Question-only outline disappeared with headings');
  await pg.goto(QUESTION_URL,{waitUntil:'load'});await sleep(150);
  await pg.evaluate(()=>{globalThis.questionErrors=[];addEventListener('error',e=>questionErrors.push(e.message));addEventListener('unhandledrejection',e=>questionErrors.push(String(e.reason)));});
  async function questionMeasure(){return await pg.evaluate(()=>new Promise(resolve=>{const listener=event=>{if(event.source!==document.getElementById('document').contentWindow||event.data?.type!=='question-qa-result')return;removeEventListener('message',listener);resolve(event.data);};addEventListener('message',listener);document.getElementById('document').contentWindow.postMessage({type:'question-qa-measure'},'*');}));}
  assert(await pg.evaluate(()=>document.querySelectorAll('#outline-questions button').length===4&&document.getElementById('review-progress').textContent.includes('0/4')),'Question/group/hidden count incorrect');
  await pg.locator('#next-question').click();await sleep(250);
  assert((await questionMeasure()).focus==='c1-origin','Next unanswered does not focus first real input');
  snap=await snapshot(pg,{interactive:true});await pg.locator(ref(snap.tree,'textbox','연결 의견')).fill('메모만 작성');await sleep(180);
  assert(await pg.evaluate(()=>document.querySelector('[data-question="C1"]').dataset.questionState)==='note','Memo-only choice falsely complete');
  await pg.locator(ref(snap.tree,'radio','아직 결정하지 않음')).click();await sleep(100);
  var questionStateColors=[];
  await pg.locator('#outline-toggle').click();
  for(var theme of ['light','dark']){
    // Compare settled theme colors, not an intermediate button transition.
    await pg._sendToTarget('Emulation.setEmulatedMedia',{features:[{name:'prefers-color-scheme',value:theme},{name:'prefers-reduced-motion',value:'reduce'}]});
    await sleep(200);
    var stateColors=await pg.evaluate(()=>{
      const read=selector=>{const s=getComputedStyle(document.querySelector(selector));return{color:s.color,background:s.backgroundColor};};
      return{answered:read('[data-question="C1"] .question-state'),unanswered:read('[data-question="C2"] .question-state'),progress:read('#review-complete'),pending:read('#review-pending'),heading:read('.heading-state[data-question-state="unanswered"]'),composer:read('.composer'),send:read('#send'),session:read('#session-open'),shortcut:read('#session-jump')};
    });
    const rgb=color=>color.match(/[\d.]+/g).slice(0,3).map(Number);
    const lum=color=>rgb(color).map(c=>{const v=c/255;return v<=0.04045?v/12.92:((v+0.055)/1.055)**2.4;}).reduce((n,v,i)=>n+v*[0.2126,0.7152,0.0722][i],0);
    const contrast=(a,b)=>{const x=lum(a),y=lum(b);return(Math.max(x,y)+0.05)/(Math.min(x,y)+0.05);};
    const green=rgb(stateColors.answered.color),red=rgb(stateColors.unanswered.color);
    assert(green[1]>green[0]&&green[1]>green[2]&&red[0]>red[1]&&red[0]>red[2],'Question status colors are not green/red '+JSON.stringify(stateColors));
    assert(stateColors.progress.color===stateColors.answered.color&&stateColors.pending.color===stateColors.unanswered.color&&stateColors.heading.color===stateColors.unanswered.color,'Progress/heading colors differ from question states');
    assert(contrast(stateColors.answered.color,stateColors.answered.background)>=4.5&&contrast(stateColors.unanswered.color,stateColors.unanswered.background)>=4.5,'Question status contrast is too low '+JSON.stringify(stateColors));
    const action=rgb(stateColors.send.background);
    assert(action[2]>action[0]&&action[2]>action[1]&&stateColors.session.background===stateColors.send.background&&stateColors.shortcut.color===stateColors.send.background,'Primary actions do not share blue emphasis '+JSON.stringify(stateColors));
    assert(contrast(stateColors.send.color,stateColors.send.background)>=4.5&&contrast(stateColors.session.color,stateColors.session.background)>=4.5,'Primary action text contrast is too low '+JSON.stringify(stateColors));
    assert((await grayscale(true)).length===0,'Status palette leaked into neutral controls');
    questionStateColors.push({theme,...stateColors});
  }
  await pg._sendToTarget('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});
  await pg._sendToTarget('Input.dispatchKeyEvent',{type:'keyUp',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});
  await pg.locator('#outline-toggle').click();await pg.locator('#outline-filter').click();
  assert(await pg.evaluate(()=>document.querySelector('[data-question="C1"]').parentElement.hidden&&document.getElementById('outline-list').hidden),'Unanswered filter retained answered question');
  await pg.locator('#outline-questions [data-question="C2"]').click();await sleep(250);snap=await snapshot(pg,{interactive:true});
  assert((await questionMeasure()).focus==='c2-draft','Question link did not focus source control');
  await pg.locator(ref(snap.tree,'checkbox','초안 보존')).click();await pg.locator(ref(snap.tree,'checkbox','모바일')).click();await pg.locator(ref(snap.tree,'checkbox','없음')).click();await sleep(160);
  assert(await pg.evaluate(()=>JSON.parse(localStorage.getItem('html-reply:'+JSON.parse(document.getElementById('reply-meta').textContent).id)).items.find(i=>i.id==='C2').values.join())==='없음','Exclusive none kept conflicting selections');
  await pg.locator(ref(snap.tree,'checkbox','초안 보존')).click();await sleep(150);
  assert(await pg.evaluate(()=>JSON.parse(localStorage.getItem('html-reply:'+JSON.parse(document.getElementById('reply-meta').textContent).id)).items.find(i=>i.id==='C2').values.join())==='초안 보존','Normal checkbox did not clear none');
  await pg.locator('#next-question').click();await sleep(250);snap=await snapshot(pg,{interactive:true});
  await pg.locator(ref(snap.tree,'textbox','직접 의견')).fill('   ');await sleep(150);
  assert(await pg.evaluate(()=>document.querySelector('[data-question="C3"]').dataset.questionState)==='unanswered','Whitespace treated as answer');
  await pg.locator(ref(snap.tree,'textbox','직접 의견')).fill('한글 의견 & <태그>');await sleep(180);
  assert(await pg.evaluate(()=>document.querySelector('[data-question="C3"]').dataset.questionState)==='answered','Written answer not complete');
  var typedFocus=await questionMeasure();assert(typedFocus.focus==='c3-answer'&&typedFocus.caret==='한글 의견 & <태그>'.length,'Question status update stole typing focus/caret '+JSON.stringify(typedFocus));
  await pg.locator('#next-question').click();await sleep(250);
  var openedQuestion=await questionMeasure();assert(openedQuestion.details&&openedQuestion.focus==='c4-multiple','Closed details question not revealed/focused');
  snap=await snapshot(pg,{interactive:true});await pg.locator(ref(snap.tree,'combobox','검증 환경')).selectOption(['Codex','GJC']);await sleep(180);
  assert(await pg.evaluate(()=>document.getElementById('next-question').hidden&&document.getElementById('review-progress').textContent.includes('4/4')),'Completed questions still pending');
  await pg.locator('#outline-toggle').click();if(await pg.evaluate(()=>document.getElementById('outline-filter').getAttribute('aria-pressed'))!=='true')await pg.locator('#outline-filter').click();
  assert(await pg.evaluate(()=>!document.getElementById('question-empty').hidden),'All-complete empty state missing');
  await pg._sendToTarget('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});
  snap=await snapshot(pg,{interactive:true});await pg.locator(ref(snap.tree,'button','조건 질문 토글')).click();await sleep(100);snap=await snapshot(pg,{interactive:true});
  await pg.locator(ref(snap.tree,'checkbox','조건 확인')).click();await pg.locator(ref(snap.tree,'button','조건 질문 토글')).click();await sleep(200);
  var questionErrors=await pg.evaluate(()=>globalThis.questionErrors);assert(questionErrors.length===0,'Question workflow runtime errors '+JSON.stringify(questionErrors));
  await pg.goto(QUESTION_URL+'?restore=question',{waitUntil:'load'});await sleep(200);
  var questionReload=await questionMeasure();assert(questionReload.selected.join()==='Codex,GJC'&&questionReload.conditional,'Reload lost multi-select/hidden question draft '+JSON.stringify(questionReload));
  assert(await pg.evaluate(()=>document.getElementById('review-progress').textContent.includes('4/4')),'Reload question progress differs');
  snap=await snapshot(pg,{interactive:true});await pg.locator(ref(snap.tree,'button','글 답변 활성 토글')).click();await sleep(120);
  assert(await pg.evaluate(()=>document.querySelectorAll('#outline-questions button').length)===3,'Disabled question remains actionable');
  await pg.goto(QUESTION_URL+'?restore=disabled',{waitUntil:'load'});await sleep(150);
  assert(await pg.evaluate(()=>document.querySelector('[data-question="C3"]').dataset.questionState)==='answered','Disabled answer draft lost on reload');
  snap=await snapshot(pg,{interactive:true});await pg.locator(ref(snap.tree,'button','읽기 전용 토글')).click();await sleep(140);
  assert(await pg.evaluate(()=>{const draft=JSON.parse(localStorage.getItem('html-reply:'+JSON.parse(document.getElementById('reply-meta').textContent).id));return draft.formState.find(f=>f.id==='C3').fields[0].value==='한글 의견 & <태그>'&&draft.formState.find(f=>f.id==='C1').fields.find(f=>f.key==='c1-note').value==='메모만 작성';}),'Readonly answer/note draft removed');
  await pg.goto(QUESTION_URL+'?restore=readonly',{waitUntil:'load'});await sleep(150);
  assert(await pg.evaluate(()=>document.querySelector('[data-question="C3"]').dataset.questionState)==='answered','Readonly draft lost on reload');
  snap=await snapshot(pg,{interactive:true});await pg.locator(ref(snap.tree,'button','글 질문 표시 토글')).click();await sleep(100);
  assert(await pg.evaluate(()=>document.querySelectorAll('#outline-questions button').length)===3,'Inline display change not observed');
  await pg.locator(ref(snap.tree,'button','글 질문 표시 토글')).click();await sleep(100);
  assert(await pg.evaluate(()=>document.querySelectorAll('#outline-questions button').length)===4,'Restored visible question missing');
  await pg.evaluate(url=>{const id=JSON.parse(document.getElementById('reply-meta').textContent).id;localStorage.setItem('html-reply:'+url.split('/').at(-1),localStorage.getItem('html-reply:'+id));},LATE_URL);
  await pg.goto(LATE_URL,{waitUntil:'load'});await sleep(150);
  assert(await pg.evaluate(()=>JSON.parse(localStorage.getItem('html-reply:'+JSON.parse(document.getElementById('reply-meta').textContent).id)).formState.find(f=>f.id==='C4').fields[0].selected.join())==='Codex,GJC','Pending option draft overwritten by empty select');
  await pg.goto(LATE_URL+'?reload=pending',{waitUntil:'load'});await sleep(150);
  snap=await snapshot(pg,{interactive:true});await pg.locator(ref(snap.tree,'button','선택지 로드')).click();await sleep(160);
  assert((await questionMeasure()).selected.join()==='Codex,GJC','Late options did not recover both saved choices');
  await pg.goto(QUESTION_URL+'?restore=after-late-check',{waitUntil:'load'});await sleep(150);
  snap=await snapshot(pg,{interactive:true});await pg.locator(ref(snap.tree,'checkbox','초안 보존')).click();await sleep(150);
  assert(await pg.evaluate(()=>document.querySelector('[data-question="C2"]').dataset.questionState)==='unanswered','Clearing all checks did not restore unanswered');
  var questionGeometries=[];
  for(var size of [[390,844],[768,900],[1440,900],[390,500],[844,390],[320,568]]){
    await pg._sendToTarget('Emulation.setDeviceMetricsOverride',{width:size[0],height:size[1],deviceScaleFactor:1,mobile:false});await sleep(80);
    await pg.locator('#outline-toggle').click();
    var bounds=await pg.evaluate(()=>{const r=document.getElementById('outline-panel').getBoundingClientRect();return{width:innerWidth,height:innerHeight,left:r.left,right:r.right,top:r.top,bottom:r.bottom,overflow:document.documentElement.scrollWidth-innerWidth};});
    assert(bounds.left>=0&&bounds.right<=bounds.width&&bounds.top>=0&&bounds.bottom<=bounds.height&&bounds.overflow<=1,'Question outline overflows viewport '+JSON.stringify(bounds));questionGeometries.push(bounds);
    await pg._sendToTarget('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});
    await pg._sendToTarget('Input.dispatchKeyEvent',{type:'keyUp',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});
  }
  await pg._sendToTarget('Emulation.clearDeviceMetricsOverride',{});
  await pg.locator('#send').click();await sleep(200);
  assert(await pg.evaluate(()=>document.getElementById('status').dataset.state)==='held','Partial questions could not be submitted');
  var questionPacket=await pg.evaluate(()=>document.getElementById('payload-text').value);
  assert(questionPacket.includes('<unanswered>C2</unanswered>')&&questionPacket.includes('<answer id="C3">한글 의견 &amp; &lt;태그&gt;</answer>')&&!questionPacket.includes('id="GROUP"')&&!questionPacket.includes('id="C5"'),'Partial question packet lost exact semantics '+questionPacket);
  await pg.locator('#cancel').click();await sleep(150);
  assert(await pg.evaluate(()=>document.getElementById('preview-scope').textContent)==='지금 보낼 초안','Cancelled response preview still marked frozen');
  var offlineQuestions=await offlineCopy(true);assertOfflineContext(offlineQuestions);
  assert(offlineQuestions.packet.items.find(item=>item.id==='C4').values.length===2,'Offline multi-choice fixture is missing');
  var starterChecks=[];
  for(var [index,starterUrl] of STARTER_URLS.entries()){
    await pg.goto(starterUrl,{waitUntil:'load'});
    for(var tick=0;tick<50;tick++){if(await pg.evaluate(index=>index===0?!!document.querySelector('#arch svg')&&!!document.getElementById('chart1')?._chart:!!document.querySelector('.stage'),index))break;await sleep(200);}
    assert(await pg.evaluate(index=>index===0?!!document.querySelector('#arch svg')&&!!document.getElementById('chart1')?._chart:!!document.querySelector('.stage'),index),'Starter dependencies did not render');
    for(var theme of ['light','dark']){
      if(index===0)await pg._sendToTarget('Emulation.setEmulatedMedia',{features:[{name:'prefers-color-scheme',value:theme}]});
      else if(await pg.evaluate(()=>document.documentElement.dataset.theme)!==theme)await pg.locator('.themebtn').click();
      await sleep(350);
      var colored=await grayscale();assert(colored.length===0,'Starter is not achromatic '+JSON.stringify({index,theme,colored}));
      if(index===0)assert(await pg.evaluate(()=>document.getElementById('chart1')._chart.getOption().color.every(c=>{const h=c.replace('#','');return h.slice(0,2)===h.slice(2,4)&&h.slice(2,4)===h.slice(4,6);} )),'Chart series palette is not gray');
      starterChecks.push({index,theme,grayscale:true});
    }
    if(index===1){await pg.locator('.nav button.move:last-child').click();await pg.locator('.simbtn').click();assert(await pg.evaluate(()=>!!document.querySelector('.reveal')),'Interactive starter no longer reveals content');}
  }
  console.log('REPLY_READER_QA '+JSON.stringify({initial,restored,geometries,contextGeometries,focusDenied,contextPreservesDraft:true,passthrough,sourceState,nestedState,paletteThemes,starterChecks,questionStateColors,questionReload,questionGeometries,questionPacket,questionErrors,questionNavigation:true,unansweredFilter:true,exclusiveNone:true,typedFocus,wheelPassthrough:true,statusColors:{draftColor,heldColor,receivedColor},dynamicHeadings:true,outlineHover:true,outlineNavigation:true,outlineEscape:true,ime,frozenPacket:true,received:true,copyFallback:true,offlinePending,offlineDraft,offlineQuestions,screenshot:screen,collapsedScreenshot:collapsedScreen,runtimeErrors:errors}));
} finally {await closeTab(pg);}
'''.replace("LATE_URL", json.dumps(late_url)).replace("QUESTION_URL", json.dumps(question_url)).replace("STARTER_URLS", json.dumps(starter_urls)).replace("NESTED_URL", json.dumps(nested_url)).replace("URL", json.dumps(url))
        result = subprocess.run(["aside", "repl", code], capture_output=True, text=True, timeout=100)
        (root / "browser.log").write_text(result.stdout + result.stderr)
        line = next((line for line in result.stdout.splitlines() if line.startswith("REPLY_READER_QA ")), None)
        if result.returncode or not line:
            raise RuntimeError((result.stdout + result.stderr)[-4500:])
        receipt = json.loads(line.removeprefix("REPLY_READER_QA "))
        receiver.join(timeout=5)
        assert received and "새 초안 두 번째" in received[0]["message"]
        assert "항목 이유 &amp; &lt;한글&gt;" in received[0]["message"]
        with store.connect() as db:
            states = [row[0] for row in db.execute("SELECT state FROM replies WHERE artifact=? ORDER BY created", (artifact["id"],))]
            question_rows = [row[0] for row in db.execute("SELECT payload FROM replies WHERE artifact=?", (question_artifact["id"],))]
        assert states == ["cancelled", "received"], states
        assert len(question_rows) == 1
        question_payload = json.loads(question_rows[0])
        assert [item['id'] for item in question_payload['items']] == ['C1', 'C2', 'C3', 'C4']
        assert question_payload['items'][2]['values'] == ['한글 의견 & <태그>']
        receipt.update(stored_states=states, actual_receiver=True, native_harness_tested=False)
        (root / "results.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2))
        print(json.dumps({"evidence": str(root / "results.json"), **receipt}, ensure_ascii=False, indent=2))
    finally:
        process.terminate()
        process.wait(timeout=5)
        log.close()


if __name__ == "__main__":
    main()
