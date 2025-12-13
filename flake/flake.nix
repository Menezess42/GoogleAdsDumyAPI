{
    descritpion = "Dumy to mimicate the Google Ads API"

        inputs = {
            nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
            flake-utils.url = "github:numtide/flake-utils";
            essentials.url = "path:/mnt/hdmenezess42/GitProjects/flakeEssentials";
        };
    outputs = {self, nixpkgs, flake-utils, essentials}:
        flake-utils.lib.eachDefaultSystem(system:
                let
                pkgs = import nixpkgs {inherit system; };
                baseShell = essentials.devShells.${system}.python;
                in
                {
                devShell = pkgs.mkShell {
                name = "GoogleAdsDumyAPI";
                buildInputs = with pkgs; [
                (python313.withPackages (p:
                                         [
                                         #faker
                                         #pydantic
                                         #pytest
                                         #pytest-cov
                                         #dataclasses-json
                                         ]))
                ] ++ baseShell.buildInputs;

                dontUsePytestCheck = true;
                doCheck = false;

                shellHook = ''
                echo "You can start build the Google Dumy API"
                '';
                };
                });
}
