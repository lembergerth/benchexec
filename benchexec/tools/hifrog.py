"""
BenchExec is a framework for reliable benchmarking.
This file is part of BenchExec.

Copyright (C) 2007-2018  Dirk Beyer
All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import benchexec.result as result
import benchexec.util as util
import benchexec.tools.template
import benchexec.tools.ultimateautomizer as uautomizer
import benchexec.tools.cpachecker as cpachecker
import logging

from benchexec.model import SOFTTIMELIMIT


class Tool(benchexec.tools.template.BaseTool):
    """
    Tool info for HiFrog.
    """

    REQUIRED_PATHS = [
        "lib", "bin", "include",
        "hifrog"
    ]

    def executable(self):
        return util.find_executable('hifrog')

    def version(self, executable):
        stdout = self._version_from_tool(executable)
        return stdout.strip()

    def name(self):
        return 'HiFrog'

    def determine_result(self, returncode, returnsignal, output, isTimeout):
        """
        Parse the output of the tool and extract the verification result.
        This method always needs to be overridden.
        If the tool gave a result, this method needs to return one of the
        benchexec.result.RESULT_* strings.
        Otherwise an arbitrary string can be returned that will be shown to the user
        and should give some indication of the failure reason
        (e.g., "CRASH", "OUT_OF_MEMORY", etc.).
        """
        for line in reversed(output):
            if line.startswith('Finally') and 'the program is' in line:
                if 'unsafe' in line.lower():
                    return result.RESULT_FALSE_REACH
                else if 'safe' in line.lower():
                    return result.RESULT_TRUE_PROP
        return result.RESULT_UNKNOWN

    def get_value_from_output(self, lines, identifier):
        for line in reversed(lines):
            if identifier in line:
                start = line.find(':') + 1
                end = line.find('(', start)
                return line[start:end].strip()
        return None
