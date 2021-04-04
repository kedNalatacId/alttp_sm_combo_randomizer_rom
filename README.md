
BE WARNED, this is a "pet" project... it's probably not what you want.

You still have time to turn back, you're probably looking for:
https://github.com/tewtal/alttp_sm_combo_randomizer_rom

-----

The canonical method of running build.py is:  
`# python3 build.py --config options.json`

You can look at example.json for a breakdown of all the options.

This assembly can be used for either SMZ3 or SMR with keycards

-----

A number of changes have occurred between Tewtal's original version and here.

1. Move from build.sh to build.py
    - some of the downstream dependencies have been folded in
    - various pythonic changes (could still be better)
    - creates temporary intermediate files and cleans up after them
    - this might be an improvement; not for me to judge
    - currently building SM sprite data is hard-coded instead of `find -exec`
        - unclear on the user stories here of why it was being done with `find -exec`

2. Use templating for some files to allow rapid prototyping
    - To be clear, this is NOT a good solution for production
        - results may be too inconsistent for production
        - the overhead of building IPSs on the fly is bad for prod
    - It does help development be able to move faster
        - no need to find space for variables and load everything
          all the way through from front-app to back-end
        - Best used with the CLI --AutoIPS flag

3. Allow a JSON file for common arguments to avoid repetition
    - asar's location -- doesn't have to be in local dir
    - output file -- it can be placed anywhere on the filesystem
    - see sample.json and json_config_options.md for more info

4. Expanded keysanity mode
    - keycards don't have to be on just because keysanity is
    - each dungeon item (map, compass, small key, big key) can functionally
        have its own keysanity flag set
        e.g. small keys could be in dungeon only, but everything else
        would get dialog boxes and be outside their respective dungeon
    - passed in using bitmasks

4. Added quickswap from ALTTPR
    - but removed iterating through the bottles as it was annoying
        - instead bottles cycle via double-shoulder press
            - this version has been PRed into both ALTTPR and SMZ3 (not necessarily accepted)
        - can be added back if requested

5. Added SMZ3 heart color (previously only available from frontend)
    - for those of us who compile seeds from CLI

6. Added "surprise mode" that randomly chooses decorations
    - Currently includes game-impacting items (like G4 cutscene and quickswap)
        - fine for single-mode/fun, NOT FINE for multiplayer/race
        - for prod, surprise mode should be enabled elsewhere, not here,
            shouldn't be a problem; just because the code for quickswap
            is here doesn't mean it should be enabled, for instance
    - surprise mode is mostly for non-game-impacting stuff like:
        - SM energy beep
        - Z3 heart beep
        - Z3 heart color
        - whether SM map is lit up from start or not
        - etc, &c... and more to come as the code continues to get combed through

7. Removed various amounts of unneeded whitespace and changed various tabs to spaces
    - Corrected various speeling mistooks, etc.

8. progressive bow works

9. Zebes can start asleep rather than awake for SMZ3
    - TODO: Can only get to the pit room because of the morph and missiles check.

10. Fast Ganon, Early GT, Fast Mother Brain, Early Tourian
    - Fast Ganon has the Pyramid Hole open upon first load of Zelda
    - Early GT allows setting a variable number of crystals (between 0 and 7) to open Ganon's Tower
        - Invincible Ganon is included; it may be that 4 crystals open GT, but 6 are required for Ganon
    - Fast Mother Brain has Tourian open upon first load of Metroid
    - Early Tourian allows fewer bosses in order to gain access to Tourian (between 0 and 4)
        - It's also possible to set some bosses as "pre-defeated" by graying out their statues.
          e.g. If Kraid and Phantoon are pre-defeated, then only
            Dragon and Ridley would be required to access Tourian

11. Starting gear (Zelda only so far)
    - It's possible to set Link with starting gear such as boots or sword
