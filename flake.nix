{
    description = "Dummy to mimicate the Google Ads API";
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
                
                gad-api = pkgs.python313Packages.buildPythonPackage {
                    pname = "googleAdsDummy";
                    version = "0.1.0";
                    pyproject = true;
                    src = pkgs.lib.cleanSourceWith {
                        src = ./.;
                        filter = path: type:
                            let baseName = baseNameOf path;
                            in !(builtins.elem baseName [ ".direnv" ".git" "htmlcov" "htmlTestsReports" ".pytest_cache" ]);
                    };
                    build-system = with pkgs.python313Packages; [ setuptools ];
                    propagatedBuildInputs = with pkgs.python313Packages; [
                        faker
                        faker_commerce
                        pydantic
                        pandas
                    ];
                    doCheck = false;
                };
                
                in
                {
                devShell = pkgs.mkShell {
                name = "GoogleAdsDummyAPI";
                buildInputs = with pkgs; [
                (python313.withPackages (p:
                                         [
                                         p.faker
                                         faker_commerce
                                         p.pydantic
                                         p.pytest
                                         p.pytest-cov
                                         p.pytest-html
                                         p.pandas
                                         gad-api
                                         ]))
                ] ++ baseShell.buildInputs;
                dontUsePytestCheck = true;
                doCheck = false;
                shellHook = ''
                    echo "You can start build the Google Dummy API"
                    '';
                };
                });
}

# {
#     description = "Dummy to mimicate the Google Ads API";
#     inputs = {
#         nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
#         flake-utils.url = "github:numtide/flake-utils";
#         essentials.url = "path:/mnt/hdmenezess42/GitProjects/flakeEssentials";
#     };
#     outputs = {self, nixpkgs, flake-utils, essentials}:
#         flake-utils.lib.eachDefaultSystem(system:
#                 let
#                 pkgs = import nixpkgs {inherit system; };
#                 baseShell = essentials.devShells.${system}.python;
#                 
#                 faker_commerce = pkgs.python313Packages.buildPythonPackage rec {
#                     pname = "faker-commerce";
#                     version = "1.0.4";
#                     pyproject = true;
#                     src = pkgs.fetchPypi {
#                         inherit pname version;
#                         sha256 = "sha256-9T2gQUOrcHVEk/qXwMZPUgjI+PPFAnNRbuPK/Oo3KVM=";
#                     };
#                     build-system = with pkgs.python313Packages; [ setuptools ];
#                     propagatedBuildInputs = with pkgs.python313Packages; [ faker ];
#                     doCheck = false;
#                 };
#                 in
#                 {
#                 devShell = pkgs.mkShell {
#                 name = "GoogleAdsDummyAPI";
#                 buildInputs = with pkgs; [
#                 (python313.withPackages (p:
#                                          [
#                                          p.faker
#                                          faker_commerce
#                                          p.pydantic
#                                          p.pytest
#                                          p.pytest-cov
#                                          p.pytest-html
#                                          p.pandas
#                                          ]))
#                 ] ++ baseShell.buildInputs;
#                 dontUsePytestCheck = true;
#                 doCheck = false;
#                 shellHook = ''
#                     echo "You can start build the Google Dummy API"
#                     '';
#                 };
#                 });
# }
