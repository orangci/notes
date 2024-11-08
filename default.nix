{ pkgs ? import <nixpkgs> { } }:
pkgs.mkShell {
  buildInputs = with pkgs; [
    tailwindcss
    hugo
  ];

  shellHook = ''
    # tailwindcss -i css/owo.css -o css/uwu.css --watch
  '';
}
