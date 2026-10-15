const $=id=>document.getElementById(id);
function toast(s){const t=$("toast");t.textContent=s;t.classList.add("show");setTimeout(()=>t.classList.remove("show"),3000)}
async function post(url,data){const r=await fetch(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});const d=await r.json();if(!r.ok)throw Error(d.error||"Request failed");return d}
async function run(button,url,data,target){button.disabled=true;const old=button.textContent;button.textContent="Working…";try{const d=await post(url,data);const el=$(target);el.classList.remove("hidden");if(target==="riskout"){const level=d.level.toLowerCase();el.innerHTML=`<div class="risknum ${level}">${d.score}/10 · ${d.level}</div><p>${d.changed_files} changed files · ${d.requires_human_review?"Human review recommended":"No high-risk path signal detected"}</p><ul>${d.factors.map(x=>"<li>"+esc(x)+"</li>").join("")}</ul><small>${esc(d.disclaimer)}</small>`}else el.textContent=d.report;el.scrollIntoView({behavior:"smooth",block:"nearest"});toast("Done")}catch(e){toast(e.message)}finally{button.disabled=false;button.textContent=old}}
function esc(s){return String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]))}
$("samplelog").onclick=()=>$("log").value="Running tests…\nTraceback (most recent call last):\nAssertionError: expected 200, received 500\nFAILED tests/test_api.py::test_health";
$("samplepaths").onclick=()=>$("paths").value="backend/auth.py\nk8s/deployment.yaml\ndb/migrations/001.sql\nrequirements.txt";
$("analyze").onclick=e=>run(e.currentTarget,"/api/analyze-log",{log:$("log").value},"logout");
$("score").onclick=e=>run(e.currentTarget,"/api/risk-score",{paths:$("paths").value},"riskout");
$("reviewbtn").onclick=e=>run(e.currentTarget,"/api/review",{diff:$("diff").value},"reviewout");
