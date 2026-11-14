// sk06 v2, the full edit (picture only; the sound is mixed in work/sk06/mix.py). Reel time = voice-cut time + 0.12 s.
// Akhilesh's notes on v1 (2026-11-14): one Pandey (every face shot on Wan 3.0, the look after "doosra"); a clean
// zoom-in on his face; the three startup logos stacked over moving B-roll; words behind his head only when they matter
// and readable; company parts cut fast "like a pro editor"; sharp MTAR pictures; the brake: seated passengers jolt
// forward, the camera is thrown back and returns to him as HE says "Ab semiconductors par aaiye"; CG Power and Kaynes
// on their charts; no aisle shot on "Entry ke waqt".
// Talking clips start at c = r - 0.12 - cut_start + 0.5 + shift (the lip check's shift).
import React from "react";
import { AbsoluteFill, Img, Sequence, staticFile, useCurrentFrame } from "remotion";
import charts from "../public/data/charts.json";
import media from "../public/data/media.json";
import {
  Bug, Captions, ChartView, LogoBadge, Clip, Disclaimer, DrawArrow, DrawBox, DrawLine, F, FONTS, Label, LogoCard, Moving, BigWord,
  Montage, Item, KineticDisclaimer, cam, clamp, smooth, punchAt, whip, shake, Dir, Punch, Cap, HW,
} from "./fx";

export const OUT0 = 104.85, OUTC = 0.9;
const GLASS = 1.28, PASS = 0.24;                          // the dive reaches the windscreen pane; the pass through it
export const SLOW_AT = OUT0 + (4.3 - OUTC);             // the top shot plays at half speed from clip 4.3 s
export const TOTAL = Math.round((SLOW_AT + (6.06 - 4.3) / 0.5) * 100) / 100;
const C: any = charts;
const M: any = media;                                    // B-roll lists, filled from footage_in (data/media.json)

type Scene = { a: number; b: number; inDir?: Dir; outDir?: Dir; shakes?: [number, number?, number?][];
  draw: (t: number, mirror: string) => React.ReactNode; over?: (t: number) => React.ReactNode };

const talk = (src: string, a: number, off: number, punches: Punch[] = []) => (t: number) => {
  const p = punchAt(t, punches);
  return <Clip src={src} c0={a - off} s={p.s} cx={p.cx} cy={p.cy} />;
};
const montage = (key: string, a: number, b: number) => (t: number) => <Montage t={t} a={a} b={b} items={M[key] as Item[]} />;
const chartScene = (key: string, keys: { t: number; z: number; cx: number; cy: number }[], marks?: (t: number) => React.ReactNode) => (t: number) => {
  const c = cam(t, keys);
  return <ChartView def={C[key]} z={c.z} cx={c.cx} cy={c.cy}>{marks ? marks(t) : null}</ChartView>;
};
const card = () => <AbsoluteFill style={{ background: "radial-gradient(circle at 50% 45%, #fbfaf6 0%, #e9e6dd 100%)" }} />;

const LOGO: Record<string, string> = { centum: "logos/centum.png", mtar: "logos/mtar_badge.png", cgpower: "logos/cgpower.png", kaynes: "logos/kaynes.png" };
const MC = C.centum.marks, MM = C.mtar.marks, MG = C.cgpower.marks, MK = C.kaynes.marks;

const SCENES: Scene[] = [
  // 0 the opening: dive with LONG-TERM on the roof, through the windscreen, the Wan 3.0 approach to his face, T1w3 from "doosra"
  { a: 0, b: 7.30, outDir: "up", draw: (t) => {
      // the dive to the windscreen; then the camera passes THROUGH the glass: the pane opens from its centre outward
      // while the Wan 3.0 aisle grows in behind it (A1, lips +0.30 s: c = r - 0.62); T1w3 from "doosra"
      if (t >= 5.62) return <Sequence from={F(5.62)} layout="none"><Clip src="T1w3.mp4" c0={3.93} s={1.2} cx={0.509} cy={0.475} /></Sequence>;
      const u = smooth((t - GLASS) / PASS);
      const a1 = t >= GLASS ? <Sequence from={F(GLASS)} layout="none">
          <Clip src="A1_kw.mp4" c0={GLASS - 0.62} s={1.06 - 0.06 * u} cx={0.5} cy={0.45} filter={`blur(${3 * (1 - u)}px)`} />
        </Sequence> : null;
      const r = -10 + 140 * u;
      const dive = t < GLASS + PASS ? <Clip src="S1_wan27_gt.mp4" c0={0} rate={2.5 / 1.6} s={1 + 0.45 * u} cx={0.5} cy={0.45}
          filter={`blur(${4 * u}px)`} mask={t >= GLASS ? `radial-gradient(ellipse 60% 48% at 50% 45%, transparent ${r}%, black ${r + 22}%)` : undefined} /> : null;
      return <>{a1}{dive}</>;
    },
    over: (t) => <BigWord text="SEMICONDUCTORS" small="doosra" t={t} t0={6.36} t1={7.12} y={1050} size={92} /> },
  // 1 "Space mein Agnikul, Skyroot, Pixel jaise naam hain": launches behind, the three logos stacking up on their names
  { a: 7.30, b: 11.95, inDir: "up", outDir: "left", draw: montage("startups", 7.30, 11.95),
    over: (t) => <>
      <LogoCard src="logos/agnikul.png" t={t} t0={8.86} y={390} w={430} h={128} />
      <LogoCard src="logos/skyroot.png" t={t} t0={9.76} y={545} w={430} h={128} />
      <LogoCard src="logos/pixxel.png" t={t} t0={10.70} y={700} w={430} h={128} />
    </>, shakes: [[8.86, 0.22, 7], [9.76, 0.22, 7], [10.70, 0.22, 7]] },
  // 2 T2b "lekin ye startups listed nahi hain, toh ... dekhte hain" (no word behind him: Akhilesh, "listed, unlisted ... really?")
  { a: 11.95, b: 17.60, inDir: "left", draw: talk("T2b.mp4", 11.95, 11.75, [{ t: 15.02, s: 1.18 }]) },
  // 3 "Pehla naam hai, Centum Electronics": fast cuts on the words, NO. 1 slammed, the logo slammed on its name
  { a: 17.60, b: 21.40, draw: montage("centum_intro", 17.60, 21.40),
    over: (t) => <><BigWord text="NO. 1" t={t} t0={18.08} t1={19.50} y={540} size={190} />
      <LogoCard src="logos/centum.png" t={t} t0={19.60} y={560} w={600} h={210} /></>,
    shakes: [[18.08, 0.3, 14], [19.60, 0.3, 14]] },
  // 4 "Ye space applications ke liye electronics banati hai": a cut on every key word
  { a: 21.40, b: 24.62, outDir: "right", draw: montage("centum_desc", 21.40, 24.62) },
  // 5 T3b2 "toh sector mein activity badhne se ... mauke ban sakte hain": punch-in on "business"
  { a: 24.62, b: 29.40, inDir: "right", outDir: "zoom", draw: talk("T3b2.mp4", 24.62, 24.37, [{ t: 27.58, s: 1.2 }]) },
  // 6 the Centum chart (v3: wider capture, the camera goes to the recent bars)
  { a: 29.40, b: 36.85, inDir: "zoom", outDir: "left",
    draw: chartScene("centum", [{ t: 29.4, z: 1, cx: 362, cy: 453 }, { t: 30.4, z: 1, cx: 362, cy: 453 }, { t: 31.0, z: 1.45, cx: 470, cy: 300 }, { t: 33.0, z: 1.45, cx: 470, cy: 300 }, { t: 33.6, z: 1.9, cx: 530, cy: 230 }],
      (t) => <>
        <DrawLine t={t} t0={30.72} x1={MC.sup.x1 - 150} x2={MC.sup.x2} y1={MC.sup.y} color="#d62828" />
        <Label t={t} t0={30.80} x={Math.max(MC.sup.x1 - 150, 356)} y={MC.sup.y + 34} text="Support" size={21} color="#d62828" />
        <DrawLine t={t} t0={31.30} x1={MC.res.x1 - 200} x2={MC.res.x2} y1={MC.res.y} color="#2a5bd7" />
        <Label t={t} t0={31.38} x={MC.res.x1 - 200} y={MC.res.y + 34} text="Resistance" size={21} color="#2a5bd7" />
        <Label t={t} t0={33.30} x={MC.res.x2 - 4} y={MC.res.y - 12} text="Breakout?" anchor="end" size={21} />
        <DrawArrow t={t} t0={34.52} x1={MC.res.x2 - 14} y1={C.centum.lastY - 8} x2={MC.res.x2 - 14} y2={MC.res.y + 12} w={6} />
      </>) },
  // 7 "Doosra naam hai, MTAR Technologies": fast cuts, NO. 2, the logo on its name
  { a: 36.85, b: 40.70, inDir: "left", draw: montage("mtar_intro", 36.85, 40.70),
    over: (t) => <><BigWord text="NO. 2" t={t} t0={37.22} t1={38.66} y={540} size={190} />
      <LogoCard src="logos/mtar.png" t={t} t0={38.74} y={560} w={560} h={360} /></>,
    shakes: [[37.22, 0.3, 14], [38.74, 0.3, 14]] },
  // 8 "Ye space programs ke liye engines aur critical assemblies banati hai"
  { a: 40.70, b: 45.80, outDir: "zoom", draw: montage("mtar_desc", 40.70, 45.80) },
  // 9 the MTAR chart: the run-up, the range, the next breakout
  { a: 45.80, b: 52.55, inDir: "zoom",
    draw: chartScene("mtar", [{ t: 45.8, z: 1, cx: 362, cy: 453 }, { t: 47.4, z: 1, cx: 362, cy: 453 }, { t: 47.9, z: 1.4, cx: 470, cy: 340 }, { t: 51.3, z: 1.4, cx: 470, cy: 340 }, { t: 51.9, z: 1.85, cx: 540, cy: 250 }],
      (t) => <>
        <DrawArrow t={t} t0={47.78} x1={MM.run.x1 - 8} y1={MM.run.y1 + 18} x2={MM.run.x2 - 14} y2={MM.run.y2 + 20} w={7} />
        <Label t={t} t0={47.95} t1={51.2} x={MM.run.x1 - 18} y={(MM.run.y1 + MM.run.y2) / 2 + 30} text="Run-up" anchor="end" size={21} />
        <DrawBox t={t} t0={48.52} x1={MM.box.x1} x2={MM.box.x2} y1={MM.box.y1} y2={MM.box.y2} />
        <Label t={t} t0={50.50} x={(MM.box.x1 + MM.box.x2) / 2} y={MM.box.y2 + 34} text="Range" anchor="middle" size={21} />
        <Label t={t} t0={51.74} x={MM.box.x2 - 4} y={MM.box.y1 - 10} text="Breakout?" anchor="end" size={21} />
      </>) },
  // 10 the brake (hard cut on the sound): the camera is thrown back, the seated passengers lurch, he stays put, the
  //    camera returns and HE says "Ab semiconductors par aaiye"
  { a: 52.55, b: 55.92, outDir: "right", shakes: [[52.57, 0.45, 16]], draw: (t) => t < 54.12
      ? <Clip src="B1b.mp4" c0={0.2} rate={2.0 / (54.12 - 52.55)} />         // the jolt, a little faster (no words here)
      : <Sequence from={F(54.12 - 52.55)} layout="none"><Clip src="B1b.mp4" c0={54.12 - 51.92} /></Sequence>,
    over: (t) => <BigWord text="SEMICONDUCTORS" t={t} t0={54.48} t1={55.36} y={1050} size={92} /> },
  // 11 "India mein chips banane aur unki packaging aur testing ke naye plants lag rahe hain": a cut on every key word
  { a: 55.92, b: 61.20, inDir: "right", draw: montage("semis", 55.92, 61.20) },
  // 12 T5b "lekin yahan bhi kai bade naam unlisted hain"
  { a: 61.20, b: 64.55, draw: talk("T5b.mp4", 61.20, 60.81) },
  // 13 T5c (Wan 3.0) "phir bhi kuch listed companies aapki watchlist mein honi chahiye"
  { a: 64.55, b: 68.75, draw: talk("T5c4.mp4", 64.55, 64.23) },
  // 14 "Pehla naam hai, CG Power": NO. 1, the logo slammed on its name
  { a: 68.75, b: 71.25, outDir: "left", draw: card,
    over: (t) => <><BigWord text="NO. 1" t={t} t0={68.94} t1={70.44} y={560} size={190} />
      <LogoCard src="logos/cgpower.png" t={t} t0={70.50} y={560} w={620} h={160} /></>,
    shakes: [[68.94, 0.3, 14], [70.50, 0.3, 14]] },
  // 15 "Iski CG Semi chip assembly, packaging aur testing mein kaam karti hai": the CG Power chart, its levels marked
  { a: 71.25, b: 77.25, inDir: "left", draw: chartScene("cgpower", [{ t: 71.25, z: 1, cx: 362, cy: 453 }, { t: 72.3, z: 1, cx: 362, cy: 453 }, { t: 73.0, z: 1.45, cx: 470, cy: 270 }, { t: 75.4, z: 1.45, cx: 470, cy: 270 }, { t: 76.2, z: 1.8, cx: 540, cy: 300 }],
      (t) => <>
        <DrawLine t={t} t0={73.76} x1={MG.res.x1 - 150} x2={MG.res.x2} y1={MG.res.y} color="#2a5bd7" />
        <Label t={t} t0={73.84} x={MG.res.x1 - 150} y={MG.res.y + 34} text="Resistance" size={21} color="#2a5bd7" />
        <DrawLine t={t} t0={74.72} x1={MG.sup.x1 - 260} x2={MG.sup.x2} y1={MG.sup.y} color="#d62828" />
        <Label t={t} t0={74.80} x={MG.sup.x1 - 260} y={MG.sup.y + 34} text="Support" size={21} color="#d62828" />
      </>),
    over: (t) => <LogoCard src="logos/cgsemi.png" t={t} t0={72.58} y={190} x={600} w={170} h={200} /> },
  // 16 "Phir aati hai, Kaynes Technology": NO. 2, the logo on its name
  { a: 77.25, b: 80.30, draw: card,
    over: (t) => <><BigWord text="NO. 2" t={t} t0={77.30} t1={78.62} y={560} size={190} />
      <LogoCard src="logos/kaynes.png" t={t} t0={78.70} y={560} w={560} h={150} /></>,
    shakes: [[77.38, 0.3, 14], [78.70, 0.3, 14]] },
  // 17 "Iski Kaynes Semicon bhi semiconductor packaging aur testing mein kaam karti hai": the Kaynes chart, its range marked
  { a: 80.30, b: 85.30, outDir: "right", draw: chartScene("kaynes", [{ t: 80.3, z: 1, cx: 362, cy: 453 }, { t: 81.3, z: 1, cx: 362, cy: 453 }, { t: 82.0, z: 1.5, cx: 480, cy: 650 }, { t: 84.2, z: 1.5, cx: 480, cy: 650 }, { t: 85.0, z: 1.75, cx: 540, cy: 680 }],
      (t) => <>
        <DrawLine t={t} t0={82.16} x1={MK.res.x1 - 150} x2={MK.res.x2} y1={MK.res.y} color="#2a5bd7" />
        <Label t={t} t0={82.24} x={MK.res.x1 - 150} y={MK.res.y - 12} text="Resistance" size={21} color="#2a5bd7" />
        <DrawLine t={t} t0={82.94} x1={MK.sup.x1 - 60} x2={MK.sup.x2} y1={MK.sup.y} color="#d62828" />
        <Label t={t} t0={83.02} x={MK.sup.x1 - 60} y={MK.sup.y + 34} text="Support" size={21} color="#d62828" />
      </>),
    over: (t) => <LogoCard src="logos/kaynessemicon.png" t={t} t0={80.80} y={190} w={420} h={120} /> },
  // 18 T7b (Wan 3.0) "toh chip industry ko samajhte waqt ... radar par hone chahiye": punch-in on "ye businesses"
  { a: 85.30, b: 91.90, inDir: "right", outDir: "zoom", draw: talk("T7b3.mp4", 85.30, 85.00, [{ t: 88.92, s: 1.18 }]) },
  // 19 "Ab ye chaaron companies ke charts ko technically evaluate kijiye": the four charts, then all four
  { a: 91.90, b: 96.65, inDir: "zoom", draw: (t) => {
      const seq: [number, string][] = [[91.90, "centum"], [92.90, "mtar"], [93.58, "cgpower"], [94.22, "kaynes"]];
      if (t < 94.98) {
        let k = "centum", s0 = 91.90; for (const [s, n] of seq) if (t >= s) { k = n; s0 = s; }
        const pz = 1 + 0.06 * (1 - clamp((t - s0) / 0.14));
        return <AbsoluteFill style={{ transform: `scale(${pz})` }}><ChartView def={C[k]} z={1.3} cx={470} cy={453} />
          <LogoBadge src={LOGO[k]} x={34} y={196} w={290} h={100} t={t} t0={s0} /></AbsoluteFill>;
      }
      const u = clamp((t - 94.98) / 0.25);
      return (
        <AbsoluteFill style={{ background: "#fff" }}>
          {["centum", "mtar", "cgpower", "kaynes"].map((n, i) => (
            <div key={n} style={{ position: "absolute", left: (i % 2) * 360 + 4, top: 150 + Math.floor(i / 2) * 520, width: 352, height: 510, overflow: "hidden",
              border: "2px solid #e6e6e6", transform: `scale(${0.92 + 0.08 * u})`, opacity: clamp(u * 1.6 - i * 0.15) }}>
              <Img src={staticFile(C[n].img)} style={{ position: "absolute", left: 0, top: 0, width: 352, height: 352 * C[n].h / C[n].w }} />
              <LogoBadge src={LOGO[n]} x={14} y={46} w={196} h={68} />
            </div>))}
        </AbsoluteFill>);
    } },
  // 20 T8a "kyunki sirf achha stock aur achha sector dekhkar baat poori nahi hoti": punch-in on "baat"
  { a: 96.65, b: 101.80, draw: talk("T8a.mp4", 96.65, 96.40, [{ t: 100.26, s: 1.18 }]) },
  // 21 T8b (Wan 3.0) "Entry ke waqt, chart ka setup bhi dekhiye": the whole line on his face, SETUP behind his head
  { a: 101.80, b: OUT0, draw: talk("T8b3_kw.mp4", 101.80, 101.52) },
  // 22 the outro brake: thrown back, out through the windscreen, up to the top shot (= frame 1)
  { a: OUT0, b: TOTAL, shakes: [[OUT0 + 0.05, 0.55, 16]], draw: (t) => t < SLOW_AT ? <Clip src="S3_outro_gt.mp4" c0={OUTC} />
      : <Sequence from={F(SLOW_AT - OUT0)} layout="none"><Clip src="S3_outro_gt.mp4" c0={4.3} rate={0.5} /></Sequence> },
];

// captions: Roman Hinglish, phrase by phrase, on the words; none on the full-screen marked charts
const CAPS: Cap[] = [
  { t0: 0.22, t1: 1.95, text: "Long-term investing karte hain?" },
  { t0: 2.16, t1: 4.55, text: "Ye do sectors ko ignore mat kijiye.", hi: "ignore mat kijiye" },
  { t0: 12.20, t1: 14.95, text: "Lekin ye startups listed nahi hain,", hi: "listed nahi" },
  { t0: 15.00, t1: 16.12, text: "toh space se judi" },
  { t0: 16.14, t1: 17.60, text: "listed companies dekhte hain.", hi: "listed companies" },
  { t0: 21.42, t1: 23.14, text: "Ye space applications ke liye", hi: "space applications" },
  { t0: 23.16, t1: 24.70, text: "electronics banati hai,", hi: "electronics" },
  { t0: 24.74, t1: 27.02, text: "toh sector mein activity badhne se", hi: "activity" },
  { t0: 27.04, t1: 29.40, text: "iske liye business ke mauke ban sakte hain.", hi: "business ke mauke" },
  { t0: 41.14, t1: 43.06, text: "Ye space programs ke liye", hi: "space programs" },
  { t0: 43.08, t1: 45.80, text: "engines aur critical assemblies banati hai.", hi: "engines" },
  { t0: 54.10, t1: 54.46, text: "Ab..." },
  { t0: 55.38, t1: 55.92, text: "par aaiye." },
  { t0: 56.34, t1: 57.96, text: "India mein chips banane aur", hi: "chips" },
  { t0: 57.98, t1: 59.70, text: "unki packaging aur testing ke", hi: "packaging aur testing" },
  { t0: 59.72, t1: 61.20, text: "naye plants lag rahe hain.", hi: "naye plants" },
  { t0: 61.32, t1: 63.40, text: "Lekin yahan bhi kai bade naam" },
  { t0: 63.42, t1: 64.55, text: "unlisted hain.", hi: "unlisted" },
  { t0: 64.66, t1: 66.78, text: "Phir bhi kuch listed companies", hi: "listed companies" },
  { t0: 66.80, t1: 68.75, text: "aapki watchlist mein honi chahiye.", hi: "watchlist" },
  { t0: 85.42, t1: 87.50, text: "Toh chip industry ko samajhte waqt", hi: "chip industry" },
  { t0: 87.52, t1: 88.88, text: "chips banane ke saath" },
  { t0: 88.90, t1: 90.04, text: "ye businesses bhi", hi: "businesses" },
  { t0: 90.06, t1: 91.90, text: "aapke radar par hone chahiye.", hi: "radar" },
  { t0: 96.82, t1: 98.44, text: "kyunki sirf achha stock", hi: "achha stock" },
  { t0: 98.46, t1: 100.22, text: "aur achha sector dekhkar", hi: "achha sector" },
  { t0: 100.24, t1: 101.80, text: "baat poori nahi hoti." },
  { t0: 102.04, t1: 103.18, text: "Entry ke waqt,", hi: "Entry" },
];

const SceneLayer: React.FC<{ s: Scene }> = ({ s }) => {
  const t = s.a + useCurrentFrame() / 30;
  let w = { dx: 0, dy: 0, blur: 0, z: 1, o: 1 };
  if (s.inDir && s.inDir !== "none" && t < s.a + HW) w = whip(t, s.a, s.inDir, "in");
  if (s.outDir && s.outDir !== "none" && t > s.b - HW) w = whip(t, s.b, s.outDir, "out");
  let sx = 0, sy = 0, sr = 0;
  for (const [t0, dur, amp] of s.shakes ?? []) { const k = shake(t, t0, dur ?? 0.35, amp ?? 12); sx += k.x; sy += k.y; sr += k.r; }
  const sc = sx || sy ? 1.05 : 1;
  return (
    <AbsoluteFill style={{ transform: `translate(${sx}px, ${sy}px) rotate(${sr}deg) scale(${sc})` }}>
      <Moving dx={w.dx} dy={w.dy} blur={w.blur} z={w.z}>{(m) => <>{s.draw(t, m)}{s.over && !m && s.over(t)}</>}</Moving>
    </AbsoluteFill>
  );
};

export const Reel: React.FC = () => {
  const t = useCurrentFrame() / 30;
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <FONTS />
      {SCENES.map((s, i) => (
        <Sequence key={i} from={F(s.a)} durationInFrames={F(s.b) - F(s.a)}><SceneLayer s={s} /></Sequence>
      ))}
      <Captions t={t} caps={CAPS} />
      <KineticDisclaimer t={t} t0={SLOW_AT - 0.7} t1={TOTAL - 0.12} />
      <Bug />
    </AbsoluteFill>
  );
};
