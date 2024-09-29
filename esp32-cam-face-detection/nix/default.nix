{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python311
    pkgs.python311Packages.numpy
    pkgs.python311Packages.opencv4
    pkgs.python311Packages.pyserial
    pkgs.python311Packages.matplotlib
  ];

  shellHook = ''
    echo "Nix environment ready for ESP32-CAM Face Detection"
  '';
}
