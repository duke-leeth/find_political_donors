# -*- coding: utf-8 -*-
#
# File: find_political_donors.py
# Python Version: Python 2.7
# Require library:  heapq, sys
#
# Summary:
#   Take campaign contributions data published by Federal Election Commission,
#   and find the statistics(median, total amount, total number of contributions)
#   by zipcode and date respectively.
#
# Input:
#   itcont.txt
# Output:
#   medianvals_by_zip.txt
#   medianvals_by_date.txt
#


dic_by_zip = {}  # (CMTE_ID, ZIP_CODE):[MedianSearch, Sum Amount]
dic_by_date = {}  # (CMTE_ID, TRANSACTION_DT) : [MedianSearch, Sum Amount]


def valid_CMTE_ID(CMTE_ID):
    """ Validation of CMTE_ID format: <Non-empty>
        Args:   <CMTE_ID: String>
        Return: True if CMTE_ID is valid else False
    """

    if CMTE_ID=='':
        return False
    return True


def valid_ZIP_CODE(ZIP_CODE):
    """ Validation of zip code format: <Should be a string with more than 5-chars>
        Args:     <zip code: String>
        Returns: True if zip code is valid else False
    """

    if ZIP_CODE=='' or len(ZIP_CODE)<5:
        return False
    return True


import datetime
def valid_TRANSACTION_DT(TRANSACTION_DT):
    """ Validation of transaction date format: mmddyyyy
        Args:   <TRANSACTION_DT: String>
        Return: True if date is valid else False
    """

    if TRANSACTION_DT=='' or len(TRANSACTION_DT)!=8:
        return False

    try:
        if datetime.datetime.strptime(TRANSACTION_DT, '%m%d%Y').strftime('%m%d%Y') == TRANSACTION_DT:
            return True
    except ValueError:
        return False


def valid_TRANSACTION_AMT(TRANSACTION_AMT):
    """ Validation of transaction amount format: <mmddyyyy>
        Args:   <TRANSACTION_AMT: String>
        Return: True if transaction amount is valid else False
    """

    if TRANSACTION_AMT=='':
        return False

    try:
        float(TRANSACTION_AMT)
        return True
    except ValueError:
        return False


def valid_otherID(OTHER_ID):
    """ Validation of OTHER_ID format: <Should be Empty>
        Args:    <OTHER_ID: String>
        Return: True if OTHER_ID is valid else False
    """

    if OTHER_ID!='':
        return False
    return True


def valid_ID_AMT_OtherID(CMTE_ID, TRANSACTION_AMT, OTHER_ID):
    """ Validation of three common fields
        Args:   <CMTE_ID: String>,
                <TRANSACTION_AMT: String>,
                <OTHER_ID: String>
        Return: True if all of them are valid else False
    """

    if not valid_CMTE_ID(CMTE_ID):
        return False

    if not valid_TRANSACTION_AMT(TRANSACTION_AMT):
        return False

    if not valid_otherID(OTHER_ID):
        return False

    return True


from heapq import *
class MedianSearch:
    """ MedianSearch Object to find the median of all the values
        Method:
            add(<number:float>) : add a new element
            findMedian()        : return the median <float>
            size()              : return the number of the elements
    """

    def __init__(self):
        self.mini = []
        self.maxi = []

    def add(self, x):
        heappush(self.mini, -heappushpop(self.maxi, x))
        if len(self.maxi) < len(self.mini):
            heappush(self.maxi, -heappop(self.mini))

    def findMedian(self):
        if len(self.maxi) > len(self.mini):
            return float(self.maxi[0])
        else:
            return float(self.maxi[0] - self.mini[0]) / 2.0

    def size(self):
        return len(self.mini) + len(self.maxi)


def Prcess_Transcation(line):
    """ Process single line of transaction read from file
        Args:   <line: String>
        Return: <medianvals_by_zip single line for valid line: String>
    """

    res = ''
    sep = '|'
    tmpList = line.split(sep)

    CMTE_ID = tmpList[0]
    ZIP_CODE = tmpList[10]
    TRANSACTION_DT = tmpList[13]
    TRANSACTION_AMT = tmpList[14]
    OTHER_ID = tmpList[15]

    if not valid_ID_AMT_OtherID(CMTE_ID, TRANSACTION_AMT, OTHER_ID):
        return res

    if valid_TRANSACTION_DT(TRANSACTION_DT):
        key = (CMTE_ID, TRANSACTION_DT)
        if key not in dic_by_date:
            ms1 = MedianSearch()
            ms1.add(float(TRANSACTION_AMT))
            dic_by_date[key] = [ ms1, float(TRANSACTION_AMT)]
        else:
            val = dic_by_date[key]
            val[0].add( float(TRANSACTION_AMT) )
            val[1] += float(TRANSACTION_AMT)


    if valid_ZIP_CODE(ZIP_CODE):
        key = (CMTE_ID, ZIP_CODE[:5])
        if key not in dic_by_zip:
            ms2 = MedianSearch()
            ms2.add(float(TRANSACTION_AMT))
            dic_by_zip[key] = [ ms2, float(TRANSACTION_AMT) ]
        else:
            val = dic_by_zip[key]
            val[0].add( float(TRANSACTION_AMT) )
            val[1] += float(TRANSACTION_AMT)

        val_new = dic_by_zip[key]
        median = int( round( val_new[0].findMedian() ) )

        res = sep.join( [key[0], key[1], str(median), str(val_new[0].size()), str(int(val_new[1]))] )

    return res


def Process_lines(tmp_lines, fout):
    """ Process multiple lines and write to the output file
        Args:   <tmp_lines: String>
                <fout: File Object>
        Return: Void
    """

    outlist_by_zipcode = []
    for line in tmp_lines:
        out_by_zipcode = Prcess_Transcation(line)
        if out_by_zipcode!='':
            outlist_by_zipcode.append(out_by_zipcode)
    fout.write('\n'.join(outlist_by_zipcode))


def Output_by_DateFile(out_filename2):
    """ Write medianvals_by_date.txt
        Args:   <out_filename2: File Object>
        Return: Void
    """

    fout = open(out_filename2, 'a')

    outlist_by_date = []
    sep = '|'

    keys = sorted(dic_by_date.keys(), key=lambda tup: (tup[0],tup[1]) )


    for key in keys:
        val_new = dic_by_date[key]
        median = int( round( val_new[0].findMedian() ) )
        outlist_by_date.append( sep.join([key[0], key[1], str(median), str(val_new[0].size()), str(int(val_new[1]))]))

    fout.write('\n'.join(outlist_by_date))
    fout.close()


def Process_file(in_filename, out_filename1, out_filename2):
    """ Batch process lines read from in_filename,
            batch output to out_filename1,
            and write diretly to out_filename2 after read operation is completed
        Args:   <if_filename: String>,
                <out_filename1: String>,
                <out_filename2: String>
        Return: void
    """

    BUF_SIZE = 1024*1024*20 # 20MB

    fin = open(in_filename,'r')
    fout = open(out_filename1, 'a')

    tmp_lines = fin.readlines(BUF_SIZE)
    while tmp_lines:
        Process_lines(tmp_lines, fout)
        tmp_lines = fin.readlines(BUF_SIZE)

    fin.close()
    fout.close()

    Output_by_DateFile(out_filename2)


import sys
def main(argv=sys.argv):
    """ Execute with given input file, output files from command line
        Args:   <in_filename: String>,
                <out_filename1: String>,
                <out_filename2: String>
        Return: void
    """
    in_filename = argv[1]
    out_filename1 = argv[2]
    out_filename2 = argv[3]
    Process_file(in_filename, out_filename1, out_filename2)


if __name__ == "__main__":
    main()
