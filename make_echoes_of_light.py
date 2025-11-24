# make_echoes_of_light.py
# Creates: Echoes_of_Light_Full_Cinematic.mid
# Requires: pip install MIDIUtil

from midiutil import MIDIFile

TITLE = "Echoes of Light — Full Cinematic"
OUTFILE = "Echoes_of_Light_Full_Cinematic.mid"

# ---------- Session ----------
BPM = 100
TPB = 480   # ticks per beat (handled internally by MIDIUtil)
TSIG_NUM = 4
TSIG_DEN = 4

# Program numbers (General MIDI; 0-based)
GM = {
    "piano": 0,          # Acoustic Grand
    "strings": 48,       # Strings Ensemble 1
    "violin": 40,        # Violin
    "viola": 41,         # Viola
    "cello": 42,         # Cello
    "bass": 43,          # Contrabass
    "horns": 60,         # French Horn
    "trumpet": 56,       # Trumpet
    "choir": 52,         # Choir Aahs
    "pad": 89            # Warm Pad
}
DRUM_CH = 9  # Channel 10 in 1-based GM

# ---------- Tracks ----------
# 0 Piano, 1 Strings (pad), 2 Brass (horns+trumpet), 3 Choir, 4 Percussion, 5 Pad,
# 6 Violin I, 7 Violin II, 8 Viola, 9 Cello, 10 Bass
TRACKS = [
    ("Piano",      0, GM["piano"]),
    ("StringsPad", 1, GM["strings"]),
    ("Brass",      2, GM["horns"]),
    ("Choir",      3, GM["choir"]),
    ("Percussion", DRUM_CH, None),
    ("SynthPad",   4, GM["pad"]),
    ("Violin I",   5, GM["violin"]),
    ("Violin II",  6, GM["violin"]),
    ("Viola",      7, GM["viola"]),
    ("Cello",      8, GM["cello"]),
    ("Bass",       9, GM["bass"]),
]

mf = MIDIFile(numTracks=len(TRACKS), removeDuplicates=True, deinterleave=False, adjust_origin=True)

for i, (name, ch, prog) in enumerate(TRACKS):
    mf.addTrackName(i, 0, name)
    mf.addTempo(i, 0, BPM)
    mf.addTimeSignature(i, 0, TSIG_NUM, TSIG_DEN, 24)  # simple 4/4
    if prog is not None:
        mf.addProgramChange(i, ch, 0, prog)

# ---------- Helpers ----------
def chord(track, ch, when, dur, notes, vel):
    """Block chord."""
    for n in notes:
        mf.addNote(track, ch, n, when, dur, vel)

def arp(track, ch, when, dur, notes, vel, step=0.25):
    """Arpeggiate notes over 1 bar (4 beats) by step beats."""
    t = when
    for n in notes:
        mf.addNote(track, ch, n, t, dur, vel)
        t += step

def hit(track, ch, when, dur, note, vel):
    mf.addNote(track, ch, note, when, dur, vel)

# MIDI note helpers
# D minor core chords (Dm, Bb, F, C):
Dm = [62, 65, 69]           # D F A
Bb = [70, 74, 77]           # Bb D F
F  = [65, 69, 72]           # F A C
C  = [60, 64, 67]           # C E G
# Climax loop (Dm, Gm, Bb, A):
Gm = [67, 70, 74]           # G Bb D
A7 = [69, 73, 76]           # A C# E  (dominant feel)

INTRO_SEQ   = [Dm, Bb, F, C]               # 4 bars
CLIMAX_SEQ  = [Dm, Gm, Bb, A7]             # 4 bars

# Bar → beat mapping (4/4; 1 bar = 4 beats)
def bar_time(b): return b * 4.0

# ---------- Form (48 bars total; ~3:00 @ 100 BPM) ----------
# 0–7:   Intro (8 bars)
# 8–19:  Build-up (12 bars)
# 20–31: Climax (12 bars)
# 32–43: Resolution (12 bars)
# 44–47: Outro (4 bars)

# ========== INTRO (bars 0–7) ==========
for i, chord_set in enumerate(INTRO_SEQ * 2):
    bar = i
    t = bar_time(bar)
    # Piano arps (gentle)
    arp(0, TRACKS[0][1], t, 0.25, [n for n in chord_set] + [n+12 for n in chord_set], 60, step=0.33)
    # Strings pad (sustained)
    chord(1, TRACKS[1][1], t, 4.0, [n for n in chord_set], 50)
    # Pad drone (low root, 2 bars)
    if i % 2 == 0:
        chord(5, TRACKS[5][1], t, 8.0, [chord_set[0]-24], 40)

# ========== BUILD-UP (bars 8–19) ==========
build_seq = INTRO_SEQ * 3
for i, chord_set in enumerate(build_seq):
    bar = 8 + i
    t = bar_time(bar)
    # Piano arps a bit stronger
    arp(0, TRACKS[0][1], t, 0.25, [n for n in chord_set] + [n+12 for n in chord_set], 72, step=0.33)
    # Strings sustain with slow crescendo
    chord(1, TRACKS[1][1], t, 4.0, chord_set, 60 + (i // 4)*4)
    # Light horns roots (whole notes)
    chord(2, TRACKS[2][1], t, 4.0, [chord_set[0]-12], 58)
    # Choir soft “ooh” from bar 12 (index 4)
    if i >= 4:
        chord(3, TRACKS[3][1], t, 4.0, [chord_set[0]+12, chord_set[1]+12, chord_set[2]+12], 55)
    # Taiko pulse from bar 16 (index 8): kick every 2 beats
    if i >= 8:
        for beat in (0, 2):
            hit(4, DRUM_CH, t + beat, 0.15, 36, 96)  # 36 = Bass Drum
    # Small riser every 4 bars (simulate with tom rolls)
    if i % 4 == 3:
        for s in (3.0, 3.5, 3.75):
            hit(4, DRUM_CH, t + s, 0.1, 45, 90)  # 45 = Low Tom

# ========== CLIMAX (bars 20–31) ==========
climax_seq = CLIMAX_SEQ * 3
for i, chord_set in enumerate(climax_seq):
    bar = 20 + i
    t = bar_time(bar)
    # Piano strong arps
    arp(0, TRACKS[0][1], t, 0.25, [n for n in chord_set] + [n+12 for n in chord_set], 92, step=0.25)
    # Strings pad full
    chord(1, TRACKS[1][1], t, 4.0, chord_set, 82)
    # Brass upper stabs (octave up)
    chord(2, TRACKS[2][1], t, 1.0, [n+12 for n in chord_set], 104)
    # Choir wide SATB block
    satb = [chord_set[0]+24, chord_set[1]+12, chord_set[2], chord_set[0]-12]
    chord(3, TRACKS[3][1], t, 4.0, satb, 106)
    # Percussion: taikos on 1 & 3 + crash on 1
    for beat in (0, 2):
        hit(4, DRUM_CH, t + beat, 0.15, 36, 120)   # kick
        hit(4, DRUM_CH, t + beat, 0.15, 43, 110)   # high floor tom
    hit(4, DRUM_CH, t + 0.0, 0.4, 49, 112)         # crash cymbal
    # Melody (Violins I) — simple heroic line following root to 5th
    mel = [chord_set[0]+24, chord_set[1]+24, chord_set[2]+24, chord_set[0]+31]  # D–F–A–D'
    step = 1.0
    tm = t
    for n in mel:
        hit(6, TRACKS[6][1], tm, 0.9, n, 108)
        tm += step
    # Harmony (Violins II)
    harm = [n-5 for n in mel]
    tm = t
    for n in harm:
        hit(7, TRACKS[7][1], tm, 0.9, n, 96)
        tm += step
    # Inner strings (Viola long)
    chord(8, TRACKS[8][1], t, 4.0, [chord_set[1]+7], 80)
    # Cello counter (descending)
    hit(9, TRACKS[9][1], t, 2.0, chord_set[0]-12, 90)
    hit(9, TRACKS[9][1], t+2.0, 2.0, chord_set[2]-12, 88)
    # Bass pedal
    chord(10, TRACKS[10][1], t, 4.0, [chord_set[0]-24], 92)

# Ring out big dominant A at bar 32
t = bar_time(32)
chord(3, TRACKS[3][1], t, 4.0, [69+24, 73+12, 76, 57], 100)  # choir sustain

# === ADD CHOIR "AHH" VOCALS (Bars 0–47) ===
# Smooth "Ahh" sustained harmonies following D minor progression
# Softer in intro, rising in climax, fading in outro

choir_velocity = 50

# Intro (bars 0–7): soft, airy AHH
for i, chord_set in enumerate(INTRO_SEQ * 2):
    bar = i
    t = bar_time(bar)
    chord(3, TRACKS[3][1], t, 4.0, [n + 12 for n in chord_set], choir_velocity)

# Build-up (bars 8–19): more power
for i, chord_set in enumerate(INTRO_SEQ * 3):
    bar = 8 + i
    t = bar_time(bar)
    chord(3, TRACKS[3][1], t, 4.0, [n + 12 for n in chord_set], choir_velocity + 10)

# Climax (bars 20–31): full choir fortissimo
for i, chord_set in enumerate(CLIMAX_SEQ * 3):
    bar = 20 + i
    t = bar_time(bar)
    chord(3, TRACKS[3][1], t, 4.0, [n + 24 for n in chord_set] + [n + 12 for n in chord_set], choir_velocity + 40)

# Resolution (bars 32–43): gentle, descending harmonies
for i, chord_set in enumerate(INTRO_SEQ * 3):
    bar = 32 + i
    t = bar_time(bar)
    chord(3, TRACKS[3][1], t, 4.0, [n + 12 for n in chord_set], choir_velocity - 10)

# Outro (bars 44–47): final fading AHH
for i in range(4):
    bar = 44 + i
    t = bar_time(bar)
    chord(3, TRACKS[3][1], t, 4.0, [62 + 12, 65 + 12, 69 + 12], choir_velocity - 20)

# ========== RESOLUTION (bars 32–43) ==========
res_seq = INTRO_SEQ * 3
for i, chord_set in enumerate(res_seq):
    bar = 32 + i
    t = bar_time(bar)
    arp(0, TRACKS[0][1], t, 0.25, chord_set, 66, step=0.33)
    chord(1, TRACKS[1][1], t, 4.0, chord_set, 64)
    # Soft female choir echo
    chord(3, TRACKS[3][1], t, 4.0, [chord_set[0]+24], 60)
    # Sparse tom on bar starts
    hit(4, DRUM_CH, t + 0.0, 0.12, 45, 64)

# ========== OUTRO (bars 44–47) ==========
for i in range(4):
    bar = 44 + i
    t = bar_time(bar)
    # One long Dm chord; length decreases slightly to allow reverb tail
    dur = 4.0 if i < 3 else 3.5
    chord(0, TRACKS[0][1], t, dur, [62, 65, 69, 74], 52)     # Piano
    chord(1, TRACKS[1][1], t, dur, [50, 57, 62], 48)         # Strings
    chord(3, TRACKS[3][1], t, dur, [62+12], 44)              # Choir
    chord(5, TRACKS[5][1], t, dur, [38], 40)                 # Pad
    # Gentle cymbal at very end
    if i == 0:
        hit(4, DRUM_CH, t, 0.5, 49, 70)

with open(OUTFILE, "wb") as f:
    mf.writeFile(f)

print(f"Done! Wrote {OUTFILE}")
