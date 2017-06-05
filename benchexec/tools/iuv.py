"""
BenchExec is a framework for reliable benchmarking.
This file is part of BenchExec.

Copyright (C) 2007-2017  Dirk Beyer
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


class Tool(benchexec.tools.template.BaseTool):
    """
    Tool info for IUV (Input Using Verifier) .
    """

    REQUIRED_PATHS = [
                "iuv",
                "klee",
                "crest",
                "cpatiger",
                "lib",
                "run_iuv",
                "ReachSafety.prp"
    ] + ['validators/uautomizer/' + p for p in uautomizer.Tool.REQUIRED_PATHS]\
      + ['validators/cpachecker/' + p for p in cpachecker.Tool.REQUIRED_PATHS]

    def executable(self):
        return util.find_executable('run_iuv')


    def version(self, executable):
        """
        The output looks like this:
        IUV 0.1, using:
        KLEE 0.2.0 (https://klee.github.io),
        CREST f5ff7fc (http://www.burn.im/crest),
        LLVM version 3.4.2
        """
        stdout = self._version_from_tool(executable)
        return stdout.strip()


    def name(self):
        return 'IUV'


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
            if line.startswith('ERROR:'):
                return "ERROR ({0})".format(returncode)
            elif line.startswith('IUV: FALSE'):
                return result.RESULT_FALSE_REACH
            elif line.startswith('IUV: TRUE'):
                return result.RESULT_TRUE
        return result.RESULT_UNKNOWN

    def get_value_from_output(self, lines, identifier):
      for line in reversed(lines):
        if identifier in line:
          start = line.find(':') + 1
          end = line.find('(', start)
          return line[start:end].strip()
      return None
