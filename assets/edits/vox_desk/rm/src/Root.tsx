import React from "react";
import { Composition } from "remotion";
import { Chart, V0 as ChartV0 } from "./scenes/Chart";
import { Pass, V0 as PassV0 } from "./scenes/Pass";
import * as M from "./scenes/More";
import { Over18, OverQ } from "./scenes/Overlays";
import { CertPass, CERTPASS } from "./scenes/CertPass";

const FPS = 30;
const dur = (v0: number, v1: number) => Math.round((v1 - v0) * FPS) + 9;
const C = (id: string, comp: React.FC, v: readonly [number, number], h = 1280) => <Composition key={id} id={id} component={comp} durationInFrames={dur(v[0], v[1])} fps={FPS} width={720} height={h} />;
export const Root: React.FC = () => (
  <>
    {C("Hook", M.Hook, M.HOOK, 640)}
    {C("Chart", Chart, [ChartV0, 7.95])}
    {C("Gst", M.Gst, M.GST)}
    {C("Cert", M.Cert, M.CERT)}
    {C("Pass", Pass, [PassV0, 30.05])}
    {C("Hack", M.Hack, M.HACK)}
    {C("Rob", M.Rob, M.ROB)}
    {C("Quar", M.Quar, M.QUAR)}
    {C("Audit", M.Audit, M.AUDIT)}
    {C("Unaff", M.Unaff, M.UNAFF)}
    {C("Trust", M.Trust, M.TRUST)}
    {C("Digi", M.Digi, M.DIGI)}
    {C("Rev", M.Rev, M.REV)}
    {C("Cred", M.Cred, M.CRED, 640)}
    {C("CertPass", CertPass, CERTPASS)}
    <Composition id="Over18" component={Over18} durationInFrames={30} fps={FPS} width={540} height={180} />
    <Composition id="OverQ" component={OverQ} durationInFrames={30} fps={FPS} width={200} height={200} />
  </>
);
