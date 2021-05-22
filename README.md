# sol-env

## Installation

The best way to install `sol-env` is cloning it with `git`, and making a symlink in your `$PATH`.

```bash
git clone https://github.com/hacker-dom/sol-env
ln -s $(pwd)/sol-env/sol_env.py [path-to-python3-dir/bin/sol-env]
chmod 755 [path-to-python3-dir/bin/sol-env]
```

## Motivation
There has been talk (e.g. [here](https://github.com/ethereum/solidity/issues/10825) and [here](https://github.com/ethereum/solidity/issues/8146)) about allowing better support for debug assertions in Solidity. Until that is implemented into Solidity and/or current tooling (and for versions prior to the implementation), this simple utility aspires to be a temporary solution.

`sol-env` allows you to switch between different environments for your Solidity code. There are many examples when this would be useful. You might want to have multiple environments: one for unit and [Echidna][echidna] tests, one for running `console.log`s with [hardhat](https://github.com/nomiclabs/hardhat), and one for production.

It is easily imaginable that there will be small differences in the code between these environments. Solidity currently doesn't allow you to do that; `sol-env` does!

## Use cases

Here are some examples:

### Use case 1

If our mental model of our system is correct, the path condition to get to this line contains this requirement nevertheless, we write an assertion, so that our hard-coded concrete and Echidna fuzz tests will alert us if our assumption is wrong.

```solidity
assert(isAllowedlisted[user]); // sol-env:console-log,tests
```


### Use case 2
Here we "know" that this can't underflow, but we add an assert so that anytime during development, if this fails, we will be notified.

```solidity
assert(balance - amountOwed <= balance); // sol-env:console-log,tests
```

### Use case 3
For tests use this we library internally so we don't have to link it. In production we use this as an external library due to EIP-170.

```solidity
library Foo {
  function foo()
    
    internal // sol-env:console-log,tests
    // external  // sol-env:production
    returns (uint)
  {
    [...]
  }
```

### Use case 4

```solidity
// console.log("Module:swap called with %s", inputValue) // sol-env:console-log
[...]
// console.log("Module:swap returning %s", outputValue) // sol-env:console-log
```

### Use case 5
Prior to Solidity 0.6.5, Solidity did not have support for the `immutable` keyword. This meant that in order to specify parameters that should be baked into the bytecode as opposed to stored as storage values, you would have to use the `constant` keyword. You can automate that as such

```solidity
address constant CHAINLINK_GANACHE_ADDR = 0xaaa // sol-env:ganache
address constant CHAINLINK_KOVAN_ADDR = 0xaab // sol-env:kovan
address constant CHAINLINK_MAINNET_ADDR = 0xaac // sol-env:mainnet
```

### Use case 6
With the `--comment` option, `sol-env` can operate on non-Solidity files, as long as they are specified as a positional argument, rather than a directory. Let's say you are using [Echidna][echidna] during development. Then you might have an `echidna.config.yml`:

```yml
testLimit: 5000 # sol-env:dev
# testLimit: 200000 # sol-env:canonical
```

During development, you're able to run [Echidna][echidna] on a smaller test limit. Once you've written your properties, you can use

```bash
sol-env echidna.config.yml --env canonical --comment '#'
```

and the file will transform to:

```yml
# testLimit: 5000 # sol-env:dev
testLimit: 200000 # sol-env:canonical
```

## Setup

To use `sol-env`, put a postfix of `// sol-env:A,B,C` after any Solidity line. When you run `sol-env`, you specify an environment, e.g. A, B, C or something else. If the environment is A, B or C, then `sol-env` will activate this line. This means that if it is commented (in particular, if the first non-whitespace character gives rise to `// `), then it will remove that `// `.[1]

And vice versa: if the environment is other than A, B or C, `sol-env` will make sure this line is deactivated (i.e. if it is activated it will deactivate it and if it is deactivated it will remain deactivated).

You can of course also specify a single environment with `// sol-env:A`. Or an empty environment list with `// sol-env:` (in which case the line will always be deactivated!).

[1] Note that this also means that if you have multiple comment segments such as

```solidity
//   // _checkState() // sol-env:production
```

and you run it with `--env production` *twice*, `sol-env` will remove both ocurrences. As such, it is not recommended to have adjacent sections of `// `.

## Scope

Run using `sol-env [path] --env [env]`. If `path` is a file, `sol-env` will run on that file. If `path` is a directory, `sol-env` will operate on all `.sol` files in the `./contracts` immediate subdirectory.

## Files
- [tests](./test.py)
- [implemention](./sol_env.py)

## License

Unlicense. Use at your own risk.

[echidna]: https://github.com/crytic/echidna