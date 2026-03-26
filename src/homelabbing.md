+++
title = "The Joys of Homelabbing"
desc = "My long and happily fruitful journey with homelabbing."
date = "2026-03-26"
+++
*NOTE: Bit of a draft? Will update more later, I feel like I'm missing something but I'm not sure so I'll just publish it...*

A homelab is an at-home server, a computer setup usually physically inside your house and entirely under your control (or so you'd hope).

It's very useful for a wide assortment of things digitally, especially in this day and age, where mega-corporations all but force us to use their products and services, either at the price of your data and privacy (without your consent), your money, or both.

With a homelab, you can have a free and easy alternative to services such as Google Photos, Netflix, Microsoft Office, OneDrive, et cetera. Ones that you have complete and total control over.

I could go into a lot more detail about why homelabbing is amazing and you should definitely do it, but that's not the purpose of this article. I'm just here to explain how my homelab works, and maybe that'll inspire you in one way or another. Let's begin. 

## What It's For
The list of things I use my homelab for is long, and it only grows over time. You can see some of the services I host over at my [Glance dashboard](https://glance.orangc.net). Some of the notable ones are:

- [Immich](https://immich.app): An excellent alternative to Google Photos.
- Vaultwarden: Bitwarden, but selfhosted. I don't feel very safe with my passwords on someone else's server, somewhere.
- Cryptpad: All in one alternative to Google Docs, Slides, Sheets, et cetera.
- Forgejo: Alternative to GitHub.
- Ntfy: Possibly the most awesome thing on this list, one that I've yet to use to its fullest capabilities. Script with Ntfy to send notifications to your phone or to other places.
- Copyparty: An amazing file server. See it at work [here](https://orang.ci/walls) with my wallpaper collection.
- SearXNG: Alternative to Google itself, a search engine.
- Jellyfin: Organise and watch media of all sorts. With a torrenting setup, this is a superior alternative to Netflix.
- Technitium: Authoritative DNS server 
- Caddy: Web server responsible for reverse proxying all those services 
- Glance: Dashboard for keeping track of things 
- Zipline: Image server
- Microbin: Simple pastebin
- Umami: Privacy-respecting website analytics
- More that I will not list here.
- A Matrix homeserver 
- A Minecraft server

## Hardware
Running a homelab requires an at-home data center. You'll need the likes of Ryzen Threadrippers.. wait, wrong script! I'm sorry!

You can run a homelab on a potato, if your potato comes with an ethernet port. Unless you're running a heavy duty game server such as Minecraft, or selfhosting slopware (AI clankers), please don't fall under the illusion that you need any special hardware. At the time of writing, one of my friends uses some laptop as his homelab. Personally, I shilled out roughly 800 SAR to buy an HP EliteDesk mini PC. It's small, and that's mighty convenient. It rocks a modest Intel i5-6500T with integrated graphics and 32GIB of DDR4 RAM (I don't use all that RAM).

To recap: computer, ethernet cable (optional, but please, don't use WiFi). Not much else, really! Any spare computer will do. Optionally, an external storage solution of some sort, which I'll talk about later in this article.

## Networking
Everyone loves this part. It's the most enjoyable, soothing, even *relaxing* part of the homelabbing process. After all, nothing ever goes wrong with networking; it practically puts you to sleep.

Nobody has ever said that, but humour me a little...

My setup does not utilise port forwarding anywhere at all nor expose my public IP anywhere either, and good riddance to both of those things.

TODO: Draw a diagram for this because I am not very good at explaining things

Before I delve into my explanation, I'll quickly explain what Tailscale is and Cloudflare Tunnels are. 

Tailscale is a way of setting up your own little internet. With it, you create and use a tailnet, a P2P network of your devices (or your friends, if you give them access to your tailnet). As long as you're connected to your tailnet, from anywhere in the world, you're able to access other devices on it as if they're on your LAN. You can even use it as a VPN; use any device on your tailnet as an exit node. Via Tailscale Funnel, you can expose individual nodes to the wider web. 

Cloudflare Tunnels is a service run by Cloudflare that allows you to expose your services to the wider web without exposing your IP. This works by using Cloudflare servers as a middle man, which you go through (hence, "tunnels"). I don't particularly like Cloudflare, so I'm working on a way to stop relying on them.

Moving on to my explanation of my own networking setup, for this example I'll use Forgejo. It's served on http://localhost:8805, which is then reverse proxied by Caddy to both git.cormorant-emperor.ts.net (cormorant-emperor being the name of my tailnet), and https://git.orangc.net. The latter goes through Cloudflare Tunnels. The former, through Tailscale, and is only accessible to me.

I use the [caddy-tailscale plugin](https://GitHub.com/tailscale/caddy-tailscale) to serve multiple nodes on my tailnet at once from one device.

Some services which should be private are only available on my tailnet, and aren't accessible through a subdomain of orangc.net. Nobody needs to access my Immich instance, as only I need to see my own private photos.

While I like my current networking setup and it makes sense, I feel as though it isn't quite perfect yet. I'm planning on improving it further, perhaps by looking more into Netbird.

## Backups
As you might've ascertained at this point, I have a lot of important data on gensokyo (hostname of my homelab) that I cannot quite afford to lose.

Unfortunately, I do not have a way to backup my data off-site for now, so I cannot follow the 3-2-1 meta in full. However, I can at least do 3-2.

Via the amazing [restic](https://restic.net), I have daily automated backups to an external HDD plugged into my little server. Restic even supports snapshots and encryption, and that eases my paranoia even further.

For a third layer of redundancy, I also plug in a USB stick that I have every few weeks and backup Bitwarden, SSH keys, PGP keys, and anything of similar importance.

If anyone were to smash gensokyo with a hammer (please do not, my poor wallet!), I would not lose any data. I would also be able to bring it back to life in minutes on another computer because of NixOS reproducibility...

## Mandatory NixOS Shilling
Gensokyo runs on NixOS. I would say that perhaps the biggest portion of my NixOS flake is dedicated to server related modules, although I'm not quite sure about it.

I think that there is nowhere the advantages and perks of NixOS shine more than a server. Servers are devices that are much more unstable and volatile at least in my own experience; we're always tinkering with them, and often times move them from place to place, et cetera.

Declarativity makes this process so much easier. Especially with secrets management (long live sops-nix) for things like environment variables and passwords and more; secrets are encrypted and stored in a yaml file within my NixOS flake itself.

Modularity makes my server modules easily togglable. I can shrimply toggle off modules.server.immich.enable, and Immich is gone.

TODO: I did not do a good job of shilling Nix here
## Concluding Thoughts
Homelabbing is a deep rabbit hole that never truly ends. I've personally reached a situation where I'm happy with the current state of my homelab, but that by no means indicates that I'm content to now stop and say, "alright, I'll just let it run now, I won't mess with it anymore".

I'm absolutely going to mess with it! I'm going to tinker and tinker and continue improving it and also my skills, because it's really fun and I'm really addicted.
