{
  description = "Ray CLI is a command-line engineering utility for generating and broadcasting DMX data over sACN and Art-Net.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs = {
        pyproject-nix.follows = "pyproject-nix";
        nixpkgs.follows = "nixpkgs";
      };
    };

    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs = {
        pyproject-nix.follows = "pyproject-nix";
        uv2nix.follows = "uv2nix";
        nixpkgs.follows = "nixpkgs";
      };
    };
  };

  outputs =
    {
      self,
      nixpkgs,
      uv2nix,
      pyproject-nix,
      pyproject-build-systems,
    }:
    let
      system = "aarch64-darwin";
      pkgs = nixpkgs.legacyPackages.${system};

      workspace = uv2nix.lib.workspace.loadWorkspace {
        workspaceRoot = ./.;
      };

      overlay = workspace.mkPyprojectOverlay {
        sourcePreference = "wheel";
      };

      python = pkgs.python311;

      pythonSet =
        (pkgs.callPackage pyproject-nix.build.packages {
          inherit python;
        }).overrideScope
          (
            pkgs.lib.composeManyExtensions [
              pyproject-build-systems.overlays.default
              overlay
            ]
          );

    in
    {
      packages.${system}.default = pythonSet.mkVirtualEnv "ray-cli-env" workspace.deps.default;

      apps.${system}.default = {
        type = "app";
        program = "${self.packages.${system}.default}/bin/ray-cli";
      };

      devShells.${system}.default = pkgs.mkShell {
        name = "ray-cli-dev";

        packages = [
          pkgs.uv
          python
        ];

        shellHook = ''
          export UV_PYTHON=${python.interpreter}
          unset PYTHONPATH

          uv sync --quiet
          source .venv/bin/activate
        '';
      };
    };
}
