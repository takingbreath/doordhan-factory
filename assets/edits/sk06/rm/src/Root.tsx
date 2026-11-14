import React from "react";
import { Composition } from "remotion";
import { Reel, TOTAL } from "./Reel";
export const Root: React.FC = () => (
  <>
    <Composition id="SK06" component={Reel} durationInFrames={Math.round(TOTAL * 30)} fps={30} width={720} height={1280} />
  </>
);
