'''
    Aristos Athens

    Get date and time data from unstructured text.
'''

from chronyk import Chronyk

def test(input_string):
    output = Chronyk(input_string)
    print(output)

if __name__ == "__main__":
    example_text = \
    '''
        Hi Kerry, can we schedule a meeting for tomorrow?
    '''
    test("December 15")
    test("tomorrow")
    test(example_text)