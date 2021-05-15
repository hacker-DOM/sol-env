#!/usr/bin/env python3

import argparse
import os
import glob
import re
from enum import IntEnum

class VerbosityLog(IntEnum):
    SILENT = 0
    DEFAULT = 1
    VERBOSE = 2

# when imported from ./test, don't run logs
verbosity = VerbosityLog.SILENT

def _dead():
    raise Exception('This case should not happen. Please create an issue in sol-env.')

def setVerbosity(silent, verbose):
    global verbosity
    if not silent and not verbose:
         verbosity = VerbosityLog.DEFAULT
    elif not silent and verbose:
        verbosity = VerbosityLog.VERBOSE

def log(str):
    if verbosity >= VerbosityLog.DEFAULT:
        print (str)

def logVerbose(str):
    if verbosity == VerbosityLog.VERBOSE:
        print (str)

def parse_args():
    parser = argparse.ArgumentParser(
        description='Switch between environments in Solidity.'
    )
    parser.add_argument(
        "path",
        help="Specify a path to a file or root of a directory containing a `contracts` (immediate) subdirectory."
    )
    parser.add_argument(
        '--env',
        action='store',
        help='Specify which environment to use.',
        required=True,
    )

    parser.add_argument(
        '--silent',
        action='store_true',
        help='Don\'t print anything.',
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print in verbose mode.',
    )

    return parser.parse_args()

def get_fns(path):
    if os.path.isfile(path):
        return [path]
    else:
        return glob.glob(path + '/contracts/**/*.sol', recursive=True)

def rm_line_break(line):
    if line[-1] == '\n':
        return (True, line[:-1])
    if line[-1] != '\n':
        return (False, line)
    _dead(0)

def process_line(env, fn, line, line_no):
    segments = line.split('// sol-env:')
    if len(segments) == 1:
        # No "// sol-env:"
        return (False, line)
    if len(segments) > 1:
        assert len(segments) <= 2, 'too many "// sol-env:"s'
        
        # "// sol-env:" segment
        # Remove newline character for parsing sol-envs
        sol_env_segment = rm_line_break(segments[1])[1]
        # sol-envs
        envs = sol_env_segment.split(',')

        # Find first non-whitespace character in "code" segment
        re_iter = re.finditer('\S', segments[0])
        list_of_spans = [x.span() for x in re_iter]
        if len(list_of_spans) == 0:
            # Line is composed only of whitespaces
            # In this case we pass
            return (False, line)
        elif len(list_of_spans) > 0:
            # index of first non-whitespace character
            ifnwc = list_of_spans[0][0]
            if segments[0][ifnwc:ifnwc + 3] == '// ':
                # First non-whitespace character gives rise to "// "
                comment_idx = ifnwc
                if env in envs:
                    # Activate line
                    new_line = line[:comment_idx] + line[comment_idx + 3:]
                    log('%s:L%s activated' % (fn, line_no))
                    log('New:\n%s' % rm_line_break(new_line)[1])
                    return (True, new_line)
                elif env not in envs:
                    # Line is already deactivated, do nothing
                    return (False, line)
                _dead()
            if segments[0][ifnwc:ifnwc + 3] != '// ':
                if env in envs:
                    # Line is already activated, do nothing
                    return (False, line)
                if env not in envs:
                    # Deactivate line
                    new_line = line[:ifnwc] + '// ' + line[ifnwc:]
                    log('%s:L%s deactivated' % (fn, line_no))
                    log('New:\n%s' % rm_line_break(new_line)[1])
                    return (True, new_line)
                _dead()
            _dead()
        _dead()        

def process_fn(env, fn):
    file_changed = False
    logVerbose('Opening file %s' % fn)
    f = open(fn, 'r')
    lines = f.readlines()
    for line_idx, line in enumerate(lines):
        line_no = line_idx + 1
        try:
            line_changed, new_line = process_line(env, fn, line, line_no)
        except Exception as e:
            print ('Error ocurred in %s:L%s:\n%s' % (fn, repr(line_no), repr(e)))
            raise
        if line_changed:
            lines[line_idx] = new_line
            file_changed = True
    return file_changed, lines

def process_fns(env, fns):
    changes = {}
    for fn in fns:
        file_changed, new_lines = process_fn(env, fn)
        if file_changed:
            # We'll run all changes at the end to reduce risk of violating atomicity
            changes[fn] = new_lines
    return changes
    
def process_changes(changes):
    for fn in changes:
        f = open(fn, 'w')
        logVerbose('Writing file %s' % fn)
        f.writelines(changes[fn])
        f.close()

def main():
    try:
        args = parse_args()
        setVerbosity(args.silent, args.verbose)
        # filenames
        fns = get_fns(args.path)
        changes = process_fns(args.env, fns)
        process_changes(changes)
    except Exception as e:
        print ('An error ocurred:\n%s' % repr(e))
        raise

if __name__ == '__main__':
    main()