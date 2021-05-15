# sol-env

## Installation

The best way to install `sol-env` is cloning it with `git`, and making a symlink in your `$PATH`.

```bash
git clone https://github.com/hacker-dom/sol-env
ln -s $(pwd)/sol-env/sol_env.py [path-to-python3/bin/sol-env]
chmod 755 [path-to-python3/bin/sol-env]
```

## Motivation
There has been talk (e.g. [here[https://github.com/ethereum/solidity/issues/10825) and [here](https://github.com/ethereum/solidity/issues/8146)) about allowing better support for debug assertions in Solidity. Until that is implemented into Solidity and/or current tooling (and for versions prior to the implementation), this simple utility aspires to be a temporary solution.

`sol-env` allows you to switch between different environments for your Solidity code. There are many examples when this would be useful. You might want to have multiple environments: one for unit and [Echidna](https://github.com/crytic/echidna) tests, one for running `console.log`s with [hardhat](https://github.com/nomiclabs/hardhat), and one for production.

It is easily imaginable that there will be small differences in the code between these environments. Solidity currently doesn't allow you to do that; `sol-env` does!

## Examples

Here are some examples:

```solidity
// if our mental model of our system is correct,
// the path condition to get to this line contains this requirement
// nevertheless, we write an assertion, so that our hard-coded concrete
// and Echidna fuzz tests will alert us if our assumption is wrong
assert(isAllowedlisted[user]); // sol-env:console-log,tests
```

```
// here we "know" that this can't underflow,
// but we add an assert so that anytime during development,
// if this fails, we will be notified
assert(balance - amountOwed <= balance); // sol-env:console-log,tests
```

```
library Foo {
  function foo()
    // for tests use this library internally so we don't have to link it
    internal // sol-env:console-log,tests
    // in production use this as an external library due to EIP-170
    // external  // sol-env:production
    returns (uint)
  {
    [...]
  }
```


```
// console.log("Module:swap called with %s", inputValue) // sol-env:console-log
[...]
// console.log("Module:swap returning %s", outputValue) // sol-env:console-log
```

## Setup

To use `sol-env`, put a postfix of "// sol-env:A,B,C" after any Solidity line. When you run `sol-env`, you specify an environment. If the environment is A, B or C, then `sol-env` will activate this line. This means that if it is commented (in particular, if the first non-whitespace character gives rise to '// '), then it will remove that '// '.[1] And vice versa.

[1] Note that this also means that if you have multiple comment segments such as

```
//   // _checkState() // sol-env:production
```

and you run it with `--env production` *twice*, `sol-env` will remove both ocurrences. As such, it is not recommended to have adjacent sections of '// '.

## Scope

Run using `sol-env [path] --env [env]`. If `path` is a file, `sol-env` will run on that file. If `path` is a directory, `sol-env` will operate on all `.sol` files in the `./contracts` immediate subdirectory.

## Files
- [tests](./test.py)
- [implemention](./sol_env.py)

## License

Unlicense. Use at your own risk.