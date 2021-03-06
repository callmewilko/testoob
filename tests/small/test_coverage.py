"coverage tests"

import helpers

from os.path import abspath

from unittest import TestCase

import coverage_sample_module as sample
import coverage_sample_module2 as sample2

import testoob

class SimpleStub:
    def __getattr__(self, name):
        setattr(self, name, SimpleStub())
        return getattr(self, name)

class CoverageTest(TestCase):
    def setUp(self):
        helpers.ensure_coverage_support()
        from testoob.coverage import Coverage
        self.coverage = Coverage()
    def tearDown(self):
        del self.coverage

class unit_tests(CoverageTest):
    "Small-grain tests for Coverage"

    sample_coverage_dictionary = {
        abspath("one.py") : { "lines"   : range(100),
                              "covered" : range(30,100) },
        abspath("two.py") : { "lines"   : range(66),
                              "covered" : range(66) },
    }

    def test_total_lines(self):
        self.coverage.coverage = self.sample_coverage_dictionary.copy()
        self.assertEqual( 166, self.coverage.total_lines() )

    def test_total_lines_covered(self):
        self.coverage.coverage = self.sample_coverage_dictionary.copy()
        self.assertEqual( 136, self.coverage.total_lines_covered() )

    def test_total_coverage_percentage(self):
        self.coverage.coverage = self.sample_coverage_dictionary.copy()
        self.assertEqual( 81, self.coverage.total_coverage_percentage() )

    def test_should_cover_frame_path_to_ignore(self):
        self.coverage.ignorepaths = [abspath("/a/b/c")]

        mock_frame = SimpleStub()
        mock_frame.f_code.co_filename = "/a/b/c/blah.py"

        self.failIf( self.coverage._should_cover_frame(mock_frame) )

    def test_should_cover_frame_nonexecutable_line(self):
        self.coverage.coverage = self.sample_coverage_dictionary.copy()

        mock_frame = SimpleStub()
        mock_frame.f_code.co_filename = abspath("one.py")
        mock_frame.f_lineno = 1000 # out of the range of one.py's lines

        self.failIf( self.coverage._should_cover_frame(mock_frame) )

    def test_single_file_statistics(self):
        coverage_dict = {
            "lines"   : range(10),
            "covered" : range(5)
        }

        result = self.coverage._single_file_statistics(coverage_dict)
        self.assertEqual( 10, result["lines"] )
        self.assertEqual( 5, result["covered"] )
        self.assertEqual( 50, result["percent"] )


class system_tests(CoverageTest):
    "Large-grain tests for Coverage"

    def skip_if_no_coverage_support(self):
        if not testoob.capabilities.c.settrace:
            testoob.testing.skip("requires sys.settrace")
        if not testoob.capabilities.c.trace_coverage_support(sample.__file__.replace(".pyc", ".py")):
            testoob.testing.skip("requires coverage support from trace")
    
    def test_percentage_full(self):
        self.skip_if_no_coverage_support()
        self.coverage.runfunc(sample.foo, 5)
        self.assertEqual( 100, self.coverage.total_coverage_percentage() )

    def get_coverage_percentage(self, filename):
        statistics = self.coverage.getstatistics()
        coverage_percentage = 0
        for file_ in statistics:
            if file_.endswith(filename):
                coverage_percentage = statistics[file_]['percent']
        return coverage_percentage
        
    def test_multithreaded_coverage(self):
        self.skip_if_no_coverage_support()
        self.coverage.runfunc(sample2.multi_thread_func)
        self.assertEqual( 100, self.get_coverage_percentage('coverage_sample_module2.py') )

if __name__ == "__main__":
    import testoob
    testoob.main()
