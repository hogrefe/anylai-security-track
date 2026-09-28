import hashlib,json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(1048576),b''): h.update(c)
 return h.hexdigest()
def verify():
 m=ROOT/'release-manifest.json'; side=ROOT/'release-manifest.sha256'
 if not side.read_text().strip().split()[0]==digest(m): raise SystemExit('manifest sidecar mismatch')
 data=json.loads(m.read_text()); files=data['files']; paths=[x['path'] for x in files]
 if len(paths)!=len(set(paths)): raise SystemExit('duplicate manifest path')
 actual=sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.name not in {'release-manifest.json','release-manifest.sha256'})
 if sorted(paths)!=actual: raise SystemExit('inventory mismatch')
 for e in files:
  if len(e.get('sha256',''))!=64 or digest(ROOT/e['path'])!=e['sha256']: raise SystemExit('content hash mismatch: '+e['path'])
 return data
def main():
 data=verify(); out=Path(os.environ.get('RC7_OUTPUT_DIR',str(ROOT.parent/'rc7-output'))); out.mkdir(parents=True,exist_ok=True)
 r=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-q'],cwd=ROOT,text=True,capture_output=True)
 (out/'tests.log').write_text(r.stdout+r.stderr)
 if r.returncode: raise SystemExit(r.returncode)
 from security_assessment.runner import write_s1_artifact
 artifact=write_s1_artifact(out)
 result={'rc':'SECURITY-S14-RC7-CANDIDATE','python':sys.version.split()[0],'tests':'PASS','artifact':artifact.name,'artifact_sha256':digest(artifact),'s8_s10':'historical context only; not reproduced or verified by this package'}
 (out/'reproduction-output.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__': main()
