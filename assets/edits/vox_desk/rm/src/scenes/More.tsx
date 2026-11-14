// sk05 v8 scenes, chosen from the script (work/sk05/storyboard_v7.md). Every event starts on its word (wt()).
// SAFE AREA (Instagram): everything that matters sits inside x 40..640 and y 170..855 of the 720x1280 frame. The right strip (action buttons), the top 170 px (header)
// and the bottom 225 px (caption, audio) are covered by the app; the burned captions live at y 860..1020.
import React from "react";
import { Img, staticFile } from "remotion";
import { C, FONT, Gate, easeBack, easeOut, prog, useV, wt } from "../lib/core";
import { BrowserWin, CalPage, Clipping, Crack, Cutout, LogoTag, PathMark, Print, Scribble, Seal, StampText, TapeLabel, Tick, Underline } from "../lib/marks";
import { Form, Stage, TickerCard, Track } from "../lib/widgets";

// ---------------------------------------------------------------- hook (top half 720x640, v -0.15 .. 3.05)
export const HOOK = [-0.15, 3.05] as const;
export const Hook: React.FC = () => {
  const tK = wt("कांड");
  return (
    <Stage v0={HOOK[0]} dy={-40}>
      <LogoTag x={340} y={250} w={440} t0={-1} rot={-2} />
      <Cutout src="img/v/padlock.png" x={150} y={470} w={180} rot={5} t0={-1} pop={false} />
      <TickerCard x={450} y={470} tIn={tK} tA={-5} tB={-5} tPct={tK} tGir={tK + 0.7} k={0.55} rot={-3} />
    </Stage>
  );
};

// ---------------------------------------------------------------- GST (v0 7.95)
export const GST = [7.95, 14.55] as const;
export const Gst: React.FC = () => {
  const tG = wt("GST"), tI = wt("income"), tX = wt("import-export"), tE = wt("E-Mudhra", 11.42), tD = wt("digital", 12.18), tS = wt("signature", 12.62), tC = wt("certificates", 13.06), tU = wt("use"), tH = wt("होते"), tN = wt("हैं", 14.08);
  const s1: [number, number] = [220, 505], s2: [number, number] = [500, 565], s3: [number, number] = [355, 775];
  return (
    <Stage v0={GST[0]} cam={[{ t: GST[0], z: 1, cx: 340, cy: 512 }, { t: GST[1], z: 1.04, cx: 340, cy: 512 }]}>
      <Form lines={["GST"]} x={165} y={410} w={250} rot={-5} t0={tG} />
      <Form lines={["INCOME", "TAX"]} x={445} y={470} w={250} rot={4} t0={tI} />
      <Form lines={["IMPORT-", "EXPORT"]} x={300} y={680} w={250} rot={-3} t0={tX} />
      <LogoTag x={340} y={230} w={360} t0={tE} rot={-3} />
      <Seal x={s1[0]} y={s1[1]} d={130} t0={tD + 0.06} /><Seal x={s2[0]} y={s2[1]} d={130} t0={tS + 0.06} /><Seal x={s3[0]} y={s3[1]} d={130} t0={tC + 0.06} />
      <Track keys={[
        { t: tD - 0.45, x: 300, y: 150, rot: -25, s: 1.3, a: 0 }, { t: tD - 0.02, x: s1[0], y: s1[1] - 40, rot: -18, s: 1.1, a: 1 }, { t: tD + 0.06, x: s1[0], y: s1[1], rot: -18, s: 1.0 }, { t: tD + 0.16, x: s1[0], y: s1[1] - 40, rot: -18, s: 1.1 },
        { t: tS - 0.02, x: s2[0], y: s2[1] - 40, rot: 12, s: 1.1 }, { t: tS + 0.06, x: s2[0], y: s2[1], rot: 12, s: 1.0 }, { t: tS + 0.16, x: s2[0], y: s2[1] - 40, rot: 12, s: 1.1 },
        { t: tC - 0.02, x: s3[0], y: s3[1] - 40, rot: -10, s: 1.1 }, { t: tC + 0.06, x: s3[0], y: s3[1], rot: -10, s: 1.0 }, { t: tC + 0.18, x: s3[0], y: s3[1] - 40, rot: -10, s: 1.1 }, { t: tU + 0.35, x: s3[0] + 160, y: s3[1] - 120, rot: -10, s: 1.1, a: 0 },
      ]}><Cutout src="img/v/token.png" x={0} y={0} w={210} rot={0} t0={tD - 0.5} pop={false} rim={4} /></Track>
      <Scribble cx={s1[0]} cy={s1[1]} rx={82} ry={78} t0={tU} dur={0.35} color="#e6dc2a" width={13} seed={21} />
      <Scribble cx={s2[0]} cy={s2[1]} rx={82} ry={78} t0={tH} dur={0.35} color="#e6dc2a" width={13} seed={22} />
      <Scribble cx={s3[0]} cy={s3[1]} rx={82} ry={78} t0={tN} dur={0.35} color="#e6dc2a" width={13} seed={23} />
    </Stage>
  );
};

// ---------------------------------------------------------------- certificate (v0 15.75)
export const CERT = [15.75, 23.6] as const;
export const Cert: React.FC = () => {
  const tWeb = wt("website", 16.44), tReal = wt("असली", 17.04), tCert = wt("certificate", 18.38), tDeti = wt("देती"), tAnd = wt("और", 19.84), tPad = wt("certificate", 20.0), tCtl = wt("control"), tSirf = wt("सिर्फ", 21.86), tComp = wt("company", 22.18);
  return (
    <Stage v0={CERT[0]} cam={[{ t: CERT[0], z: 1, cx: 340, cy: 512 }, { t: tReal, z: 1, cx: 340, cy: 512 }, { t: tReal + 0.55, z: 2.1, cx: 262, cy: 250 }, { t: tCert + 0.25, z: 2.1, cx: 262, cy: 250 }, { t: tCert + 0.7, z: 1, cx: 340, cy: 512 }]}>
      <BrowserWin x={340} y={400} w={520} rot={-1.5} t0={tWeb} okAt={tCert} lock="bad" tOut={tAnd - 0.05} />
      <Seal x={440} y={470} d={140} t0={tDeti + 0.04} rot={-8} />
      <Cutout src="img/v/padlock.png" x={340} y={520} w={300} rot={-2} t0={tPad} />
      <Track keys={[
        { t: tCtl, x: 640, y: 200, rot: -30, s: 1.1, a: 0 }, { t: tCtl + 0.2, x: 560, y: 290, rot: -35, s: 1.1, a: 1 }, { t: tSirf, x: 430, y: 430, rot: -70, s: 1.05 }, { t: tSirf + 0.5, x: 340, y: 509, rot: -90, s: 1.0 },
      ]}><Cutout src="img/v/key.png" x={0} y={0} w={240} rot={0} t0={tCtl - 0.1} pop={false} rim={4} /></Track>
      <LogoTag x={480} y={330} w={210} t0={tSirf + 0.3} rot={10} />
      <Scribble cx={480} cy={330} rx={130} ry={56} t0={tComp} dur={0.4} color="#6a5acd" width={7} seed={31} />
    </Stage>
  );
};

// ---------------------------------------------------------------- hacker (v0 30.05 .. 35.40; the edit cuts to Billu between 31.00 and 32.35)
export const HACK = [30.05, 35.4] as const;
export const Hack: React.FC = () => {
  const tH = wt("hacker"), tNak = wt("नकली", 30.78), tStamp = 32.4, tWeb = wt("website", 32.76), tAs = wt("असली", 33.56), tSak = wt("सकता");
  return (
    <Stage v0={HACK[0]} cam={[{ t: HACK[0], z: 1, cx: 340, cy: 512 }, { t: HACK[1], z: 1.05, cx: 340, cy: 512 }]}>
      <Track keys={[{ t: tH, x: -200, y: 650, a: 0 }, { t: tH + 0.45, x: 190, y: 640, a: 1 }]}><Cutout src="img/v/hacker.png" x={0} y={0} w={380} t0={tH - 0.1} pop={false} /></Track>
      <Cutout src="img/v/certificate.png" x={410} y={300} w={340} rot={4} t0={tNak} />
      <Seal x={450} y={338} d={120} t0={tStamp + 0.06} />
      <Track keys={[{ t: tStamp - 0.45, x: 520, y: 90, rot: 8, s: 1.1, a: 0 }, { t: tStamp - 0.15, x: 470, y: 215, rot: 4, s: 1.1, a: 1 }, { t: tStamp + 0.06, x: 455, y: 262, rot: 2, s: 1.0 }, { t: tStamp + 0.26, x: 500, y: 150, rot: 8, s: 1.1 }, { t: tStamp + 0.5, x: 560, y: 40, rot: 8, a: 0 }]}>
        <Cutout src="img/v/stamp.png" x={0} y={0} w={170} t0={tStamp - 0.5} pop={false} rim={4} />
      </Track>
      <BrowserWin x={440} y={570} w={300} rot={2} t0={tWeb} lock="bad" okAt={tAs} xAt={tSak} url="emudhra.com" />
      <Tick cx={565} cy={480} s={28} t0={tAs + 0.1} />
    </Stage>
  );
};

// ---------------------------------------------------------------- Rob (v0 35.40)
export const ROB = [35.4, 39.3] as const;
export const Rob: React.FC = () => {
  const tR = wt("Rob"), tEm = wt("email", 36.32), tK = wt("कब"), tB = wt("बताई");
  return (
    <Stage v0={ROB[0]} cam={[{ t: ROB[0], z: 1, cx: 340, cy: 512 }, { t: ROB[1], z: 1.05, cx: 340, cy: 512 }]}>
      <Cutout src="img/v/rob.png" x={250} y={470} w={380} rot={-3} t0={tR} offsetColor="#efe22e" />
      <Track keys={[{ t: tEm, x: 290, y: 650, rot: -8, s: 0.6, a: 0 }, { t: tEm + 0.12, x: 320, y: 630, rot: -8, s: 0.8, a: 1 }, { t: tEm + 0.95, x: 560, y: 360, rot: 22, s: 0.9, a: 1 }, { t: tEm + 1.25, x: 600, y: 330, rot: 24, s: 0.9, a: 0 }]}>
        <Cutout src="img/v/envelope.png" x={0} y={0} w={220} t0={tEm - 0.1} pop={false} rim={4} />
      </Track>
      <CalPage x={480} y={690} w={200} rot={4} t0={tK} top="" big="?" />
      <Underline x1={380} x2={580} y={810} t0={tB} color="#e6dc2a" width={13} />
    </Stage>
  );
};

// ---------------------------------------------------------------- email quarantined (v0 42.95)
export const QUAR = [42.95, 51.8] as const;
export const Quar: React.FC = () => {
  const tBo = wt("बोली"), tEm = wt("email", 45.04), tHo = wt("हो", 45.7), tGai = wt("गई", 45.84), tFu = wt("Follow-up"), tAc = wt("action"), tSe = wt("security", 49.28), tPr = wt("problem");
  return (
    <Stage v0={QUAR[0]} cam={[{ t: QUAR[0], z: 1, cx: 340, cy: 512 }, { t: QUAR[1], z: 1.04, cx: 340, cy: 512 }]}>
      <LogoTag x={200} y={225} w={300} t0={wt("E-Mudhra", 43.76)} rot={-4} />
      <Cutout src="img/v/drawer.png" x={440} y={400} w={400} rot={2} t0={tBo} />
      <Track keys={[{ t: tEm, x: 70, y: 470, rot: -10, s: 1, a: 0 }, { t: tEm + 0.1, x: 100, y: 460, rot: -10, s: 1, a: 1 }, { t: tHo - 0.1, x: 360, y: 320, rot: 6, s: 0.95 }, { t: tHo + 0.2, x: 380, y: 390, rot: 8, s: 0.5, a: 0 }]}>
        <Cutout src="img/v/envelope.png" x={0} y={0} w={220} t0={tEm - 0.1} pop={false} rim={4} />
      </Track>
      <Clipping src="img/q_quar.png" x={340} y={650} w={560} h={88} rot={-1.2} t0={tGai} hl={tGai + 0.1} />
      <Cutout src="img/v/envelope.png" x={150} y={770} w={200} rot={-6} t0={tFu} />
      <Tick cx={310} cy={775} s={38} t0={tAc} />
      <Cutout src="img/v/padlock.png" x={510} y={720} w={210} rot={3} t0={tSe} />
      <Crack x={514} y={690} len={160} t0={tPr} angle={86} seed={5} width={7} />
    </Stage>
  );
};

// ---------------------------------------------------------------- audits (v0 52.90)
export const AUDIT = [52.9, 55.55] as const;
export const Audit: React.FC = () => {
  const tCl = wt("करीब", 52.92), t18 = wt("18", 53.24), tAnd = wt("और", 54.32), tDo = wt("दो", 54.58), tAu = wt("audits");
  return (
    <Stage v0={AUDIT[0]}>
      <Clipping src="img/aud_18.png" x={340} y={300} w={600} h={100} rot={-1} t0={tCl} hl={t18 - 0.05} />
      <Track keys={[{ t: t18 - 0.35, x: 800, y: 520, rot: -25, s: 1, a: 0 }, { t: t18 - 0.1, x: 660, y: 390, rot: -25, s: 1, a: 1 }, { t: t18 + 0.35, x: 600, y: 350, rot: -25, s: 1.05 }]}>
        <Cutout src="img/v/magnifier.png" x={0} y={0} w={360} t0={t18 - 0.4} pop={false} rim={4} />
      </Track>
      <Cutout src="img/v/clipboard.png" x={190} y={640} w={260} rot={-4} t0={tAnd} />
      <Scribble cx={112} cy={522} rx={30} ry={26} t0={tDo} dur={0.3} color="#6a5acd" width={6} seed={41} />
      <Scribble cx={112} cy={560} rx={30} ry={26} t0={tAu} dur={0.3} color="#6a5acd" width={6} seed={42} />
    </Stage>
  );
};

// ---------------------------------------------------------------- unaffected (v0 58.45)
export const UNAFF = [58.45, 63.6] as const;
export const Unaff: React.FC = () => {
  const tAb = wt("अब"), tD = wt("data"), tB = wt("breach"), tSg = wt("signing"), tSv = wt("services"), tUn = wt("unaffected");
  return (
    <Stage v0={UNAFF[0]} cam={[{ t: UNAFF[0], z: 1, cx: 340, cy: 512 }, { t: UNAFF[1], z: 1.04, cx: 340, cy: 512 }]}>
      <Clipping src="img/stmt_title.png" x={340} y={215} w={600} h={108} rot={-1} t0={tAb} />
      <Clipping src="img/nobreach.png" x={340} y={400} w={580} h={100} rot={-1.5} t0={tD} hl={tB} />
      <Clipping src="img/signing.png" x={340} y={560} w={600} h={100} rot={1.2} t0={tSg} hl={tSv} />
      <Tick cx={340} cy={735} s={90} t0={tUn} width={22} />
      <Scribble cx={340} cy={730} rx={150} ry={130} t0={tUn + 0.1} dur={0.5} color="#2fa872" width={9} seed={51} />
    </Stage>
  );
};

// ---------------------------------------------------------------- trust (v0 69.00)
export const TRUST = [69.0, 72.35] as const;
const Half: React.FC<{ side: -1 | 1; t: number }> = ({ side, t }) => {
  const v = useV(); const u = Math.max(0, v - t);
  const clip = side < 0 ? "polygon(0 0, 52% 0, 46% 45%, 56% 100%, 0 100%)" : "polygon(52% 0, 100% 0, 100% 100%, 56% 100%, 46% 45%)";
  return <div style={{ position: "absolute", left: 175, top: 260, width: 330, height: 450, transform: `translate(${side * 150 * u}px, ${380 * u * u}px) rotate(${side * 40 * u}deg)`, clipPath: clip }}><Img src={staticFile("img/v/padlock.png")} style={{ width: 330 }} /></div>;
};
export const Trust: React.FC = () => {
  const tB = wt("भरोसा"), tU = wt("उठने"), tS = wt("समझो", 71.38);
  return (
    <Stage v0={TRUST[0]} cam={[{ t: TRUST[0], z: 1, cx: 340, cy: 512 }, { t: TRUST[1], z: 1.06, cx: 340, cy: 512 }]}>
      <Gate a={tB} b={tS}><Cutout src="img/v/padlock.png" x={340} y={500} w={330} rot={-2} t0={tB} /><Crack x={352} y={460} len={260} t0={tU} angle={86} seed={6} width={8} /></Gate>
      <Gate a={tS}><Half side={-1} t={tS} /><Half side={1} t={tS} /></Gate>
    </Stage>
  );
};

// ---------------------------------------------------------------- DigiNotar (v0 72.35)
export const DIGI = [72.35, 84.5] as const;
const NL: [number, number][] = [[745, 200], [760, 150], [820, 122], [900, 140], [990, 135], [1002, 165], [985, 260], [972, 330], [945, 385], [880, 385], [870, 420], [862, 470], [780, 452], [720, 470], [660, 452], [640, 430], [700, 385], [690, 338], [722, 310], [732, 262]].map(([x, y]) => [-540 + x * 1.2857, 138 + y * 1.2857] as [number, number]);
export const Digi: React.FC = () => {
  const t2011 = wt("2011"), tNl = wt("Netherlands"), tDi = wt("DigiNotar"), tHk = wt("hack", 75.88), tFk = wt("नकली", 76.74), tCe = wt("certificates", 77.06);
  const tW = [wt("सबने"), wt("उसकी"), wt("मुहर")], tX = [wt("reject"), wt("कर", 79.6), wt("दी", 79.78)], tMa = wt("मामला"), tCal = wt("तीन", 81.84), tWk = wt("हफ्ते"), tBk = wt("bankrupt");
  return (
    <Stage v0={DIGI[0]} hud={<><Clipping src="img/reg_hack.png" x={340} y={225} w={600} h={100} rot={-1.2} t0={tDi} hl={tDi + 0.15} /><StampText text="HACKED" x={340} y={430} rot={-9} t0={tHk} size={84} /></>} cam={[
      { t: DIGI[0], z: 1, cx: 340, cy: 512 }, { t: tNl - 0.3, z: 1, cx: 340, cy: 512 }, { t: tNl + 0.1, z: 0.42, cx: 360, cy: 640 }, { t: tNl + 0.35, z: 0.42, cx: 360, cy: 640 }, { t: tNl + 1.2, z: 1.55, cx: 546, cy: 523 },
      { t: tFk - 0.25, z: 1.55, cx: 546, cy: 523 }, { t: tFk + 0.3, z: 1, cx: 340, cy: 512 }]}>
      <TapeLabel x={150} y={215} w={200} h={76} rot={-5} t0={t2011} text="2011" size={56} seed={9} />
      <Gate a={tNl} b={tFk - 0.1}>
        <Print src="img/atlas.jpg" x={360} y={640} w={1800} h={1010} rot={0} t0={tNl} border={22} fit="fill" />
        <PathMark pts={NL} t0={tNl + 0.5} dur={0.9} width={22} />
        <TapeLabel x={546} y={610} w={360} h={90} rot={-3} t0={tNl + 0.9} text="NETHERLANDS" size={44} seed={12} />
      </Gate>
      <Cutout src="img/v/certificate.png" x={210} y={560} w={300} rot={-8} t0={tFk} />
      <Cutout src="img/v/certificate.png" x={430} y={610} w={300} rot={6} t0={tCe} />
      {[110, 325, 540].map((x, i) => <BrowserWin key={i} x={x} y={i === 1 ? 790 : 770} w={180} rot={[-3, 2, -2][i]} t0={tW[i]} lock="bad" xAt={tX[i]} tOut={tMa} />)}
      <CalPage x={340} y={730} w={200} rot={-3} t0={tCal} top="WEEKS" big="3" />
      <Underline x1={250} x2={430} y={850} t0={tWk} color="#e6dc2a" width={13} />
      <StampText text="BANKRUPT" x={340} y={520} rot={-12} t0={tBk} size={96} />
    </Stage>
  );
};

// ---------------------------------------------------------------- 1% (v0 84.50)
export const REV = [84.5, 87.5] as const;
const RevInner: React.FC = () => {
  const v = useV(); const tR = wt("revenue"), tSi = wt("सिर्फ", 85.88), tOne = wt("1%");
  const gx = 340, gy = 470, sp = 52; const r0 = 3, c0 = 6; const dim = 1 - 0.65 * easeOut(prog(v, tSi, 0.25));
  return (
    <>
      {Array.from({ length: 100 }, (_, n) => { const r = Math.floor(n / 10), c = n % 10; const t = tR + r * 0.065; const q = easeBack(prog(v, t, 0.18), 1.4); if (v < t) return null;
        return <Img key={n} src={staticFile("img/v/coin.png")} style={{ position: "absolute", left: gx + (c - 4.5) * sp - 23, top: gy + (r - 4.5) * sp - 23, width: 46, transform: `scale(${q})`, opacity: dim, filter: "drop-shadow(2px 4px 3px rgba(30,20,8,0.45))" }} />; })}
      {v >= tSi && <div style={{ position: "absolute", left: gx + (c0 - 4.5) * sp - 60, top: gy + (r0 - 4.5) * sp - 60, width: 120, height: 120, borderRadius: "50%", background: "#efe22e", mixBlendMode: "multiply", transform: `scale(${easeBack(prog(v, tSi, 0.25), 1.5)})`, filter: "url(#rough)" }} />}
      {v >= tSi && <Img src={staticFile("img/v/coin.png")} style={{ position: "absolute", left: gx + (c0 - 4.5) * sp - 52, top: gy + (r0 - 4.5) * sp - 52, width: 104, transform: `scale(${easeBack(prog(v, tSi, 0.25), 1.5)})`, filter: "drop-shadow(4px 8px 6px rgba(30,20,8,0.5))" }} />}
      <Scribble cx={gx + (c0 - 4.5) * sp} cy={gy + (r0 - 4.5) * sp} rx={74} ry={74} t0={tOne} dur={0.4} color="#6a5acd" width={7} seed={61} />
      <TapeLabel x={340} y={800} w={270} h={120} rot={-3} t0={tOne} text="1%" size={96} seed={14} />
    </>
  );
};
export const Rev: React.FC = () => <Stage v0={REV[0]} cam={[{ t: REV[0], z: 1, cx: 340, cy: 512 }, { t: REV[1], z: 1.04, cx: 340, cy: 512 }]}><RevInner /></Stage>;

// ---------------------------------------------------------------- credibility (top half 720x640, v0 87.50)
export const CRED = [87.5, 91.85] as const;
const CredInner: React.FC = () => {
  const v = useV(); const tP = wt("पूरी"), tT = wt("credibility"), tQ = wt("है", 90.06); const q = easeBack(prog(v, tQ, 0.3), 1.8);
  return (
    <>
      <LogoTag x={340} y={330} w={520} t0={tP} tTear={tT} rot={-2} />
      {v >= tQ && <div style={{ position: "absolute", left: 340, top: 330, transform: `translate(-50%,-50%) rotate(6deg) scale(${0.6 + 0.4 * q})`, fontFamily: FONT.marker, fontSize: 300, color: "#efe22e", WebkitTextStroke: "7px #1e1e23", filter: "drop-shadow(8px 12px 6px rgba(30,20,8,0.45))", opacity: Math.min(1, q * 2) }}>?</div>}
    </>
  );
};
export const Cred: React.FC = () => <Stage v0={CRED[0]} dy={-40}><CredInner /></Stage>;
