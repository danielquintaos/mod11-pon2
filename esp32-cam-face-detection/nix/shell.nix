let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  buildInputs = [
    pkgs.python311
    pkgs.python311Packages.opencv4
    pkgs.python311Packages.numpy
    pkgs.python311Packages.pyserial
  ];

  shellHook = ''
    echo "Welcome to the ESP32-CAM Face Detection Shell!"
  '';
}
