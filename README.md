# ComposableServices

## About
- The idea is that services here are built by simultenously executing a set of "command pipelines," where a command pipeline is a sequence of commands that run with stdout of predecesors piped into the stdin of the successors.
- A WIP
- Still some things hard coded in the scripts that should be moved to CLI args

## Philosophy
- Make services that do stuff by reusing little pieces of code
- Have a config file that holds comments and the relationships of these components as a service.
- They share data through pipes natively but other ideas can be implemented

## Directory of scripts
- delete.py: used to maintain freespace where logs or video files from sec cameras are continuously writing to disk
- check.py: used to close ffmpeg by sending a q for when an rtsp server quits sending data and ffmpeg gets hung

## Why
- I have a lot of backend stuff that works like this: long-running, kit-bashed scripts, and this just works and with low maintenance
- Little pieces can be improved or re-written even in other languages just fine
- A lot of flow-control and scheduling headache can be delegated to OS pipes and buffers

## Looking ahead
- Anyone is free to use. PRs welcome. I'll improve these as time permits.
