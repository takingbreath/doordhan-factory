#!/bin/zsh
# render every Remotion scene to ../gfx6/<name>.mp4 (720 wide, h264, crf 16)
cd "$(dirname "$0")"
render() { n=$1; id=$2; npx remotion render src/index.ts $id ../gfx6/$n.mp4 --codec h264 --crf 16 --concurrency 3 > /tmp/rm_render_$n.log 2>&1 && echo "done $n" || echo "FAILED $n"; }
typeset -A M; M=(hook Hook chart Chart gst Gst cert Cert pass Pass hack Hack rob Rob quar Quar audit Audit unaff Unaff trust Trust digi Digi rev Rev cred Cred)
for n in ${(k)M}; do echo "$n ${M[$n]}"; done | xargs -P 3 -L 1 zsh -c 'cd '"$PWD"'; n=$0; id=$1; npx remotion render src/index.ts $id ../gfx6/$n.mp4 --codec h264 --crf 16 --concurrency 3 > /tmp/rm_render_$n.log 2>&1 && echo "done $n" || echo "FAILED $n"'
