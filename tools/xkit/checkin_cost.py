#!/usr/bin/env python3
"""Usage of one check-in window in this session's transcript.
Usage: python3 -I checkin_cost.py START END   (ISO UTC, e.g. 2026-11-12T02:10:00Z 2026-11-12T02:40:00Z)
Counts API steps in the window and their weighted tokens
(input 1x, cache write 2x, cache read 0.1x, output 5x), split by what each step used."""
import json, sys, glob, os, collections
start, end = sys.argv[1], sys.argv[2]
base = os.path.expanduser('~/.claude/projects') if os.path.isdir(os.path.expanduser('~/.claude/projects')) else '/root/.claude/projects'
files = sorted(glob.glob(base + '/*/*.jsonl'), key=os.path.getmtime)
f = files[-1]
W = dict(i=1.0, cw=2.0, cr=0.1, o=5.0)
calls = collections.OrderedDict()
for line in open(f):
    try: o = json.loads(line)
    except Exception: continue
    if o.get('type') != 'assistant': continue
    ts = o.get('timestamp', '')
    if not (start <= ts <= end): continue
    m = o['message']; mid = m.get('id')
    c = calls.setdefault(mid, {'u': {}, 'tools': []})
    c['u'] = m.get('usage') or c['u']
    for b in m.get('content', []):
        if b.get('type') == 'tool_use':
            n = b['name']; s = json.dumps(b.get('input', {}))
            if n.startswith('mcp__remote-devices__Claude_Browser__'):
                g = 'browser: 2nd Buffer' if ('"seed"' in s or 'publish.buffer.com' in s) else 'browser: other'
            elif n.startswith('mcp__Buffer__'): g = 'Buffer connector'
            elif n in ('Bash', 'Read', 'Write', 'Edit', 'Grep', 'Glob'): g = 'files & commands'
            elif n == 'Projects': g = 'project docs'
            else: g = 'other'
            c['tools'].append(g)
def eff(u): return u.get('input_tokens',0)*W['i'] + u.get('cache_creation_input_tokens',0)*W['cw'] + u.get('cache_read_input_tokens',0)*W['cr'] + u.get('output_tokens',0)*W['o']
tot = collections.Counter(); steps = collections.Counter(); ctx = []
for c in calls.values():
    e = eff(c['u']); g = c['tools'] or ['reply/thinking']
    for x in g: tot[x] += e/len(g); steps[x] += 1/len(g)
    u = c['u']; ctx.append(u.get('input_tokens',0)+u.get('cache_creation_input_tokens',0)+u.get('cache_read_input_tokens',0))
T = sum(tot.values())
print(f"window {start} → {end}: {len(calls)} steps, {T/1e3:.0f}K weighted tokens, avg {T/max(len(calls),1)/1e3:.1f}K/step, context {min(ctx or [0])//1000}–{max(ctx or [0])//1000}K")
for g, v in tot.most_common(): print(f"  {g:22s} {steps[g]:5.1f} steps  {v/1e3:7.0f}K")
