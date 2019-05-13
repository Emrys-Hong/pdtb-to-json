import pandas as pd
from pathlib import Path
import os

def read_file(filepath, dict_whole, index):
    """
    Args: 
            filepath(str): path to the file
    Returns: 
            ret(list[str, ..*]): list of string in relations
            dict_whole(dict): after adding new content to the dict
            index(int): after increasing the number"""
    with open(filepath, encoding='latin-1') as f:
        lines = f.readlines()
    for line_content in lines:
        line_content_list = line_content.split('|')
        assert(len(line_content_list) == 48)
        dict_whole[index] = line_content_list
        index += 1
    return dict_whole, index
    
def get_all_filenames(datapath=DATAPATH):
    """Returns (list[str]) all the filepath + filename in that dir"""
    ret = []
    sections = os.listdir(datapath)
    for sec in sections:
        filenames = os.listdir(datapath/sec)
        for filename in filenames:
            ret.append(datapath/sec/filename)
    return ret

def pdtb2csv():
    """takes content from @function read_file and Returns: DATAFRAME"""
    index = 0
    dict_whole = {}
    filenames = get_all_filenames()
    for filename in filenames:
        dict_whole, index= read_file(filename, dict_whole, index)
    columns = ['Relation',     'Section',     'FileNumber',     'Connective_SpanList',    'Connective_GornList',     'Connective_RawText',    'Connective_StringPosition',     'SentenceNumber',     'ConnHead',     'Conn1',    'Conn2',     'ConnHeadSemClass1',     'ConnHeadSemClass2',     'Conn2SemClass1',    'Conn2SemClass2',     'Attribution_Source',     'Attribution_Type',    'Attribution_Polarity',     'Attribution_Determinacy',    'Attribution_SpanList',     'Attribution_GornList',     'Attribution_RawText',     'Arg1_SpanList',     'Arg1_GornList',     'Arg1_RawText',     'Arg1_Attribution_Source',     'Arg1_Attribution_Type',    'Arg1_Attribution_Polarity',     'Arg1_Attribution_Determinacy',    'Arg1_Attribution_SpanList',     'Arg1_Attribution_GornList',    'Arg1_Attribution_RawText',     'Arg2_SpanList',    'Arg2_GornList',      'Arg2_RawText',    'Arg2_Attribution_Source',     'Arg2_Attribution_Type',    'Arg2_Attribution_Polarity',     'Arg2_Attribution_Determinacy',    'Arg2_Attribution_SpanList',     'Arg2_Attribution_GornList',    'Arg2_Attribution_RawText',     'Sup1_SpanList', 'Sup1_GornList',    'Sup1_RawText',   'Sup2_SpanList',    'Sup2_GornList',  'Sup2_RawText']
    print(len(columns))
    pdtb_csv_format = pd.DataFrame.from_dict(dict_whole, orient='index', columns=columns)
    return pdtb_csv_format



if __name__ == '__main__':
    DATAPATH = Path('/home/pengfei/data/dataset/pdtb_v2_modified/data_t/pdtb/')
    CSV_NAME = 'pdtb2_v2_modified.csv'
    pdtb2 = pdtb2csv()
    pdtb2.to_csv(CSV_NAME)
