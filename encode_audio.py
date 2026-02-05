r"""
Generate Base64 from an MP3 for the hackathon API tester.
Usage:
  1. Put your .mp3 file in this folder (e.g. sample.mp3)
     OR
  2. Run: python encode_audio.py "C:\path\to\your\file.mp3"
"""
import base64
import sys
from pathlib import Path

# Default: look for an MP3 in the same folder as this script
script_dir = Path(__file__).resolve().parent

if len(sys.argv) >= 2:
    mp3_path = Path(sys.argv[1])
else:
    # Try common names; Windows may hide extension so "sample" might be sample.mp3
    candidates = [
        script_dir / "sample.mp3",
        script_dir / "sample.mp3.mp3",
        script_dir / "sample",
    ]
    mp3s = list(script_dir.glob("*.mp3"))
    if mp3s:
        candidates.append(mp3s[0])
    mp3_path = None
    for c in candidates:
        if c.exists():
            mp3_path = c
            break
    if mp3_path is None:
        mp3_path = script_dir / "sample.mp3"  # for error message

if not mp3_path or not mp3_path.exists():
    print(f"ERROR: File not found: {mp3_path}")
    print()
    print("Do one of the following:")
    print("  1. Copy your MP3 into this folder and name it 'sample.mp3'")
    print(f"     Folder: {script_dir}")
    print("  2. Run with the full path: python encode_audio.py \"C:\\path\\to\\your.mp3\"")
    sys.exit(1)

audio_bytes = mp3_path.read_bytes()
audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

out_file = script_dir / "audio_base64.txt"
out_file.write_text(audio_base64, encoding="utf-8")

print(f"OK: Read {len(audio_bytes)} bytes from {mp3_path.name}")
print(f"Saved Base64 ({len(audio_base64)} chars) to: {out_file}")
