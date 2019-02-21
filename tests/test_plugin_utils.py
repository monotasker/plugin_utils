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
    ([[17], [86, 129], [72, 82, 69], [84, 1], [10, 2], [61, 77],
      [87, 77], [72, 82, 69], [63, 61, 62, 84, 1],
      [63, 61, 66, 62, 128, 10, 2], 76, 76, 72, 89, 122, [67], [67],
      [], [], [2, 122, 128]
      ],
     [17, 86, 129, 72, 82, 69, 84, 1, 10, 2, 61, 77, 87, 77, 72,
      82, 69, 63, 61, 62, 84, 1, 63, 61, 66, 62, 128, 10, 2, 76,
      76, 72, 89, 122, 67, 67, 2, 122, 128]
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
                          ('ἀποκρινομαι',
                           {'οκ': 'εκ',
                            'ρ': 'δ',
                            'ιν': 'εχ'},
                           'ἀπεκδεχομαι'),
                          ])
def test_multiple_replace(string_in, equivs, string_out):
    """
    Unit test for multiple_replace() utility function.
    """
    actual = plugin_utils.multiple_replace(string_in, equivs)
    print('string in', string_in)
    print('actual', actual)
    print('expected', string_out)
    print('equivs', equivs)
    assert actual == string_out
