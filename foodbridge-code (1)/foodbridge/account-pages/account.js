(()=>{const out=document.getElementById("out"),h=location.hash.slice(1),[k,v]=h.split("="),post=async(p,b)=>{const r=await fetch(p,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(b)});const d=await r.json().catch(()=>({}));if(!r.ok)throw new Error(typeof d.detail==="string"?d.detail:"Request failed");return d};
const say=(c,t)=>{out.textContent="";const d=document.createElement("div");d.className=c;d.textContent=t;out.append(d)};
if(k==="verify"&&v)post("/api/auth/verify",{token:v}).then(d=>say("ok",d.message),e=>say("err",e.message));
else if(k==="reset"&&v){out.innerHTML='<form><label>New password (12+ characters)</label><input id="a" type="password" minlength="12" required><label>Confirm</label><input id="b" type="password" required><button>Reset password</button></form>';
 out.querySelector("form").onsubmit=e=>{e.preventDefault();post("/api/auth/reset-password",{token:v,password:a.value,confirmation:b.value}).then(d=>say("ok",d.message),x=>say("err",x.message))}}
else say("err","This link is incomplete. Request a new one from the sign-in page.")})();
