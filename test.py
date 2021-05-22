#!/usr/bin/env python3

from sol_env import process_line

coms_envs_preimages_imgs = [
    # any lines without the metadata are fixed-points
    ('//', 'dev', 'foo', 'foo'),
    # empty lines are also invariant
    ('//', 'dev', '    // sol-env:dev', '    // sol-env:dev'),
    ('//', 'dev', '', ''),
    ('//', 'dev', '    ', '    '),
    # An activated line remains activated
    (
        '//',
        'tests',
        '    assert(isAllowedlisted[user]); // sol-env:console-log,tests',
        '    assert(isAllowedlisted[user]); // sol-env:console-log,tests',
    ),
    # A deactivated line gets activated
    (
        '//',
        'tests',
        '    // assert(isAllowedlisted[user]); // sol-env:console-log,tests',
        '    assert(isAllowedlisted[user]); // sol-env:console-log,tests',
    ),
    # A deactivated line stays deactivated
    (   
        '//',
        'production',
        '    // assert(isAllowedlisted[user]); // sol-env:console-log,tests',
        '    // assert(isAllowedlisted[user]); // sol-env:console-log,tests',
    ),
    # An activated line gets deactivated
    (
        '//',
        'production',
        '    assert(isAllowedlisted[user]); // sol-env:console-log,tests',
        '    // assert(isAllowedlisted[user]); // sol-env:console-log,tests',
    ),
    # A yml/vyper activated line remains activated
    (
        '#',
        'dev',
        'testLimit: 5000 # sol-env:dev',
        'testLimit: 5000 # sol-env:dev',
    ),
    # A yml/vyper deactivated line gets activated
    (
        '#',
        'dev',
        '# testLimit: 5000 # sol-env:dev',
        'testLimit: 5000 # sol-env:dev',
    ),
    # A yml/vyper activated line gets deactivated
    (
        '#',
        'canonical',
        'testLimit: 5000 # sol-env:dev',
        '# testLimit: 5000 # sol-env:dev',
    ),
    # A yml/vyper deactivated line remains deactivated
    (
        '#',
        'canonical',
        '# testLimit: 5000 # sol-env:dev',
        '# testLimit: 5000 # sol-env:dev',
    ),
]


def main():
    for idx, (com, env, preimg, img) in enumerate(coms_envs_preimages_imgs):
        # test newline
        assert img + '\n' == process_line(com, env, 'test.py', preimg + '\n', idx)[1]
        # test w/o newline
        assert img == process_line(com, env, 'test.py', preimg, idx)[1]
        # print result
        print ('Test passed:\ncom    = %s\nenv    = %s\npreimg = %s\nimg    = %s' % (com, env, preimg, img))
    print ('All tests passing!')

if __name__ == '__main__':
    main()