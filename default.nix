{pkgs ? import <nixpkgs> {}}:
pkgs.mkShell {
  buildInputs = with pkgs; [
    nodejs
    python313
    python313Packages.virtualenv
  ];

  shellHook = ''
    if [ ! -d "venv" ]; then
      python -m venv venv
      source venv/bin/activate
      pip install --upgrade pip
      pip install -r requirements.txt
    else
      source venv/bin/activate
    fi
    python3 main.py
  '';
}
