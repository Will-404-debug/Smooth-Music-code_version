# Smooth Music Project (Code Version)

## Overview
Python script that writes a fully arranged cinematic MIDI piece called **"Echoes of Light (Full Cinematic)"**. It programs piano, strings, brass, choir, pads, and percussion across a 48-bar form (about 3 minutes at 100 BPM) and saves the result to `Echoes_of_Light_Full_Cinematic.mid`.

## Requirements
- Python 3.9+ (tested with recent 3.x)
- [`midiutil`](https://pypi.org/project/MIDIUtil/) for MIDI file creation

Install the dependency:
```bash
pip install MIDIUtil
```

## Quick start
```bash
cd Smooth-Music-code_version
python make_echoes_of_light.py
```
The script prints `Done! Wrote Echoes_of_Light_Full_Cinematic.mid` and drops the MIDI in the repo root. Open the file in your DAW or a MIDI player to audition.

## Composition at a glance
- **Tempo/time:** 100 BPM, 4/4, 48 bars (~3:00)
- **Form:** Intro (0-7) → Build-up (8-19) → Climax (20-31) → Resolution (32-43) → Outro (44-47)
- **Key center:** D minor, with a climax loop of Dm–Gm–Bb–A7

### Tracks and instrumentation
- Piano arps (gentle to strong)
- Strings pad bed
- Brass stabs (horns/trumpet)
- Choir aahs (soft to fortissimo)
- Percussion (taiko-style hits, tom rolls, cymbal)
- Synth pad drone
- Separate section strings: Violin I, Violin II, Viola, Cello, Bass

### What the script does
- Sets up GM program numbers, tempo, and time signature for each track.
- Defines helper functions for chords, arps, and hits, then sequences motifs per section.
- Writes everything into a single multi-track MIDI file and saves it to disk.

## Customization tips
- **Tempo:** change `BPM` near the top.
- **Length/sections:** edit the `INTRO_SEQ`, `CLIMAX_SEQ`, and the section loops.
- **Instrumentation:** swap GM program numbers in `TRACKS` or add your own tracks.
- **Dynamics:** tweak velocity values in the section loops for louder/softer parts.

## Files
- `make_echoes_of_light.py` — script that generates the MIDI.
- `Echoes_of_Light_Full_Cinematic.mid` — output after running the script.
- `LICENSE` — MIT License.

## License
MIT License. See `LICENSE` for details.
