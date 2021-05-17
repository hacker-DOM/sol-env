#!/usr/bin/env python3

from sol_env import process_line

envs_preimages_and_images = [
    # any lines without the metadata are fixed-points
    ('dev', 'foo', 'foo'),
    # empty lines are also invariant
    ('dev', '    // sol-env:dev', '    // sol-env:dev'),
    ('dev', '', ''),
    ('dev', '    ', '    '),
    # An activated line remains activated
    (
        'tests',
        '    assert(isAllowedlisted[user]); // sol-env:console-log,tests',
        '    assert(isAllowedlisted[user]); // sol-env:console-log,tests'
    ),
    # A deactivated line gets activated
    (
        'tests',
        '    // assert(isAllowedlisted[user]); // sol-env:console-log,tests',
        '    assert(isAllowedlisted[user]); // sol-env:console-log,tests'
    ),
    # A deactivated line stays deactivated
    (
        'production',
        '    // assert(isAllowedlisted[user]); // sol-env:console-log,tests',
        '    // assert(isAllowedlisted[user]); // sol-env:console-log,tests'
    ),
    # An activated line gets deactivated
    (
        'production',
        '    assert(isAllowedlisted[user]); // sol-env:console-log,tests',
        '    // assert(isAllowedlisted[user]); // sol-env:console-log,tests'
    ),
]

def main():
    for idx, (env, preimg, img) in enumerate(envs_preimages_and_images):
        # test newline
        assert img + '\n' == process_line(env, 'test.py', preimg + '\n', idx)[1]
        # test w/o newline
        assert img == process_line(env, 'test.py', preimg, idx)[1]
        # print result
        print ('test passed:\nenv    = %s\npreimg = %s\nimg    = %s' % (env, preimg, img))

if __name__ == '__main__':
    main()