{pkgs ? import <nixpkgs> {}}:
pkgs.mkShell {
  buildInputs = with pkgs; [
    tailwindcss
    hugo
  ];

  shellHook = ''
    # tailwindcss -i css/owo.css -o themes/archie/assets/css/uwu.css --watch
    hugo new content/posts/00.md
    codium .
    codium content/posts/00.md
    firefox http://localhost:1313
    hugo server
  '';
}
