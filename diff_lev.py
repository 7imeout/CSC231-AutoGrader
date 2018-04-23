import sys, re, Levenshtein

def cmp(ref_file_path, sub_file_path):
    try:
        ref = open(ref_file_path)
        ref_str = re.sub('\s', '', ''.join(ref.readlines()))

        sub = open(sub_file_path)
        sub_str = re.sub('\s', '', ''.join(sub.readlines()))
    except:
        print('Error occurred while opening one or more of:\n    {}\n    {}'.format(
            ref_file_path, sub_file_path
        ), file=sys.stderr, end='\n\n')
        return -1.0

    d = Levenshtein.distance(ref_str, sub_str)
    return max((len(ref_str) - d) / len(ref_str), 0.00)