# Dynamic and Adaptive Code Customization with Process Rewriting

## Intro
This project aims to dynamically customize code of a running process. The major component is an extended CRIU/CRIT tool that can rewrite the saved process images.

This repo contains a modified version of [DynamoRIO](https://dynamorio.org/) to dump code coverage of execution phases, and a modified version of [CRIU](https://criu.org/) that can edit a process, disable code path, and insert library pages to a process at arbitrary VMA location.

## [Build DynaCut](docs/build_dynacut.md)

## [Dynamically remove unwanted features for a toy program](docs/customize_toy_program.md)

## [Dynamically remove unwanted features for server applications](docs/customize_servers.md)

## [Remove initialization code for a toy example](docs/init_removal_toy_program.md)

## [Remove initialization code for server applications](docs/init_removal_servers.md)