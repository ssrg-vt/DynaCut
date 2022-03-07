# Dynamic and Adaptive Code Customization with Process Rewriting

## Intro
This project aims to dynamically customize code of a running process. The major component is an extended CRIU/CRIT tool that can rewrite the saved process images.
This repo contains a modified version of CRIU that can edit a process, disable code path, and insert library pages to a process at arbitrary VMA location.

Table of Contents
---
   * [<a href="docs/build_dynacut.md">Build DynaCut</a>](#build-dynacut)
   * [<a href="docs/customize_toy_program.md">Dynamically remove unwanted features for a toy program</a>](#dynamically-remove-unwanted-features-for-a-toy-program)
   * [<a href="docs/customize_servers.md">Dynamically remove unwanted features for server applications</a>](#dynamically-remove-unwanted-features-for-server-applications)
   * [<a href="docs/init_removal_toy_program.md">Remove initialization code for a toy example</a>](#remove-initialization-code-for-a-toy-example)
   * [<a href="docs/init_removal_servers.md">Remove initialization code for server applications</a>](#remove-initialization-code-for-server-applications)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc). (To generate the ToC of README.md, just run `./gh-md-toc README.md`)

## [Build DynaCut](docs/build_dynacut.md)

## [Dynamically remove unwanted features for a toy program](docs/customize_toy_program.md)

## [Dynamically remove unwanted features for server applications](docs/customize_servers.md)

## [Remove initialization code for a toy example](docs/init_removal_toy_program.md)

## [Remove initialization code for server applications](docs/init_removal_servers.md)