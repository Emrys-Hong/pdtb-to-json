import pandas as pd
from pathlib import Path
from collections import Counter
import os
import difflib
import math

def _get_files(data_path=DATA_PATH):
    """Returns (list): [('00', 'wsj_0000'), ..., ('24', 'wsj_2400']"""
    sections = os.listdir(data_path)
    ret = []
    for sec in sections:
        for filename in os.listdir(data_path/sec):
            ret.append((sec, filename))
    return ret

def get_batch(section, filenumber):
    """
    Args: 
            section(int)
            filenumber(int)
    Returns:
            (list[int]): list of index with all the file with the same format in that batch"""
    return pdtb2.index[(pdtb2['Section'] == section) & (pdtb2.FileNumber == filenumber)].tolist()


def _get_arg(char_span_list, rawtext):
    arg = ''
    for span in char_span_list:
        arg += rawtext[int(span[0])-2:int(span[1])-2]
    return arg

def _get_span_list(span):
    """
    Args:
            span(str): "34..96;97..101"
    Returns:
            ret(list[list[str]]):
            if one arg has one segment: [[34,96]]
            if one arg has two segment: example [[34, 96], [97, 101]]
    """
    if span == '':
        return []
    spans = span.split(';')
    return [[int(k) for k in o.split('..')] for o in spans ]

def check_number_of_errors():
    count = 0
    single = 0
    double = 0
    triple = 0
    files =  _get_files()
    for (section, filename) in files:
        with open(DATA_PATH/section/filename, encoding='latin-1') as f:
            rawtext = f.read()
            rawtext = rawtext.replace('\n', '')
        section = int(section)
        filenumber = int(filename[-2:])
        batch = get_batch(section, filenumber)
        for i in batch:
            # for arg1
            arg1_char_span_string = pdtb2.loc[i, 'Arg1_SpanList']
            arg1_char_span_list = _get_span_list(arg1_char_span_string)
            arg1_rawtext = pdtb2.loc[i, 'Arg1_RawText']
            if _get_arg(arg1_char_span_list, rawtext) != arg1_rawtext:
                if len(arg1_char_span_list) == 1:
                    single += 1
                elif len(arg1_char_span_list) == 2:
                    double += 1
                else:
                    triple += 1
    print("error numbers for arg1  single:", single, " double: ", double, " triple: ", triple)
    count = 0
    single = 0
    double = 0
    triple = 0
    files =  _get_files()
    for (section, filename) in files:
        with open(DATA_PATH/section/filename, encoding='latin-1') as f:
            rawtext = f.read()
            rawtext = rawtext.replace('\n', '')
        section = int(section)
        filenumber = int(filename[-2:])
        batch = get_batch(section, filenumber)
        for i in batch:
            # for arg2
            arg2_char_span_string = pdtb2.loc[i, 'Arg2_SpanList']
            arg2_char_span_list = _get_span_list(arg2_char_span_string)
            arg2_rawtext = pdtb2.loc[i, 'Arg2_RawText']
            if _get_arg(arg2_char_span_list, rawtext) != arg2_rawtext:
                if len(arg2_char_span_list) == 1:
                    single += 1
                elif len(arg2_char_span_list) == 2:
                    double += 1
                else:
                    triple += 1
    print("error numbers for arg2  single:", single, " double: ", double, " triple: ", triple)
    
def get_length(list):
    length = 0
    for o in list:
        length += o[1] - o[0]
    return length


def get_start_end(span_list, rawtext, tolerance_size):
    tolerance_size += 1
    start = span_list[0][0]
    end = span_list[len(span_list)-1][1]
    if start-tolerance_size<0:
        start = 0
    else:
        start -= tolerance_size
    if end + tolerance_size>len(rawtext)-1:
        end = len(rawtext) -1
    else:
        end += len(rawtext)+tolerance_size
    
    return start, end

def correct_span(span_list, arg_rawtext, rawtext):
    """
    Args: 
            span_list[list[[int, int], ...]]
            arg_rawtext(str)
            rawtext(str): doc raw text
    Returns: 
            corrected_span(str): [34, 39]
    """
    corrected_span = ''
    tolerance_size = abs(get_length(span_list) - len(arg_rawtext))
    start, end = get_start_end(span_list, rawtext, tolerance_size)

    s = difflib.SequenceMatcher(None, rawtext[start: end], arg_rawtext)
    for i, j, n in s.get_matching_blocks():
        if n!=0:
            corrected_span += f'{start+i+2}..{start+i+n+2};' # here is a offset of 2 char we need to consider
    corrected_span = corrected_span[:-1]
    return corrected_span

def sanity_check(corrected_span, rawtext, arg_rawtext):
    """Args: 
            corrected_span(str)
            rawtext(str): doc string
            arg_rawtext(str): gold argument string
    Returns: 
            (boolean): the corrected span is corrected"""
    span_list_corrected = _get_span_list(corrected_span)
    return _get_arg(span_list_corrected, rawtext) == arg_rawtext

def correct_docs():
    files =  _get_files()
    count = 0
    for (section, filename) in files:
        print('section:', section, ' files: ', filename)
        with open(DATA_PATH/section/filename, encoding='latin-1') as f:
            rawtext = f.read()
            rawtext = rawtext.replace('\n', '')
        section = int(section)
        filenumber = int(filename[-2:])
        batch = get_batch(section, filenumber)
        for i in batch:
            # for arg1
            arg1_char_span_string = pdtb2.loc[i, 'Arg1_SpanList']
            arg1_char_span_list = _get_span_list(arg1_char_span_string)
            arg1_rawtext = pdtb2.loc[i, 'Arg1_RawText']
            if _get_arg(arg1_char_span_list, rawtext) != arg1_rawtext:
                corrected_span = correct_span(arg1_char_span_list, arg1_rawtext, rawtext)
                arg1_char_span_list_corrected = _get_span_list(corrected_span)

                count += 1
                pdtb2.loc[i, 'Arg1_SpanList'] = corrected_span

            # for arg2
            arg2_char_span_string = pdtb2.loc[i, 'Arg2_SpanList']
            arg2_char_span_list = _get_span_list(arg2_char_span_string)
            arg2_rawtext = pdtb2.loc[i, 'Arg2_RawText']
            if _get_arg(arg2_char_span_list, rawtext) != arg2_rawtext:
                corrected_span = correct_span(arg2_char_span_list, arg2_rawtext, rawtext)

                count += 1
                pdtb2.loc[i, 'Arg2_SpanList'] = corrected_span
    return pdtb2


if __name__ == "__main__":
    DATA_PATH = Path("/home/pengfei/data/pdtb_v2/data/raw/wsj/")
    pdtb2 = pd.read_csv("../pdtb2/pdtb2.csv")
    pdtb2 = correct_docs()
    pdtb2.to_csv('pdtb2.csv')
