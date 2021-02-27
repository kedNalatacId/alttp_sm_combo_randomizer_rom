
## Some relevant asm build options for SMZ3

You can copy the sample_config.json and change the parameters in order
to get started. You do NOT need this file at all if you use the AsarBin
and AutoIPS options available from CLI for SMZ3.

Unlike SMZ3's JSON config, this is a flat configuration file.

### Essential Parameters

- asar
    - Optional
    - Defaults to 'asar' in local directory
    - Can be set via AsarBin when building SMZ3 from CLI
- mode
    - Optional
    - Sets whether we're building for SMZ3 or SMR
- surprise_me
    - Optional
    - Boolean
    - Chooses various options at random

### Metroid-Specific Parameters

- cards
    - Optional
    - Boolean
    - Whether to use keycards or not
- new_screw
    - Optional
    - Ignored when surprise mode is set
    - Boolean
    - Whether to use separated space jump / screw attack or not
    - Defaults to True
- map
    - Optional
    - Ignored when surprise mode is set
    - Boolean
    - Whether to show Super Metroid's map upon landing
- energybeep
    - Optional
    - Ignored when surprise mode is set
    - Boolean
    - Whether the low health beep should play or not
- map_icons
    - Optional
    - Ignored when surprise mode is set
    - Boolean
    - Whether or not keycard map icons appera on the SM map
- oldcards
    - Optional
    - Ignored when surprise mode is set
    - Boolean
    - Whether to use new or old keycard graphics
- skip_g4_cutscene
    - Optional
    - Ignored when surprise mode is set
    - IMPORTANT: This value is chosen by the global seed;
        it should be the same for all players
    - Skips the Golden Four Statue cut scene when heading to Tourian
- zebes
    - Optional
    - Ignored when surprise mode is set
    - Values are either "asleep" or "awake"
    - Starts Zebes either asleep (like classic SM) or awake
    - Zebes wakes up on any transition to Zelda
    - The door to wake zebes is currently bottom of the climb heading into pit room
        - goal is to move it to back of pit room (so that pit room is still asleep)

### Zelda-Specific Parameters

- keyshuffle
    - Optional
    - Which dungeon items are active
    - This is a simple bitmask
        - 1 == maps
        - 2 == compasses
        - 4 == small keys
        - 8 == big keys
- heartbeep
    - Optional
    - Ignored when surprise mode is set
    - Possible Values:
        - 00 or "off"
        - 20 or "normal"
        - 40 or "half"
        - 80 or "quarter"
- heartcolor
    - Optional
    - Ignored when surprise mode is set
    - Possible Values:
        - blue
        - green
        - red
        - yellow
- quickswap
    - Optional
    - Ignored when surprise mode is set
    - IMPORTANT: This value is chosen by the global seed;
        it should be the same for all players
    - Enables quick swap in Zelda via the L + R shoulder buttons
- skipz3title
    - Optional
    - Ignored when surprise mode is set
    - IMPORTANT: This value is chosen by the global seed;
        it should be the same for all players
    - Skips the Zelda file select screen
