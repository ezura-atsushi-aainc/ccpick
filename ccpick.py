# -*- coding: utf-8 -*-
from pathlib import Path
from typing import List, Set, Dict, Any
import argparse
import json
import subprocess
import sys

argparser = argparse.ArgumentParser(description='Cyclomatic Complexity Finder')

argparser.add_argument('--csv', action='store_true', help='Enable CSV output', required=False)
argparser.add_argument('--repo-root', type=str, help='Target repository root', required=True)
argparser.add_argument('--threshold', type=int, help='Threshold of cyclomatic complexity for checking', required=False, default=10)
args = argparser.parse_args()

enableCsv: bool = args.csv
repoRoot: str = args.repo_root
ccThreshold: int = args.threshold

dir = Path(repoRoot)
php_files = dir.rglob('*.php')

# Initialize for report violations
class_cyclomatic_complexity = {}

for php_file in php_files:
    result: Dict[str, Any] = subprocess.run(['phpmd', php_file, 'json', 'codesize'], capture_output=True, text=True)
    ripped_result: Dict[str, Any] = json.loads(result.stdout)['files']
    if not ripped_result:
        continue

    cc_result = ripped_result[0]
    cc_file: str = cc_result['file']
    for violation in cc_result['violations']:
        cc_package: str = '' if violation['package'] is None else violation['package']
        cc_class: str   = '' if violation['class'] is None else violation['class']
        cc_method: str  = '' if violation['method'] is None else violation['method']
        cc_desc: str    = '' if violation['description'] is None else violation['description']

        cc_name = cc_package + '\\' + cc_class + '\\' + cc_method

        # parse description
        words = cc_desc.split(' ')
        if words[3] != 'has':
            continue
        num = 1 if words[4] in ('a', 'an') else int(words[4])

        if words[5].lower() == 'cyclomatic':
            cc = int(words[8].split('.')[0])
            if cc >= ccThreshold:
                class_cyclomatic_complexity[cc_name] = cc

for name, cc in sorted(class_cyclomatic_complexity.items()):
    if enableCsv:
        print(f'{cc},{name}')
    else:
        print(f'{name}: {cc}')
