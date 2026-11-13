#!/usr/bin/env python3
"""일반 페이지 주석을 실제 드래그와 격리된 수신 경로로 검증한다."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

SKILL = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("annotation_bridge", SKILL / "scripts/reply-bridge.py")
bridge = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bridge)

FIXTURE = '''<!doctype html><html lang="ko"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="darkreader-lock">
<style>body{margin:24px;font:16px/1.8 system-ui}p{max-width:40em}section{padding:20px 0}</style>
<title>주석 검증</title><article><h1>공통 페이지의 주석</h1><section id="evidence"><h2>검토할 문장</h2>
<p id="first">선택한 원문은 주석을 쓰는 동안 그대로 유지됩니다.</p>
<p id="second">새 선택이 작성 중인 주석의 원문을 바꾸면 안 됩니다.</p>
<input aria-label="선택 제외 입력" value="입력칸은 주석 대상으로 삼지 않습니다"></section></article></html>'''

BROWSER = r'''
const pg=await openTab('about:blank');
const check=(ok,message)=>{if(!ok)throw Error(message);};
async function waitFor(fn,message){for(let n=0;n<40;n++){if(await fn())return;await sleep(50);}throw Error(message);}
try {
 await pg._sendToTarget('Page.addScriptToEvaluateOnNewDocument',{source:'window.qaErrors=[];addEventListener("error",e=>qaErrors.push(e.message));addEventListener("unhandledrejection",e=>qaErrors.push(String(e.reason)));'});
 await pg.goto(PAGE_URL);console.log((await snapshot(pg,{interactive:true})).tree);
 await waitFor(()=>pg.evaluate(()=>document.getElementById('loading').hidden),'본문 초기화 실패');
 const frame=()=>pg.frames()[1];
 async function selection(id){
  await frame().evaluate(id=>{const node=document.getElementById(id);node.scrollIntoView({block:'center'});const range=document.createRange();range.selectNodeContents(node);getSelection().removeAllRanges();getSelection().addRange(range);document.dispatchEvent(new Event('selectionchange'));},id);
 }
 async function drag(id){
  const rect=await frame().evaluate(id=>{const node=document.getElementById(id);node.scrollIntoView({block:'center'});const text=node.firstChild;const a=document.createRange(),b=document.createRange();a.setStart(text,0);a.setEnd(text,1);b.setStart(text,10);b.setEnd(text,11);const x=a.getBoundingClientRect(),y=b.getBoundingClientRect();return{from:{x:x.left+1,y:x.top+x.height/2},to:{x:y.right-1,y:y.top+y.height/2}};},id);
  const offset=await pg.locator('#document').boundingBox();
  const from={x:rect.from.x+offset.x,y:rect.from.y+offset.y},to={x:rect.to.x+offset.x,y:rect.to.y+offset.y};
  await pg._sendToTarget('Input.dispatchMouseEvent',{type:'mouseMoved',...from});
  await pg._sendToTarget('Input.dispatchMouseEvent',{type:'mousePressed',...from,button:'left',buttons:1,clickCount:1});
  for(let n=1;n<=5;n++)await pg._sendToTarget('Input.dispatchMouseEvent',{type:'mouseMoved',x:from.x+(to.x-from.x)*n/5,y:from.y+(to.y-from.y)*n/5,button:'left',buttons:1});
  await pg._sendToTarget('Input.dispatchMouseEvent',{type:'mouseReleased',...to,button:'left',buttons:0,clickCount:1});
 }
 await drag('first');
 await waitFor(()=>pg.evaluate(()=>!document.getElementById('annotation-trigger').hidden),'드래그 주석 버튼 없음');
 check(await pg.evaluate(()=>document.activeElement.id==='document'&&document.getElementById('annotation-editor').hidden),'선택만으로 포커스를 빼앗음');
 await pg.locator('#annotation-trigger').click();
 const quote=await pg.locator('#annotation-selected').innerText();
 const note='문장에 사례를 추가해 주세요 & <검증>';
 await pg.locator('#annotation-note').fill(note);
 check(await pg.locator('#annotation-note').inputValue()===note,'주석 입력 불일치');
 check(await pg.evaluate(()=>document.getElementById('send').disabled),'미저장 주석을 누락한 채 전송 가능');
 await pg.locator('#annotation-cancel').click();
 await pg.goto(PAGE_URL);
 await waitFor(()=>pg.evaluate(()=>!document.getElementById('annotation-trigger').hidden),'닫은 주석 초안 복원 실패');
 await pg.locator('#annotation-trigger').click();
 check(await pg.locator('#annotation-note').inputValue()===note,'새로고침 후 주석 손실');
 await frame().evaluate(()=>{const range=document.createRange();range.selectNodeContents(document.getElementById('second'));getSelection().removeAllRanges();getSelection().addRange(range);document.dispatchEvent(new Event('selectionchange'));});
 await sleep(80);
 check(await pg.locator('#annotation-selected').innerText()===quote,'새 선택이 주석 원문을 변경');
 await pg.evaluate(()=>document.getElementById('annotation-note').dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',isComposing:true,bubbles:true})));
 check(await pg.evaluate(()=>!document.getElementById('annotation-editor').hidden),'IME 중 Escape가 주석을 닫음');
 const longNote='길'.repeat(1001);
 await pg.locator('#annotation-note').fill(longNote);
 check(await pg.locator('#annotation-note').inputValue()===longNote,'제한 초과 입력이 잘림');
 await pg.locator('#annotation-save').click();
 check(await pg.evaluate(()=>!document.getElementById('annotation-editor').hidden&&!!document.getElementById('annotation-error').textContent),'주석 길이 제한 검사 누락');
 await pg.locator('#annotation-note').fill(note);
 check(await pg.locator('#annotation-note').inputValue()===note,'저장 전 주석 불일치');
 await pg.locator('#annotation-save').click();
 await waitFor(()=>pg.evaluate(()=>document.getElementById('payload-text').value.includes('<annotation')),'주석 XML 없음');
 await pg.goto(PAGE_URL);
 await waitFor(()=>pg.evaluate(()=>document.querySelectorAll('.annotation-row').length===1),'저장된 주석 복원 실패');
 const layouts=[];
 for(const theme of ['light','dark']){
  await pg._sendToTarget('Emulation.setEmulatedMedia',{features:[{name:'prefers-color-scheme',value:theme}]});
  for(const [width,height] of [[1440,900],[390,844],[320,568]]){
   await pg._sendToTarget('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:false});
   await selection('second');await waitFor(()=>pg.evaluate(()=>!document.getElementById('annotation-trigger').hidden),'반응형 선택 실패 '+JSON.stringify({theme,width,height,source:await frame().evaluate(()=>({width:innerWidth,height:innerHeight,selected:getSelection().toString(),rect:document.getElementById('second').getBoundingClientRect().toJSON()})),parent:await pg.evaluate(()=>({width:innerWidth,height:innerHeight,frame:document.getElementById('document').getBoundingClientRect().toJSON(),dock:document.getElementById('reply-dock').getBoundingClientRect().toJSON()}))}));
   await pg.locator('#annotation-trigger').click();
   const g=await pg.evaluate(()=>{const r=document.getElementById('annotation-editor').getBoundingClientRect();return{left:r.left,top:r.top,right:r.right,bottom:r.bottom,width:innerWidth,height:innerHeight,overflow:document.documentElement.scrollWidth-innerWidth};});
   check(g.left>=0&&g.top>=0&&g.right<=g.width+1&&g.bottom<=g.height+1&&g.overflow<=1,'주석 창 넘침 '+JSON.stringify(g));layouts.push({theme,syntheticSelection:true,...g});
   await pg.locator('#annotation-cancel').click();
  }
 }
 await pg._sendToTarget('Emulation.clearDeviceMetricsOverride',{});
 await pg.locator('#context-open').click();
 await pg.locator('#summary-toggle').click();
 check(await pg.evaluate(()=>document.getElementById('payload-preview').closest('#context-view')&&!document.getElementById('toggle')&&!document.getElementById('recipient')),'정보와 메모 분리 실패');
 await pg.locator('#context-close').click();
 await waitFor(()=>pg.evaluate(()=>!document.getElementById('send').disabled),'저장된 주석 전송 불가');
 await pg.locator('#send').click();
 await waitFor(()=>pg.evaluate(()=>document.getElementById('status').dataset.state==='held'),'격리 저장 실패');
 const frozen=await pg.locator('#payload-text').inputValue();
 await pg.locator('#context-open').click();
 await pg.locator('.annotation-row button').click();
 await sleep(200);
 check(await pg.locator('#payload-text').inputValue()===frozen,'다음 초안 변경이 전송 중 주석을 바꿈');
 check(await pg.evaluate(()=>window.qaErrors.length===0),'브라우저 실행 오류');
 console.log('ANNOTATION_PANEL_QA '+JSON.stringify({actualDrag:true,draftRecovery:true,frozenQuote:true,ime:true,limitRetention:true,layouts,frozenPacket:true,errors:[]}));
} finally { await pg._sendToTarget('Emulation.clearDeviceMetricsOverride',{}); await closeTab(pg); }
'''


def main():
    root = Path(tempfile.mkdtemp(prefix="annotation-panel-browser-"))
    source = root / "fixture.html"
    source.write_text(FIXTURE)
    store = bridge.Store(root / "state")
    art = store.register(source, "일반 페이지 주석 검증", "codex", "annotation-browser-origin", "isolated-annotation-test")
    with (root / "service.log").open("w") as log:
        process = subprocess.Popen([sys.executable, str(SKILL / "scripts/reply-bridge.py"), "--state-dir", str(store.root), "serve", "--preview"], stdout=log, stderr=log)
        try:
            for _ in range(80):
                info = bridge.running(store)
                if info and info["pid"] == process.pid:
                    break
                if process.poll() is not None:
                    raise RuntimeError("격리 서버 종료")
                time.sleep(.05)
            else:
                raise RuntimeError("격리 서버 시작 실패")
            url = f'http://127.0.0.1:{info["port"]}/artifact/{art["id"]}'
            result = subprocess.run(["aside", "repl", BROWSER.replace("PAGE_URL", json.dumps(url))], capture_output=True, text=True, timeout=115)
            (root / "browser.log").write_text(result.stdout + result.stderr)
            receipt = next((line.removeprefix("ANNOTATION_PANEL_QA ") for line in result.stdout.splitlines() if line.startswith("ANNOTATION_PANEL_QA ")), None)
            if result.returncode or not receipt:
                raise RuntimeError(str(root / "browser.log") + "\n" + (result.stdout + result.stderr)[-3000:])
            received = store.receive(art["id"], "annotation-browser-origin", 5)
            assert "<annotation" in received["message"]
            assert "&amp; &lt;검증&gt;" in received["message"]
            report = json.loads(receipt)
            report.update(actualReceiver=True, nativeHarnessTested=False)
            (root / "results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
            print(json.dumps({"results": str(root / "results.json"), **report}, ensure_ascii=False))
        finally:
            process.terminate()
            process.wait(timeout=5)


if __name__ == "__main__":
    main()
