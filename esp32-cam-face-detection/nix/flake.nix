{
  description = "ESP32-CAM Face Detection Environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }: {
    devShell = nixpkgs.lib.mkShell {
      packages = with nixpkgs; [
        python311            # Python 3.11
        python311Packages.opencv4  # OpenCV for face detection
        python311Packages.numpy    # Numpy for numerical operations
        python311Packages.pyserial # pySerial to communicate with ESP32
        python311Packages.matplotlib # Optional: For image plotting
      ];

      shellHook = ''
        echo "Welcome to the ESP32-CAM Face Detection Environment!"
      '';
    };
  };
}
