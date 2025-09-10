+++
title = "Nix(OS) Sucks"
desc = "Some thoughts on Nix/NixOS, and why it sucks— but is better than everything else."
date = "2025-04-28"
edited = "2025-09-10"
+++

I have been using NixOS since — according to the date of the earliest commit in my [dotfiles](https://orangc.net/dots) repository — September 8th, 2023. I started by using a barebones `configuration.nix` and a [decent enough rice](../assets/old-nix-kde-rice.png). I eventually switched to using flakes by forking [ZaneyOS](https://gitlab.com/Zaney/zaneyos), then, a few months later, scrapping it and writing my own [flake](https://orangc.net/dots).

Nix is a: reproducible and declarative Linux distribution (NixOS), package manager (the package repository is called Nixpkgs), and language (Nix). This means that with Nix/NixOS/Nixpkgs:

- Replicate your configuration on one machine to any other machine.
- In Nix, programs, settings, "dotfiles", and much more are all configured *declaratively* in a `.nix` file, as opposed to setting things up *imperatively* via commands in the CLI, leading to a much more consistent and easier to understand system configuration.
- Access to the largest package repository on Earth — nixpkgs.[^1]
- Portable; run Nix on any Linux distribution or even MacOS.
- Immutability.
- Easy to package programs if they aren't in nixpkgs.
- Easily try out new packages without installing them (e.g. `nix run nixpkgs#firefox`).
- Nix uses binary caches so you rarely have to compile anything; it's also easy to set up your own binary cache up.
- Nix solves dependency hell. You can mix and match different versions of packages without any conflicts.
- Rollbacks are builtin and enabled by default. Did you break.. everything? Don't sweat it; restart your computer and boot into an older version of your configuration.
- Cirno is (definitely and absolutely) the real (100%) NixOS mascot. This is extremely important.
- And much more.

Nix has its downsides too, of course.

1. The documentation tends to suck. —On that note, here are some resources for beginners:
    - Official: [NixOS Wiki](https://wiki.nixos.org/wiki/NixOS_Wiki) / [NixOS Manual](https://nixos.org/manual/nixos/unstable/) / [Nixpkgs Manual](https://nixos.org/manual/nixpkgs/unstable/) / [Nix Manual](https://nix.dev/manual/nix/2.28/)
    - [Ian Henry's NixOS Guide](https://ianthehenry.com/posts/how-to-learn-nix/introduction/)
    - [NixOS & Flakes Book](https://nixos-and-flakes.thiscute.world/)
    - [Home Manager Options Search](https://nix-community.github.io/home-manager/options.xhtml)
    - [Noogle](https://noogle.dev)
    - [Awesome-Nix](https://nix-community.github.io/awesome-nix/)
    - [An alternative to home-manager: hjem](https://github.com/feel-co/hjem/)
    - [NixOS Flake Templates](https://github.com/NixOS/templates)
    - [nix-shorts](https://github.com/justinwoo/nix-shorts)
2. ***Steep*** learning curve.[^2]
3. NixOS is very different from other Linux distributions. The problems you face will be niche, poorly documented, and you'll struggle. Things that work on Arch won't work on Nix.
4. Massive time sink. 
5. Refer to [Hlissner's thoughts on NixOS](https://github.com/hlissner/dotfiles?tab=readme-ov-file#frequently-asked-questions).

Long live Nix(OS).

[^1]: Source: [Repology](https://repology.org/repositories/statistics/total).
[^2]: [This](../assets/nix-learning-curve-of-doom.png) graph does an accurate job of portraying the Nix learning curve.