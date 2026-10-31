#!/usr/bin/env python3
"""Verify the reusable review template in Aside and an isolated reply service.

Uses actual pointer input plus the existing HTTP/SQLite/Store.receive path.
No live native conversation or model receives test input. Run with Python 3.
"""
import importlib.util
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import xml.etree.ElementTree as ET

SKILL = Path(__file__).resolve().parents[1]
BRIDGE_PATH = SKILL / "scripts/reply-bridge.py"
SPEC = importlib.util.spec_from_file_location("review_template_bridge", BRIDGE_PATH)
bridge = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bridge)

PROBE = r'''<script>
window.reviewErrors=[];
addEventListener('error',e=>reviewErrors.push(e.message));
addEventListener('unhandledrejection',e=>reviewErrors.push(String(e.reason)));
addEventListener('message',event=>{
 if(event.source!==parent||event.data?.type!=='review-qa')return;
 const {op,id}=event.data;
 const item=document.querySelector('#review-document [data-item="'+(id||'R1')+'"]');
 const target=item?.querySelector('p');
 const rect=node=>{const r=node.getBoundingClientRect();return {left:r.left,top:r.top,right:r.right,bottom:r.bottom,width:r.width,height:r.height};};
 if(op==='scroll')window.scrollTo(0,item.getBoundingClientRect().top+scrollY-65);
 if(op==='select'){
  const range=document.createRange();range.selectNodeContents(target);
  getSelection().removeAllRanges();getSelection().addRange(range);
  document.dispatchEvent(new Event('selectionchange'));
 }
 if(op==='cross'){
  const range=document.createRange();range.setStart(document.querySelector('[data-item="R1"] p').firstChild,0);range.setEnd(document.querySelector('[data-item="R2"] p').firstChild,2);
  getSelection().removeAllRanges();getSelection().addRange(range);document.dispatchEvent(new Event('selectionchange'));
 }
 if(op==='clear'){getSelection().removeAllRanges();document.dispatchEvent(new Event('selectionchange'));}
 if(op==='comment')document.getElementById('selection-comment').click();
 if(op==='close')document.getElementById('selection-close').click();
 if(op==='notes'){const list=document.getElementById('notes-'+id);list.open=true;window.scrollTo(0,list.getBoundingClientRect().top+scrollY-65);}
 if(op==='composition')document.getElementById('selection-message').dispatchEvent(new CompositionEvent('compositionstart',{bubbles:true}));
 if(op==='composition-end')document.getElementById('selection-message').dispatchEvent(new CompositionEvent('compositionend',{bubbles:true}));
 if(op==='disable')item.querySelector('input').disabled=!item.querySelector('input').disabled;
 if(op==='hide')item.hidden=!item.hidden;
 requestAnimationFrame(()=>requestAnimationFrame(()=>{
  const textNode=document.querySelector('[data-item="R1"] p').firstChild;
  const start=document.createRange(),end=document.createRange();start.setStart(textNode,0);start.setEnd(textNode,1);end.setStart(textNode,Math.min(11,textNode.length-1));end.setEnd(textNode,Math.min(12,textNode.length));
  const a=rect(start),b=rect(end),selected=getSelection();
  const colors=[...document.querySelectorAll('#review-document .review-row')].map(row=>{const badge=row.querySelector('[data-reply-state]');const style=getComputedStyle(badge);return {state:row.dataset.reviewState,text:badge.textContent,color:style.color,bg:style.backgroundColor};});
  parent.postMessage({type:'review-qa-result',key:event.data.key,width:innerWidth,height:innerHeight,overflow:document.documentElement.scrollWidth-innerWidth,scroll:scrollY,focus:document.activeElement.id,caret:document.activeElement.selectionStart,icon:!document.getElementById('selection-action').hidden,iconRect:rect(document.getElementById('selection-action')),editor:!document.getElementById('selection-editor').hidden,editorRect:rect(document.getElementById('selection-editor')),text:document.getElementById('selection-message').value,quote:document.getElementById('selection-quote').textContent,selectedText:selected.toString(),selectedRect:selected.rangeCount?rect(selected.getRangeAt(0)):null,drag:{from:{x:a.left+1,y:a.top+a.height/2},to:{x:b.right-1,y:b.top+b.height/2}},state:document.getElementById('selection-state').value,checks:['R1','R2','R3'].map(q=>document.querySelector('[data-item="'+q+'"] input').checked),memos:['R1','R2','R3'].map(q=>document.getElementById('memo-'+q).value),colors,notices:[...document.querySelectorAll('#selection-note-status,.section-notes')].map(e=>e.textContent).join('\n'),errors:reviewErrors},'*');
 }));
});
</script>'''

BROWSER = r'''
var pg=await openTab(PAGE_URL);
try{
 function check(ok,message){if(!ok)throw Error(message);}
 function ref(tree,kind,label){const matches=[...tree.matchAll(new RegExp(kind+' "([^"\\n]*)" \\[ref=([^\\]]+)\\]','g'))];const found=matches.find(m=>m[1]===label||m[1]===label+' '+label);if(!found)throw Error('Missing '+kind+' '+label+'\n'+tree);return found[2];}
 async function click(kind,label){const snap=await snapshot(pg,{interactive:true});await pg.locator(ref(snap.tree,kind,label)).click();}
 async function source(op='measure',id=''){return await pg.evaluate(({op,id})=>new Promise((resolve,reject)=>{const key=crypto.randomUUID();const timer=setTimeout(()=>{removeEventListener('message',listener);reject(Error('Source timeout'));},5000);function listener(event){if(event.source!==document.getElementById('document').contentWindow||event.data?.type!=='review-qa-result'||event.data.key!==key)return;removeEventListener('message',listener);clearTimeout(timer);resolve(event.data);}addEventListener('message',listener);document.getElementById('document').contentWindow.postMessage({type:'review-qa',op,id,key},'*');}),{op,id});}
 async function fillNote(value){const snap=await snapshot(pg,{interactive:true});await pg.locator(ref(snap.tree,'textbox','선택한 부분의 주석')).fill(value);}
 async function waitFor(fn,message){for(let n=0;n<40;n++){if(await fn())return;await sleep(75);}throw Error(message);}
 function contrast(fg,bg){const lum=c=>c.match(/[\d.]+/g).slice(0,3).map(Number).map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4;}).reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0);return(Math.max(lum(fg),lum(bg))+.05)/(Math.min(lum(fg),lum(bg))+.05);}
 console.log((await snapshot(pg,{interactive:true})).tree);
 await pg._sendToTarget('Emulation.setEmulatedMedia',{features:[{name:'prefers-color-scheme',value:'light'},{name:'prefers-reduced-motion',value:'reduce'}]});
 await waitFor(async()=>await pg.evaluate(()=>document.querySelectorAll('[data-question]').length===3),'Questions did not arrive');
 const initial=await source();check(initial.checks.every(v=>!v)&&!initial.icon&&!initial.editor,'Initial answers were invented');
 check(await pg.evaluate(()=>document.getElementById('send').disabled),'Hidden state is treated as sendable data');
 const tree=(await snapshot(pg,{interactive:true})).tree;const checkbox=tree.match(/checkbox "[^"]+" \[ref=([^\]]+)\]/);check(checkbox,'No actual checkbox');await pg.locator(checkbox[1]).click();
 await waitFor(async()=>(await source()).colors[0].state==='answered','Checkbox badge did not complete');
 await source('scroll','R1');
 const drag=await source(),offset=await pg.evaluate(()=>{const r=document.getElementById('document').getBoundingClientRect();return{x:r.left,y:r.top};});
 const from={x:drag.drag.from.x+offset.x,y:drag.drag.from.y+offset.y},to={x:drag.drag.to.x+offset.x,y:drag.drag.to.y+offset.y};
 await pg._sendToTarget('Input.dispatchMouseEvent',{type:'mouseMoved',...from});await pg._sendToTarget('Input.dispatchMouseEvent',{type:'mousePressed',...from,button:'left',buttons:1,clickCount:1});
 for(let n=1;n<=5;n++)await pg._sendToTarget('Input.dispatchMouseEvent',{type:'mouseMoved',x:from.x+(to.x-from.x)*n/5,y:from.y+(to.y-from.y)*n/5,button:'left',buttons:1});
 await pg._sendToTarget('Input.dispatchMouseEvent',{type:'mouseReleased',...to,button:'left',buttons:0,clickCount:1});
 await waitFor(async()=>(await source()).icon,'Real drag failed to reveal icon');
 const selected=await source();check(selected.selectedText.length>2&&selected.iconRect.left>=selected.selectedRect.right-2&&selected.iconRect.bottom<=selected.selectedRect.top+3,'Icon is not at selected text upper-right');
 await pg.screenshot({path:'review-selection.png'});
 await click('button','선택한 문장에 주석');await fillNote('첫 주석 & <태그>');
 await waitFor(async()=>(await source()).memos[0].includes('첫 주석 & <태그>'),'Annotation is not collected automatically');
 const typed=await source();check(typed.focus==='selection-message'&&typed.caret===11,'Typing lost focus/caret');
 check(typed.editorRect.left>=0&&typed.editorRect.top>=0&&typed.editorRect.bottom<=typed.height,'Editor escaped viewport '+JSON.stringify(typed.editorRect));
 const before=typed.editorRect;await fillNote('첫 주석 & <태그> 추가');const after=await source();check(Math.abs(after.editorRect.left-before.left)<3&&Math.abs(after.editorRect.top-before.top)<3,'Editor jumps when selection collapses during typing');await fillNote('첫 주석 & <태그>');
 await source('composition');await pg._sendToTarget('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});await pg._sendToTarget('Input.dispatchKeyEvent',{type:'keyUp',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});check((await source()).editor,'IME Escape closed draft');await source('composition-end');
 await pg.screenshot({path:'review-editor.png'});await click('button','주석 창 닫기');
 await pg.goto(PAGE_URL,{waitUntil:'load'});await waitFor(async()=>(await source()).memos[0].includes('첫 주석 & <태그>'),'Note did not restore');
 check((await source()).checks[0],'Checked answer did not restore');
 const again=(await snapshot(pg,{interactive:true})).tree.match(/checkbox "[^"]+" \[ref=([^\]]+)\]/);await pg.locator(again[1]).click();await waitFor(async()=>(await source()).colors[0].state==='unanswered','Note incorrectly completes an unchecked item');
 check(await pg.evaluate(()=>document.querySelector('[data-question="R1"]').dataset.questionState==='note'),'Note-only question not pending');
 const uncheck=(await snapshot(pg,{interactive:true})).tree.match(/checkbox "[^"]+" \[ref=([^\]]+)\]/);await pg.locator(uncheck[1]).click();
 await source('notes','R1');await click('button','R1 주석 1 수정');
 const rejected='길'.repeat(1001);await fillNote(rejected);
 await waitFor(async()=>(await source()).memos[0]==='','Over-limit edit sends stale accepted text');check((await source()).notices.includes('전송에서 제외됨, 내용을 줄여 주세요'),'Rejected draft lacks persistent warning');
 await click('button','주석 창 닫기');await pg.goto(PAGE_URL,{waitUntil:'load'});await waitFor(async()=>(await source()).state.includes(rejected),'Exact rejected draft not restored');
 check((await source()).memos[0]===''&&(await source()).checks[0],'Rejected note changed answers or outgoing carrier');
 await source('notes','R1');await click('button','R1 주석 1 수정');check((await source()).text===rejected,'Rejected editor content was truncated');await fillNote('첫 주석 & <태그>');await click('button','주석 창 닫기');
 await source('scroll','R2');await source('select','R2');await waitFor(async()=>(await source()).icon,'Second question selection missing');await click('button','선택한 문장에 주석');await fillNote('삭제할 의견');await click('button','주석 창 닫기');
 await source('notes','R2');await click('button','R2 주석 1 위치');check((await source()).selectedText.length>0,'Location does not restore quotation');
 await source('notes','R2');await click('button','R2 주석 1 지우기');const deleted=await source();check(deleted.memos[1]==='','Delete did not clear item memo '+JSON.stringify({state:deleted.state,memo:deleted.memos[1],focus:deleted.focus,editor:deleted.editor,errors:deleted.errors}));
 await source('scroll','R2');await source('select','R2');await waitFor(async()=>(await source()).icon,'Second question selection missing after delete');await click('button','선택한 문장에 주석');await fillNote('두 번째 주석');await click('button','주석 창 닫기');
 await pg.locator('#summary-toggle').click();await waitFor(async()=>await pg.evaluate(()=>document.getElementById('payload-text').value.includes('두 번째 주석')),'Outgoing preview did not update');
 const packet=await pg.evaluate(()=>document.getElementById('payload-text').value);
 check(packet.includes('<answer id="R1">')&&packet.includes('<note for="R1">')&&packet.includes('<note for="R2">')&&packet.includes('첫 주석 &amp; &lt;태그&gt;')&&packet.includes('<unanswered>R2 R3</unanswered>')&&!packet.includes('ANNOTATION_STATE'),'Compact item packet mismatch '+packet);
 await pg.locator('#summary-toggle').click();
 const palette=[];
 for(const theme of ['light','dark']){
  await pg._sendToTarget('Emulation.setEmulatedMedia',{features:[{name:'prefers-color-scheme',value:theme},{name:'prefers-reduced-motion',value:'reduce'}]});await sleep(90);
  const s=await source(),green=s.colors[0].color.match(/[\d.]+/g).slice(0,3).map(Number),red=s.colors[1].color.match(/[\d.]+/g).slice(0,3).map(Number);
  check(green[1]>green[0]&&red[0]>red[1]&&s.colors.every(c=>contrast(c.color,c.bg)>=4.5),'State color or contrast regression');palette.push({theme,colors:s.colors});
 }
 await pg.locator('#message').fill('고정된 첫 회신');await pg.locator('#send').click();await waitFor(async()=>await pg.evaluate(()=>document.getElementById('status').dataset.state)==='held','Isolated reply not held');
 const frozen=await pg.evaluate(()=>document.getElementById('payload-text').value);
 await source('scroll','R1');await source('notes','R1');await click('button','R1 주석 1 수정');await fillNote('수정한 첫 주석 & <태그>');await click('button','주석 창 닫기');check(await pg.evaluate(()=>document.getElementById('payload-text').value)===frozen,'Pending packet mutated');
 await pg.locator('#message').fill('REVIEW_TEMPLATE_RECEIVER');await pg.locator('#cancel').click();await waitFor(async()=>await pg.evaluate(()=>document.getElementById('status').dataset.state)!=='held','Cancel not applied');await pg.locator('#send').click();await waitFor(async()=>await pg.evaluate(()=>document.getElementById('status').dataset.state)==='received','Isolated Store.receive failed');
 await pg.locator('#toggle').click();const layouts=[];
 for(const theme of ['light','dark']){
  await pg._sendToTarget('Emulation.setEmulatedMedia',{features:[{name:'prefers-color-scheme',value:theme},{name:'prefers-reduced-motion',value:'reduce'}]});
  for(const size of [[1440,900],[768,900],[390,844],[320,568],[844,390]]){
   await pg._sendToTarget('Emulation.setDeviceMetricsOverride',{width:size[0],height:size[1],deviceScaleFactor:1,mobile:false});await source('scroll','R1');await source('select','R1');await waitFor(async()=>(await source()).icon,'Responsive selection missing');await source('comment');const g=await source();
   check(g.editor&&g.overflow<=1&&g.editorRect.left>=0&&g.editorRect.right<=g.width&&g.editorRect.top>=0&&g.editorRect.bottom<=g.height,'Responsive editor overflow '+JSON.stringify({theme,size,g}));layouts.push({theme,size,editor:g.editorRect,syntheticOpen:true});await source('close');await source('clear');
  }
 }
 await pg._sendToTarget('Emulation.clearDeviceMetricsOverride',{});await source('cross');await sleep(80);check(!(await source()).icon,'Cross-item selection attached to arbitrary item');await source('clear');
 const errors=(await source()).errors;check(!errors.length,'Runtime errors '+JSON.stringify(errors));
 console.log('REVIEW_CONNECTED '+JSON.stringify({actualMouseDrag:true,restored:true,rejectedDraftRecovery:true,frozenPacket:true,actualReceiver:true,nativeHarnessTested:false,packet,palette,layouts,errors,screenshots:['review-selection.png','review-editor.png'].map(n=>pwd+'/'+n)}));
}finally{await pg._sendToTarget('Emulation.clearDeviceMetricsOverride',{});await closeTab(pg);}
'''

STANDALONE = r'''
var file=await openTab(FILE_URL);
try{
 function check(value,message){if(!value)throw Error(message);}
 console.log((await snapshot(file,{interactive:true})).tree);
 check(await file.evaluate(()=>!document.getElementById('standalone-review').hidden),'Standalone copy surface absent');
 await file.locator('#check-R1').click();await file.locator('#review-overall-memo').fill('파일 전체 의견 & <한글>');
 await file.evaluate(()=>{const p=document.querySelector('[data-item="R1"] p');p.scrollIntoView({block:'center'});const r=document.createRange();r.selectNodeContents(p);getSelection().removeAllRanges();getSelection().addRange(r);document.dispatchEvent(new Event('selectionchange'));});
 await file.locator('#selection-comment').click();await file.locator('#selection-message').fill('파일 주석');await file.locator('#selection-close').click();
 await file.goto(FILE_URL,{waitUntil:'load'});
 check(await file.evaluate(()=>document.getElementById('check-R1').checked&&document.getElementById('review-overall-memo').value==='파일 전체 의견 & <한글>'&&document.getElementById('memo-R1').value.includes('파일 주석')),'Standalone draft failed to restore');
 const reply=await file.evaluate(()=>document.getElementById('review-reply').value);
 check(reply.includes('파일 주석')&&reply.includes('파일 전체 의견 & <한글>')&&reply.includes('R2')&&reply.includes('미확인'),'File copy is not self-contained');
 check(await file.evaluate(()=>document.getElementById('review-reply').value.includes(document.querySelector('label[for="check-R1"]').textContent.trim())),'Standalone question label missing');
 await file.evaluate(()=>{window.reviewCopied=null;Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async value=>{window.reviewCopied=value;}}});});await file.locator('#review-copy').click();
 check(await file.evaluate(()=>window.reviewCopied===document.getElementById('review-reply').value),'Clipboard received different packet');
 await file.evaluate(()=>{navigator.clipboard.writeText=async()=>{throw Error('denied');};});await file.locator('#review-copy').click();
 check(await file.evaluate(()=>document.getElementById('review-copy-status').textContent.includes('직접')&&document.getElementById('review-overall-memo').value==='파일 전체 의견 & <한글>'),'Manual fallback lost memo or instructions');
 const limits=await file.evaluate(async()=>{
  const field=document.getElementById('selection-state'),original=JSON.parse(field.value),sample=original.notes[0];
  function load(notes){field.value=JSON.stringify({...original,notes,activeId:null});field.dispatchEvent(new Event('input',{bubbles:true}));}
  const settle=()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));
  load(Array.from({length:20},(_,i)=>({...sample,id:'bounded-'+i,revision:i+1,message:String(i).padStart(2,'0')+' '+('긴'.repeat(997))})));await settle();
  const large=document.getElementById('memo-R1').value,kept=JSON.parse(field.value).notes;
  if(large.length>12000||!document.getElementById('review-validation').textContent.includes('전송에서 제외됨')||kept.length!==20||kept.some(note=>note.message.length!==1000))throw Error('Packet cap lost drafts or exported too much');
  load(Array.from({length:20},(_,i)=>({...sample,id:'count-'+i,revision:i+1,message:'주석 '+i})));await settle();
  const p=document.querySelector('[data-item="R1"] p'),r=document.createRange();r.selectNodeContents(p);getSelection().removeAllRanges();getSelection().addRange(r);document.dispatchEvent(new Event('selectionchange'));await settle();document.getElementById('selection-comment').click();await settle();
  if(JSON.parse(field.value).notes.length!==20||!document.getElementById('selection-editor').hidden||!document.getElementById('review-selection-status').textContent.includes('20개'))throw Error('Note count cap failed');
  load(original.notes);await settle();return{packetCap:true,noteCountCap:true,draftsRetained:true,syntheticBoundaryState:true};
 });
 const answerTypes=await file.evaluate(async()=>{
  const section=document.querySelector('[data-item="R3"]'),row=section.querySelector('.review-row'),field=section.querySelector('input');
  const settle=()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));
  for(const type of ['text','number']){
   field.type=type;field.value=type==='text'?'직접 답변':'7';field.dispatchEvent(new Event('input',{bubbles:true}));await settle();if(row.dataset.reviewState!=='answered')throw Error('Written answer does not complete '+type);
   field.readOnly=true;await settle();if(row.dataset.reviewState!=='unanswered')throw Error('Readonly answer completes '+type);
   field.readOnly=false;field.disabled=true;await settle();if(row.dataset.reviewState!=='unanswered')throw Error('Disabled answer completes '+type);
   field.disabled=false;field.value='';field.dispatchEvent(new Event('input',{bubbles:true}));await settle();if(row.dataset.reviewState!=='unanswered')throw Error('Empty answer completes '+type);
  }
  return{written:true,readonlyExcluded:true,disabledExcluded:true,emptyExcluded:true};
 });
 console.log('REVIEW_STANDALONE '+JSON.stringify({restored:true,clipboardArgumentMatches:true,manualFallback:true,actualClipboardReadback:false,limits,answerTypes,reply}));
}finally{await closeTab(file);}
'''


def main(template=None):
    root = Path(tempfile.mkdtemp(prefix="review-template-browser-"))
    # Renaming every sample ID tests that runtime behavior is not C1/C2/C3-specific.
    content = Path(template or SKILL / "assets/review-template.html").read_text()
    for old, new in [("C1", "R1"), ("C2", "R2"), ("C3", "R3")]:
        content = content.replace(old, new)
    source = root / "review.html"
    source.write_text(content.replace("</body>", PROBE + "</body>"))
    store = bridge.Store(root / "state")
    art = store.register(source, "검토 템플릿 검증", "codex", "review-template-origin", "isolated-review-template", "격리된 검토 템플릿")
    received = []
    stop = threading.Event()
    log = (root / "service.log").open("w")
    process = subprocess.Popen([sys.executable, str(BRIDGE_PATH), "--state-dir", str(store.root), "serve", "--preview"], stdout=log, stderr=log)
    standalone_server = None
    try:
        for _ in range(80):
            info = bridge.running(store)
            if info and info["pid"] == process.pid:
                break
            if process.poll() is not None:
                raise RuntimeError("Isolated service exited")
            time.sleep(.05)
        else:
            raise RuntimeError("Isolated service did not start")

        def receive():
            deadline = time.monotonic() + 150
            while not stop.is_set() and time.monotonic() < deadline:
                with store.connect() as db:
                    row = db.execute("SELECT payload FROM replies WHERE artifact=? AND state='held' ORDER BY created DESC LIMIT 1", (art["id"],)).fetchone()
                if row and json.loads(row["payload"])["text"] == "REVIEW_TEMPLATE_RECEIVER":
                    received.append(store.receive(art["id"], "review-template-origin", 5))
                    return
                stop.wait(.05)

        receiver = threading.Thread(target=receive, daemon=True)
        receiver.start()
        url = f'http://127.0.0.1:{info["port"]}/artifact/{art["id"]}'
        result = subprocess.run(["aside", "repl", BROWSER.replace("PAGE_URL", json.dumps(url))], capture_output=True, text=True, timeout=165)
        (root / "browser.log").write_text(result.stdout + result.stderr)
        receipt = next((line.removeprefix("REVIEW_CONNECTED ") for line in result.stdout.splitlines() if line.startswith("REVIEW_CONNECTED ")), None)
        if result.returncode or not receipt:
            raise RuntimeError(f"Browser verification failed; log: {root / 'browser.log'}\n{(result.stdout + result.stderr)[-5000:]}")
        receiver.join(timeout=3)
        assert received, "No actual isolated receipt"
        with store.connect() as db:
            rows = [dict(row) for row in db.execute("SELECT * FROM replies WHERE artifact=? ORDER BY created, rowid", (art["id"],))]
        assert [row["state"] for row in rows] == ["cancelled", "received"]
        payload = json.loads(rows[1]["payload"])
        items = {item["id"]: item for item in payload["items"]}
        assert set(items) == {"R1", "R2", "R3"}
        assert items["R1"]["values"] and not items["R2"]["values"]
        assert "수정한 첫 주석 & <태그>" in items["R1"]["memo"] and "두 번째 주석" in items["R2"]["memo"]
        assert "삭제할 의견" not in items["R2"]["memo"] and "길" * 1001 not in rows[1]["payload"]
        message = bridge.reply_text(art, rows[1])
        xml = ET.fromstring(message[message.index("<feedback"):])
        assert xml.find("note[@for='R1']").text == items["R1"]["memo"]
        assert xml.find("unanswered").text == "R2 R3"
        report = json.loads(receipt)
        report.update(test_root=str(root), delivered_message=message)
        class SourceHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path != "/review.html":
                    self.send_error(404)
                    return
                body = source.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *_args):
                pass

        # Aside disallows file URLs without its optional local-file permission.
        # Exercise the identical unframed source over isolated loopback instead;
        # this does not establish file:// storage/clipboard permission behavior.
        standalone_server = ThreadingHTTPServer(("127.0.0.1", 0), SourceHandler)
        threading.Thread(target=standalone_server.serve_forever, daemon=True).start()
        standalone_url = f"http://127.0.0.1:{standalone_server.server_port}/review.html"
        file_result = subprocess.run(["aside", "repl", STANDALONE.replace("FILE_URL", json.dumps(standalone_url))], capture_output=True, text=True, timeout=50)
        (root / "standalone.log").write_text(file_result.stdout + file_result.stderr)
        file_receipt = next((line.removeprefix("REVIEW_STANDALONE ") for line in file_result.stdout.splitlines() if line.startswith("REVIEW_STANDALONE ")), None)
        if file_result.returncode or not file_receipt:
            raise RuntimeError(f"Standalone verification failed; log: {root / 'standalone.log'}\n{(file_result.stdout + file_result.stderr)[-5000:]}")
        report["standalone"] = json.loads(file_receipt)
        report["standalone"]["transport"] = "isolated-loopback-unframed"
        report["standalone"]["filePermissionsVerified"] = False
        (root / "results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
        print(json.dumps({"results": str(root / "results.json"), "actualMouseDrag": True, "actualReceiver": True, "nativeHarnessTested": False, "layouts": len(report["layouts"]), "errors": report["errors"]}, ensure_ascii=False))
    finally:
        stop.set()
        if standalone_server:
            standalone_server.shutdown()
            standalone_server.server_close()
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=3)
        log.close()


if __name__ == "__main__":
    main()
