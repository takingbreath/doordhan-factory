"""Run lipsync_lag on every E5 talking clip (own audio) and on each talking segment of the v1 and v4 finals."""
import json, subprocess, sys, os
R='/home/user/doordhan-factory'; V=f'{R}/work/sk01/vid'
jobs=[]
for n in range(1,7):
    jobs.append((f'E5 v1 T{n} (own audio)', f'{V}/T{n}.mp4', None, None, None))
jobs.append(('E5 T1b expression test (own audio)', f'{V}/T1b.mp4', None, None, None))
for n in range(1,7):
    jobs.append((f'E5 v2 T{n} (own audio)', f'{V}/T{n}v2.mp4', None, None, None))
# finals: talking segments [S-0.12, next S-0.12]
v1 = {'P1':9.40,'P2':15.50,'P3':25.45,'P4':36.00,'P5':47.55,'P6':54.50}; v1_end=54.50+4.40+0.05
ns={}; exec(open(f'{R}/work/sk01/build.py').read().split('if __name__')[0], ns)
v4 = {k: ns['S'][k] for k in ['P1','P2','P3','P4','P5','P6']}; v4_end=ns['P6_END']
for tag, T, end, f in [('v1', v1, v1_end, f'{R}/outputs/sk01/sk01_top1pct_v1.mp4'), ('v4', v4, v4_end, f'{R}/outputs/sk01/sk01_top1pct_v4.mp4')]:
    keys=list(T)
    for i,k in enumerate(keys):
        a=T[k]-0.12; b=(T[keys[i+1]]-0.12) if i+1<len(keys) else end
        jobs.append((f'E5 final {tag} {k} segment', f, None, a, b))
import glob
for f in sorted(glob.glob(f'{R}/work/lag/clips/*.mp4')):
    ep=os.path.basename(f).split('_')[0]
    jobs.append((f'{ep} {os.path.basename(f)[:-4]} (own audio)', f, None, None, None))
out=[]
for label, clip, audio, a, b in jobs:
    js=f'/tmp/claude-0/lag_{len(out)}.json'
    cmd=['python3',f'{R}/pipeline/lipsync_lag.py',clip,'--label',label,'--json',js]
    if a is not None: cmd += ['--start',f'{a:.2f}','--end',f'{b:.2f}']
    r=subprocess.run(cmd,capture_output=True,text=True)
    lines=[l for l in r.stdout.splitlines()]
    print('\n'.join(lines),flush=True)
    if os.path.exists(js): out.append(json.load(open(js)))
    else: print('ERROR', label, r.stderr[-500:])
json.dump(out,open(f'{R}/work/lag/all_results.json','w'),indent=1)
