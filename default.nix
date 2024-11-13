{ pkgs ? import <nixpkgs> { } }:
pkgs.mkShell {
  buildInputs = with pkgs; [
    tailwindcss
    hugo
  ];

  shellHook = ''
      tailwindcss -i css/owo.css -o themes/archie/assets/css/uwu.css --watch
  '';
}
