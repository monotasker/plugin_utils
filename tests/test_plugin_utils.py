#! /usr/bin/python
# -*- coding: UTF-8 -*-
"""
 Unit tests for the plugin_utils module

 Configuration and some fixtures
 the file tests/conftest.py
 run with py.test -xvs path/to/tests/dir

"""

import pytest
import plugin_utils


'''
#@pytest.fixture(params=[n for n in range(4)])
#def myfixture(request, myotherfixture):
    #"""
    #A pytest fixture providing a Classname object for testing.
    #"""
    #case = request.param
    #data = myotherfixture[case]
    #return Classname(**data)
'''


@pytest.mark.parametrize('mydata,myexpected', [
    ([1, 2],
     [1, 2]),
    ('a',
     ['a']),
    ('mystring',
     ['mystring']),
    (123,
     [123])
])
def test_islist(mydata, myexpected):
    """
    Unit test for flatten() utility function.
    """
    data = mydata
    expected = myexpected
    actual = plugin_utils.islist(data)
    assert actual == expected


@pytest.mark.parametrize('mydata,myexpected', [
    ([[17L], [86L, 129L], [72L, 82L, 69L], [84L, 1L], [10L, 2L], [61L, 77L],
      [87L, 77L], [72L, 82L, 69L], [63L, 61L, 62L, 84L, 1L],
      [63L, 61L, 66L, 62L, 128L, 10L, 2L], 76L, 76L, 72L, 89L, 122L, [67L], [67L],
      [], [], [2L, 122L, 128L]
      ],
     [17L, 86L, 129L, 72L, 82L, 69L, 84L, 1L, 10L, 2L, 61L, 77L, 87L, 77L, 72L,
      82L, 69L, 63L, 61L, 62L, 84L, 1L, 63L, 61L, 66L, 62L, 128L, 10L, 2L, 76L,
      76L, 72L, 89L, 122L, 67L, 67L, 2L, 122L, 128L]
     ),  # end of first input
    (['a', ['x', 'y', 'z'], (1, 2, ['e', 'f'])],
     ['a', 'x', 'y', 'z', 1, 2, 'e', 'f']
     )  # end of second
])
def test_flatten(mydata, myexpected):
    """
    Unit test for flatten() utility function.
    """
    data = mydata
    expected = myexpected
    actual = plugin_utils.flatten(data)
    assert actual == expected


@pytest.mark.parametrize('string_in,equivs,string_out',
                         [('happiness',
                           {'h': 'd',
                            'a': 'i',
                            'p': 'z'},
                           'dizziness'),
                          (u'ἀποκρινομαι',
                           {'οκ': 'εκ',
                            'ρ': 'δ',
                            'ιν': 'εχ'},
                           u'ἀπεκδεχομαι'),
                          ])
def test_multiple_replace(string_in, equivs, string_out):
    """
    Unit test for multiple_replace() utility function.
    """
    actual = plugin_utils.multiple_replace(string_in, equivs)
    print 'string in', string_in
    print 'actual', actual
    print 'expected', string_out
    print 'equivs', equivs
    assert actual == string_out
