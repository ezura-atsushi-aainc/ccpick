# Requirement
1. `Python` >= 3.7
2. `phpmd` as executable
# How to run
```
$ python ccpick.py --threshold 20 --repo-root ~/repos/path/to/product/app
$ python ccpick.py --csv --threshold 20 --repo-root ~/repos/path/to/app > ~/Desktop/cc_list.csv
```
# Command line options
```
$ python ccpick.py --help
usage: ccpick.py [-h] [--csv] [--desc] [--phpmd-path PHPMD_PATH] --repo-root REPO_ROOT [--sort-by-name] [--threshold THRESHOLD]

Cyclomatic Complexity Finder

options:
  -h, --help            show this help message and exit
  --csv                 Enable CSV output
  --desc                Sort by descend
  --phpmd-path PHPMD_PATH
                        Path to phpmd command
  --repo-root REPO_ROOT
                        Target repository root
  --sort-by-name        Sort by method/class name
  --threshold THRESHOLD
                        Threshold of cyclomatic complexity for checking
```
