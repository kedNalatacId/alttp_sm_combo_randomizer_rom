
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
    - Boolean; defaults to false
    - Chooses various options at random

### Metroid-Specific Parameters

- cards
    - Whether to use keycards or not
    - Optional
    - Boolean; defaults to true
- new_screw
    - Whether to use separated space jump / screw attack or not
    - Optional
    - Boolean; defaults to true
    - Ignored when surprise mode is set
- map
    - Whether to show Super Metroid's map upon landing
    - Optional
    - Boolean; defaults to true
    - Ignored when surprise mode is set
- energybeep
    - Whether the low health beep should play or not
    - Optional
    - Boolean; defaults to true
    - Ignored when surprise mode is set
- map_icons
    - Whether or not keycard map icons appera on the SM map
    - Optional
    - Boolean; defaults to true
    - Ignored when surprise mode is set
- oldcards
    - Whether to use new or old keycard graphics
    - Optional
    - Boolean; defaults to false
    - Ignored when surprise mode is set
- always_bt
    - Whether to always trigger the Bomb Torizo fight or not
    - Optional
    - Boolean; defaults to true
    - Ignored when surprise mode is set
    - This value is chosen by the global seed;
        it should be the same for all players
- bt_escape
    - How fast the door closes for the Bomb Torizo fight
    - Optional
    - Values are either "normal" or "double"; defaults to double
        - "double" doubles the amount of time available to escape
            (makes it easier to escape)
    - Ignored when surprise mode is set
    - This value is chosen by the global seed;
        it should be the same for all players
- skip_g4_cutscene
    - Skips the Golden Four Statue cut scene when heading to Tourian
        - Set to false if you like watching the statue fall (not good for race seeds)
    - NOT CURRENTLY WORKING; broken with recent changes allowing Early Tourian
    - Optional
    - Boolean; defaults to true
    - Ignored when surprise mode is set
    - This value is chosen by the global seed;
        it should be the same for all players
- zebes
    - Starts Zebes either asleep (like classic SM) or awake
        - Zebes wakes up on any transition to Zelda
    - Optional
    - Values are either "asleep" or "awake"
    - Ignored when surprise mode is set
    - The door to wake zebes is currently bottom of the climb heading into pit room
        - goal is to move it to back of pit room (so that pit room is still asleep)

### Zelda-Specific Parameters

- keyshuffle
    - Which dungeon items are active
    - This is a simple bitmask
        - 1 == maps
        - 2 == compasses
        - 4 == small keys
        - 8 == big keys
    - Optional
- heartbeep
    - What speed to beep when Link is low on health
    - Optional
    - Possible Values:
        - 00 or "off"
        - 20 or "normal"
        - 40 or "half"
        - 80 or "quarter"
    - Ignored when surprise mode is set
- heartcolor
    - What color to shade Link's heart (upper right corner of screen)
    - Optional
    - Possible Values:
        - blue
        - green
        - red
        - yellow
    - Ignored when surprise mode is set
- persistent_floodgate
    - Whether to keep the floodgate area drained or not
    - Optional
    - Boolean; defaults to false
    - Ignored when surprise mode is set
- quickswap
    - Enables quick swap in Zelda via the L + R shoulder buttons
        - as well as cycling stacked items with double shoulder presses
    - Optional
    - Boolean; defaults to false
    - Ignored when surprise mode is set
    - This value is chosen by the global seed;
        it should be the same for all players
- skipz3title
    - Skips the Zelda file select screen
    - Optional
    - Boolean; defaults to true
    - Ignored when surprise mode is set
    - This value is chosen by the global seed;
        it should be the same for all players
