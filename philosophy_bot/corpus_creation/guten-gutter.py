#!/usr/bin/env python

"""Usage: guten-gutter [--output-dir DIR] [OPTIONS] FILES

Cleans the Project Gutenberg boilerplate off of the given input files.
"""

import codecs
from optparse import OptionParser
import os
import re
import sys


#--------------- processors copied from t_rext.processors ---------------#


class Processor(object): 
    """An abstract base class that defines the protocol for Processor objects.
    """

    def __init__(self, iterable):
        """Given an iterable of objects, become an iterable of other objects.

        The two sets of objects need not be the same type.

        Note that a file-like object is an iterable of lines.
        """
        self._iterable = iterable
        self.errors = []

    @property
    def iterable(self):
        for thing in self._iterable:
            self.check_input_value(thing)
            yield thing

    def check_input_value(self, value):
        pass

    def has_failed(self, original, result):
        """Given two iterables, representing the input and the output
        of this Processor, return a boolean indicating whether we think
        this Processor has failed or not.
        """
        return False

    def __iter__(self):
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__


class LineProcessor(Processor):

    def check_input_value(self, value):
        assert isinstance(value, unicode)


class TrailingWhitespaceProcessor(LineProcessor):

    def __iter__(self):
        for line in self.iterable:
            yield line.rstrip()


class SentinelProcessor(LineProcessor):
    """Yields only those lines of the input between the start
    sentinel (exclusive) and the end sentinel (exclusive.)
    
    The start sentinel is actually "super-exclusive" in that neither it,
    nor any non-blank lines immediately following it, are included in
    the output.

    Note that cleaned lines are stripped of trailing whitespace.
    """

    def __iter__(self):
        self.state = 'pre'
        for line in self.iterable:
            line = line.rstrip()
            if self.state == 'pre':
                match = re.match(self.START_RE, line.upper())
                if match:
                    self.state = 'consuming-start'
            elif self.state == 'consuming-start':
                if not line:
                    self.state = 'mid'
            elif self.state == 'mid':
                match = re.match(self.END_RE, line.upper())
                if match:
                    self.state = 'post'
                else:
                    yield line
            else:
                assert self.state == 'post'
                pass


class ComposedProcessor(LineProcessor):
    """A Processor which applies multiple Processors to an input in
    sequence.  If any Processor fails, it returns the result of
    processing only up to the point of the failure.
    """

    def __init__(self, lines, classes, name=''):
        LineProcessor.__init__(self, lines)
        self.classes = classes
        self.name = name

    def __iter__(self):
        lines = list(self.iterable)
        for cls in self.classes:
            filter_ = cls(lines)
            new_lines = list(filter_)
            if filter_.has_failed(lines, new_lines):
                self.errors.append("%s failed to clean '%s'" % (filter_, self.name))
                break
            lines = new_lines

        for line in lines:
            yield line


#-----------------------------------------------------------------------#


class GutenbergBoilerplateStripper(SentinelProcessor):
    START_RE = (
        r'^\**\s*('
        r'START\s+OF\s+(TH(IS|E)\s+)?PROJECT\s+GUTENBERG|'
        r'END.*?SMALL\s*PRINT'
        r').*?$'
    )
    END_RE = r'^\**\s*END\s+OF\s+(TH(IS|E)\s+)?PROJECT\s+GUTENBERG.*?$'

    def has_failed(self, original_lines, result_lines):
        original_lines = list(original_lines)
        result_lines = list(result_lines)
        shrinkage = len(original_lines) - len(result_lines)
        # usually under 400, but sometimes as high as 418...
        return len(result_lines) == 0 or shrinkage > 450


class ProducedByStripper(SentinelProcessor):
    # TODO: rewrite as a StartSentinelProcessor?
    START_RE = (r'^((THIS\s+)?E\-?(TEXT|BOOKS?)\s+(WAS\s+)?)?'
                '(PRODUCED|PREPARED|TRANSCRIBED|UPDATED|SCANNED|CREATED).*?$')
    END_RE = r'^\**\s*END\s+OF\s+(TH(IS|E)\s+)?PROJECT\s+GUTENBERG.*?$'

    def has_failed(self, original_lines, result_lines):
        original_lines = list(original_lines)
        result_lines = list(result_lines)
        shrinkage = len(original_lines) - len(result_lines)
        # Note: this is not sufficient by itself; it assumes that
        # GutenbergBoilerplateStripper already removed the trailing
        # legal text, which is large.
        return len(result_lines) == 0 or shrinkage > 20


class IllustrationStripper(LineProcessor):

    def __iter__(self):
        for line in self.iterable:
            match = re.match(r'^\s*\[Illustration.*?\]\s*$', line)
            if not match:
                yield line


### MAIN ###

optparser = OptionParser(__doc__.strip())
optparser.add_option("--strip-illustrations", default=False,
                     action='store_true',
                     help="also try to remove [Illustration: foo]'s")
optparser.add_option("--output-dir", default=None, metavar='DIR',
                     help="if given, save the resulting files to this "
                          "directory (under their original names) "
                          "instead of dumping them to standard output")
(options, args) = optparser.parse_args(sys.argv[1:])
print(len(args))

for filename in args:
    out = sys.stdout
    if options.output_dir is not None:
        out_filename = os.path.join(
            options.output_dir, os.path.basename(filename)
        )
        out = codecs.open(out_filename, 'w', encoding='UTF-8')
    with codecs.open(filename, 'r', encoding='UTF-8') as f:
        orchestrator = ComposedProcessor(f,
            [
                TrailingWhitespaceProcessor,
                GutenbergBoilerplateStripper,
            ] +
            ([IllustrationStripper] if options.strip_illustrations else []) +
            [
                ProducedByStripper,
            ],
            name=filename
        )
        for line in orchestrator:
            out.write(line + '\n')
        for error in orchestrator.errors:
            sys.stderr.write(error + '\n')
    if out is not sys.stdout:
        out.close()
