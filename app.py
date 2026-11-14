#!/usr/bin/env python3
import argparse,html,re
from pathlib import Path
CSS="body{margin:0;background:#10131d;color:#edf1ff;font:20px system-ui;display:grid;place-items:center;min-height:100vh}.deck{width:92vw;height:85vh;background:linear-gradient(140deg,#27334b,#171c2a);border:1px solid #46536e;border-radius:20px;position:relative;overflow:hidden}.slide{display:none;padding:7vw;height:75%;overflow:auto}.slide.active{display:block}h1{font-size:clamp(2.5rem,7vw,5rem)}h2{font-size:clamp(2rem,5vw,3.5rem)}li{margin:12px}strong{color:#a6e3a1}.foot{position:absolute;bottom:0;left:0;right:0;padding:12px;background:#10131ddd;display:flex;gap:12px}button{padding:8px 15px;background:#303b54;color:white;border:1px solid #65738e;border-radius:8px}progress{flex:1}"
JS="let s=[...document.querySelectorAll('.slide')],i=0;function go(n){i=Math.max(0,Math.min(s.length-1,n));s.forEach((x,j)=>x.classList.toggle('active',i===j));document.querySelector('progress').value=i+1;document.querySelector('#count').textContent=(i+1)+' / '+s.length}function next(){go(i+1)}function prev(){go(i-1)}document.onkeydown=e=>{if(['ArrowRight',' ','PageDown'].includes(e.key))next();if(['ArrowLeft','PageUp'].includes(e.key))prev()};document.querySelector('#full').onclick=()=>document.querySelector('.deck').requestFullscreen?.();go(0)"
def render(src):
 out=[]
 for line in src.strip().splitlines():
  x=line.strip()
  if not x:continue
  if x.startswith("#"):
   m=re.match("^("+ "#" + "{1,3}) +(.*)",x)
   if m:out.append("<h%d>%s</h%d>"%(len(m[1]),html.escape(m[2]),len(m[1])))
  elif x.startswith("- "):out.append("<li>"+html.escape(x[2:])+"</li>")
  else:out.append("<p>"+html.escape(x)+"</p>")
 return "".join(out)
def main():
 p=argparse.ArgumentParser();p.add_argument("input",nargs="?");p.add_argument("-o","--output",default="presentation.html");p.add_argument("--example",action="store_true");a=p.parse_args()
 sample="# Welcome\\nMarkdown to slides\\n\\n---\\n\\n## Workflow\\n- Write Markdown\\n- Separate slides with dashes\\n\\n---\\n\\n# Questions?"
 if not a.input and not a.example:p.error("provide a Markdown file or --example")
 src=sample if a.example else Path(a.input).read_text(encoding="utf-8")
 parts=re.split("(?m)^ *--- *$",src.strip())
 slides="".join('<section class="slide"><small>SLIDE %02d</small>%s</section>'%(i+1,render(v)) for i,v in enumerate(parts))
 page='<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Decksmith</title><style>'+CSS+'</style><main class="deck">'+slides+'<nav class="foot"><button onclick="prev()">←</button><button onclick="next()">→</button><span id="count"></span><progress max="%d" value="1"></progress><button id="full">Fullscreen</button></nav></main><script>'+JS+'</script>'%len(parts)
 Path(a.output).write_text(page,encoding="utf-8");print("Created",a.output)
if __name__=="__main__":main()
