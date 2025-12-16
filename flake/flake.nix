{
    description = "Dumy to mimicate the Google Ads API";
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
                
                faker_commerce = pkgs.python313Packages.buildPythonPackage rec {
                    pname = "faker-commerce";
                    version = "1.0.4";
                    pyproject = true;
                    src = pkgs.fetchPypi {
                        inherit pname version;
                        sha256 = "sha256-9T2gQUOrcHVEk/qXwMZPUgjI+PPFAnNRbuPK/Oo3KVM=";
                    };
                    build-system = with pkgs.python313Packages; [ setuptools ];
                    propagatedBuildInputs = with pkgs.python313Packages; [ faker ];
                    doCheck = false;
                };
                in
                {
                devShell = pkgs.mkShell {
                name = "GoogleAdsDumyAPI";
                buildInputs = with pkgs; [
                (python313.withPackages (p:
                                         [
                                         p.faker
                                         faker_commerce
                                         p.pydantic
                                         p.pytest
                                         p.pytest-cov
                                         p.pandas
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
