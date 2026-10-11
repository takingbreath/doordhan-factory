Install FaceFusion (official, open source) on this laptop and run one face-swap test for Doordhan. Use only the official repo: https://github.com/facefusion/facefusion. No forks or Hugging Face copies.

1. Check what this machine has (OS, Apple Silicon or NVIDIA GPU, free disk; it needs about 10 GB). Install Miniconda if conda is missing.
2. `conda create -n facefusion python=3.12 -y && conda activate facefusion`, then `conda install -c conda-forge ffmpeg -y`.
3. `git clone https://github.com/facefusion/facefusion && cd facefusion`, then run its installer for this machine: `python install.py --onnxruntime default` (or `cuda` on an NVIDIA GPU; on a Mac, `default` covers CoreML).
4. Ask Akhilesh for the two inputs, which he has: the character photo (the source face) and the video clip (the target).
5. Run headless (no UI), face only:
   `python facefusion.py headless-run --source-paths <character.png> --target-path <target.mp4> --output-path <out>/ff_local.mp4 --processors face_swapper face_enhancer --face-swapper-model hyperswap_1a_256 --face-swapper-pixel-boost 512x512 --face-enhancer-model gfpgan_1.4 --face-enhancer-blend 80 --face-mask-types box occlusion region --face-selector-mode one --output-video-quality 90`
   If an option name is rejected, run `python facefusion.py headless-run --help` and use the matching option from this version; keep the same intent (hyperswap, 512 pixel boost, enhancer at 80%, occlusion + region masks, the one face in frame).
6. Also make an `inswapper_128` version with the same settings, for comparison.
7. Put both outputs in doordhan-factory/outputs/recast/ and tell Akhilesh the paths, the time each run took, and any warnings. Don't commit the videos, and don't upload or post them anywhere.
