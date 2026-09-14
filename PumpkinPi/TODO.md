Were going to make it so the PumpkinPi part of the package can be installed via `pip`.
Once installed, the user should be able to run a command with the signature:
```pumpkinpi <subcommand> [options]```
or
```pumpkinpi --help```
to see, among other things, a list of subcommands to run.  Said subcommands are the names of scripts
found in the RemoteRPi/PumpkinPi subpackage.
The first signature should run `python3 <subcommand>.py [options]`. 