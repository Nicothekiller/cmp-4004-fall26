{
  description = "CMP-4004 HW3 development shell";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in {
      devShells.${system}.default = pkgs.mkShell {
        packages = [ (pkgs.python3.withPackages (ps: [
          ps.numpy
          ps.matplotlib
          ps.pytest
          ps.ipykernel
        ])) ];
      };
    };
}
