#!/usr/bin/env python3
import os
import sys
import json
import argparse
import pathlib
import jinja2
import pprint
import random

# because command line parsing is never exactly how i want it...
defaults = {
    'asar': './asar',
    'cards': True,
    'cleanup': True,
    'energybeep': True,
    'heartbeep': 'normal',
    'heartcolor': 'red',
    'keyshuffle': 15,
    'map': True,
    'mapreveal': False,
    'quickswap': False,
    'output': 'build/zsm.ips',
    'surprise_me': False,
}

def main():
    opts = parse_args()
    if (opts['surprise_me']):
        opts = surprise_me(opts)

    # setup
    print("Building Super Metroid + Zelda 3 Randomizer")
    build_sm_sprites()
    compile_templates(opts)

    # create
    zero = create_dummy('0')
    ff   = create_dummy('f')
    compile_asm(opts["asar"], zero, ff)
    create_ips(opts["output"], zero, ff)

    # teardown
    if opts['cleanup']:
        cleanup(zero, ff)
    print("Done")

# convert bits to bool
def keyshuffle_levels(arg):
    arg = int(arg)
    return {
        "map":       (arg & 1 == 1),
        "compass":   (arg & 2 == 2),
        "small_key": (arg & 4 == 4),
        "big_key":   (arg & 8 == 8)
    }

def parse_args():
    parser = argparse.ArgumentParser(description='Build SMZ3 IPS')
    parser.add_argument('--asar', default='__unset', help='Location of asar binary (default is ./asar)')
    parser.add_argument('--config', help="JSON config file")
    parser.add_argument('-k', '--keyshuffle', default='__unset', help="Keysanity level, currently between 1-15; default is (15) all on")
    parser.add_argument('-c', '--cards', default='__unset', action='store_true', help="Use Keycards; default is true")
    parser.add_argument('--no-cards', dest='cards', action='store_false')
    parser.add_argument('-m', '--map', default='__unset', action='store_true', help="Show SM map; default is true")
    parser.add_argument('--no-map', dest='map', action='store_false')
    parser.add_argument('--mapreveal', default='__unset', action='store_true', help="Reveal map with bomb shop / Sahash (default: off)")
    parser.add_argument('--no-mapreveal', dest='mapreveal', action='store_false')
    parser.add_argument('--energybeep', default='__unset', action='store_true', help="Turn on/off SM Energy Beep (default: on)")
    parser.add_argument('--no-energybeep', dest='energybeep', action='store_false')
    parser.add_argument('--heartbeep', default='__unset', help="Zelda Heart Beep Speed; default is Normal")
    parser.add_argument('--heartcolor', default='__unset', help="Zelda Heart Color; default is Red")
    parser.add_argument('--quickswap', default='__unset', action='store_true', help="Enable Zelda Quick Swap via L+R buttons")
    parser.add_argument('--no-quickswap', dest='quickswap', action='store_false')
    parser.add_argument('--surprise_me', action='store_true', help="Randomize customization settings")
    parser.add_argument('-o', '--output', default='__unset', help="Place to store IPS file (default is build/zsm.ips)")
    parser.add_argument('--cleanup', default='__unset', action='store_true', help="Whether to cleanup created files or not (default is true)")
    parser.add_argument('--no-cleanup', dest='cleanup', action='store_false')
    parser.add_argument('-z', '--zzz', action='store_true', help=argparse.SUPPRESS)

    # there's no use for "unknown" args at this time, but just in case we add one...
    # go the safe route
    args, unknown = parser.parse_known_args()
    args = vars(args)

    if args['config']:
        json_conf = {}
        with open(args['config'], 'r') as conf_file:
            json_conf = json.load(conf_file)

        # cli args take precedence, so don't just merge
        for key in json_conf:
            if key not in args or args[key] == '__unset':
                if isinstance(json_conf[key], str):
                    args[key] = json_conf[key].lower()
                else:
                    args[key] = json_conf[key]

    # Set the defaults now that we know we didn't override them with the json config
    for key in defaults:
        if key not in args or args[key] == '__unset':
            args[key] = defaults[key]

    # convert the keyshuffle levels into something more useful for templating
    args['keyshuffle'] = keyshuffle_levels(args['keyshuffle'])
    args['keycards']   = args.pop('cards');
    args['show_map']   = args.pop('map');

    if args['zzz']:
        print("Options as parsed:")
        pprint.pprint(args)
        sys.exit(0)

    return args

def surprise_me(o):
    random.seed()

    o['show_map'] = True
    if (random.randint(0, 1) < 1):
        o['show_map'] = False

    o['mapreveal'] = True
    if (random.randint(0, 1) < 1):
        o['mapreveal'] = False;

    o['new_screw'] = True
    if (random.randint(0, 1) < 1):
        o['new_screw'] = False

    o['energybeep'] = True
    if (random.randint(0, 1) < 1):
        o['energybeep'] = False

    beeps = ['00', '20', '40', '80']
    o['heartbeep'] = beeps[random.randint(0, 3)]

    color = ['red', 'green', 'blue', 'yellow']
    o['heartcolor'] = color[random.randint(0, 3)]

    o['skip_g4_cutscene'] = True
    if (random.randint(0, 9) < 2):
        o['skip_g4_cutscene'] = False

    o['quickswap'] = True
    if (random.randint(0, 9) < 2):
        o['quickswap'] = False

    return o

# Not stealing this into here, too long
# Could glob this to find it instead, TBD if that's worthwhile
def build_sm_sprites():
    os.system('python3 src/sm/sprite/data/build/build.py');

# provably the same as the below legacy function:
# python3 create_dummies.py 00.sfc ff.sfc
def create_dummy(byte):
    fn = 'build/{}{}.sfc'.format(byte, byte)
    with open(fn, 'wb') as fd:
        fd.write(bytes([int("0x{}{}".format(byte, byte), 16)] * 1024 * 1024 * 6))
    return fn

# Find all .j2 files and compile them into .asm files
def compile_templates(opts):
    for asm_tmpl in pathlib.Path('src').rglob('*.j2'):
        base_path = os.path.dirname(os.path.realpath(asm_tmpl))
        base_file = os.path.basename(os.path.realpath(asm_tmpl))
        asm_file  = os.path.splitext(base_file)[0]

        env = jinja2.Environment(loader=jinja2.FileSystemLoader(base_path))
        tmpl = env.get_template(base_file).render(opts)

        with open("{}/{}".format(base_path, asm_file), 'w') as asm:
            asm.write(tmpl)

def compile_asm(bin, zero, ff):
    os.system('{} --no-title-check --symbols=wla --symbols-path=build/zsm.sym src/main.asm {}'.format(bin, zero))
    os.system('{} --no-title-check --symbols=wla --symbols-path=build/zsm.sym src/main.asm {}'.format(bin, ff))

# this was short enough, stealing into this to reduce number of scripts to run
# [also updated to python3 syntax]
# os.system('python3 resources/create_ips.py build/00.sfc build/ff.sfc build/zsm.ips')
def create_ips(output_file, zero, ff):
    with open(zero, 'rb') as f_zero:
        d_zero = f_zero.read()
    with open(ff, 'rb') as f_ff:
        d_ff = f_ff.read()

    patches = {}
    for i in range(0, len(d_zero), 1):
        if d_zero[i] == d_ff[i]:
            patches[i] = [d_zero[i]]

    base_m = -100
    prev_m = -100
    for m in list(patches.keys()):
        if prev_m == m - 1:
            if len(patches[base_m]) < 0xFFFF:
                patches[base_m] += patches[m]
                del patches[m]
                prev_m = m
            else:
                base_m = m
                prev_m = m
        else:
            base_m = m

    d_patch = []
    for k in patches:
        l = len(patches[k])
        d_patch += [(k >> 16) & 0xff, (k >> 8) & 0xFF, k & 0xFF, (l >> 8) & 0xFF, l & 0xFF] + patches[k]

    d_patch = [0x50, 0x41, 0x54, 0x43, 0x48] + d_patch + [0x45, 0x4f, 0x46]

    with open(output_file, 'wb') as fo:
        fo.write(bytes(d_patch))

def cleanup(zero, ff):
    print("Cleaning up files")
    os.remove(zero)
    os.remove(ff)
    # WIP: remove symbol table? Seems like a good thing?
    #os.remove('build/zsm.sym')

    # remove the .asm files so they don't get used next time accidentally
    # would rather fail than use the wrong file
    for asm_tmpl in pathlib.Path('src').rglob('*.j2'):
        base_path = os.path.dirname(os.path.realpath(asm_tmpl))
        base_file = os.path.basename(os.path.realpath(asm_tmpl))
        asm_file  = os.path.splitext(base_file)[0]
        os.remove("{}/{}".format(base_path, asm_file))

# because python
if __name__ == '__main__':
    main()
