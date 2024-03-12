# -*- coding: utf-8 -*-
from pathlib import Path
from typing import List, Set, Dict, Any
import json
import subprocess
import sys

args: List[str] = sys.argv
repoRoot: str = args[1] if len(args) >= 2 else '.'
rule: str = args[2] if len(args) >= 3 else 'codesize'

dir = Path(repoRoot)
php_files = dir.rglob('*.php')

# Initialize for report violations
# class_excessive_class_length  = {}
# class_excessive_method_length = {}
# class_too_many_methods        = {}
# class_too_many_public_methods = {}
# class_too_many_fields         = {}
class_cyclomatic_complexity   = {}
# class_npath_complexity        = {}

for php_file in php_files:
    result: Dict[str, Any] = subprocess.run(['phpmd', php_file, 'json', rule], capture_output=True, text=True)
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

        # print(cc_desc)
        # The class User has 1200 lines of code. Consider refactoring User to keep number of lines under 1000.
        # The method processOrder has 150 lines of code. Consider refactoring processOrder to keep number of lines under 100.
        # The method createReport has 6 parameters. Consider reducing the number of parameters on method createReport to under 5.
        # The class Product has 25 methods. Consider refactoring Product to keep number of methods under 20.
        # The class FacebookGraphClient has 11 public methods. Consider refactoring FacebookGraphClient to keep number of public methods under 10.
        # The class Order has 22 fields. Consider refactoring Order to keep the number of fields under 15.
        # The method calculateScore has a cyclomatic complexity of 16. The configured cyclomatic complexity threshold is 10.
        # The method renderView has an NPath complexity of 1024. The configured NPath complexity threshold is 200.

        # parse description
        words = cc_desc.split(' ')
        if words[3] != 'has':
            continue
        num = 1 if words[4] in ('a', 'an') else int(words[4])

        if words[5].lower() == 'cyclomatic':
            cc = words[8].split('.')[0]
            class_cyclomatic_complexity[cc_name] = int(cc)

for name, cc in sorted(class_cyclomatic_complexity.items()):
    print(f'{cc},{name}')

# Output sample
# {'version': '2.14.1snapshot202309281310', 'package': 'phpmd', 'timestamp': '2024-01-26T09:54:26+00:00', 'files': [{'file': '/Users/ezura.atsushi/repos/letro/main/letro/app/Services/AdvertiserService.php', 'violations': [{'beginLine': 899, 'endLine': 965, 'package': 'App\\Services', 'function': None, 'class': 'AdvertiserService', 'method': 'getDailyLapByKpi', 'description': 'The method getDailyLapByKpi() has a Cyclomatic Complexity of 21. The configured cyclomatic complexity threshold is 15.', 'rule': 'CyclomaticComplexity', 'ruleSet': 'Code Size Rules', 'externalInfoUrl': 'https://phpmd.org/rules/codesize.html#cyclomaticcomplexity', 'priority': 1}, {'beginLine': 1181, 'endLine': 1239, 'package': 'App\\Services', 'function': None, 'class': 'AdvertiserService', 'method': 'calculateDailyUgcSetAbtestPatterns', 'description': 'The method calculateDailyUgcSetAbtestPatterns() has a Cyclomatic Complexity of 16. The configured cyclomatic complexity threshold is 15.', 'rule': 'CyclomaticComplexity', 'ruleSet': 'Code Size Rules', 'externalInfoUrl': 'https://phpmd.org/rules/codesize.html#cyclomaticcomplexity', 'priority': 1}, {'beginLine': 1241, 'endLine': 1292, 'package': 'App\\Services', 'function': None, 'class': 'AdvertiserService', 'method': 'calculateDailyTargetRateAbtestPattern', 'description': 'The method calculateDailyTargetRateAbtestPattern() has a Cyclomatic Complexity of 27. The configured cyclomatic complexity threshold is 15.', 'rule': 'CyclomaticComplexity', 'ruleSet': 'Code Size Rules', 'externalInfoUrl': 'https://phpmd.org/rules/codesize.html#cyclomaticcomplexity', 'priority': 1}, {'beginLine': 1303, 'endLine': 1412, 'package': 'App\\Services', 'function': None, 'class': 'AdvertiserService', 'method': 'calculateWeeklyUgcSetAbtestPatterns', 'description': 'The method calculateWeeklyUgcSetAbtestPatterns() has a Cyclomatic Complexity of 33. The configured cyclomatic complexity threshold is 15.', 'rule': 'CyclomaticComplexity', 'ruleSet': 'Code Size Rules', 'externalInfoUrl': 'https://phpmd.org/rules/codesize.html#cyclomaticcomplexity', 'priority': 1}, {'beginLine': 1456, 'endLine': 1551, 'package': 'App\\Services', 'function': None, 'class': 'AdvertiserService', 'method': 'prepareUgcSetAbtestPatternsGroupByPeriod', 'description': 'The method prepareUgcSetAbtestPatternsGroupByPeriod() has a Cyclomatic Complexity of 22. The configured cyclomatic complexity threshold is 15.', 'rule': 'CyclomaticComplexity', 'ruleSet': 'Code Size Rules', 'externalInfoUrl': 'https://phpmd.org/rules/codesize.html#cyclomaticcomplexity', 'priority': 1}]}]}
