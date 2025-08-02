with import <nixpkgs> {};

pkgs.mkShell {

  packages = [
    (pkgs.python313.withPackages (pp: with pp; [
      pyqt6
      pillow
    ]))
  ];
}
