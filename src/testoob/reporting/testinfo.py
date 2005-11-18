# TestOOB, Python Testing Out Of (The) Box
# Copyright (C) 2005 The TestOOB Team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class TestInfo:
	"""
	An interface for getting information about tests.
	Reporters receive instances of this class.

	Instances are pickleable.
	"""
	def __init__(self, test):
		failure_exception_type = test.failureException # TODO: do we need this?

class TestInfo:
    def __init__(self, fixture):
        self.fixture = fixture
    
    def module(self):
        return self.fixture.__module__

    def filename(self):
        import sys
        try:
            return sys.modules[self.module()].__file__
        except KeyError:
            return "unknown file"

    def classname(self):
        return self.fixture.__class__.__name__

    def funcname(self):
        # parsing id() because the function name is a private fixture field
        return self.fixture.id().split(".")[-1]

    def docstring(self):
        if getattr(self.fixture, self.funcname()).__doc__:
            return getattr(self.fixture, self.funcname()).__doc__.splitlines()[0]
        return ""

    def funcinfo(self):
        return (self.funcname(), self.docstring())
