# Table of Contents
1. [Introduction](README.md#introduction)
2. [Approach summary](README.md#approach-summary)
3. [Dependencies and Run Instructions](README.md#dependencies-and-run-instructions)
4. [Testing](README.md#testing)
5. [Directory Structure](README.md#directory-structure)



# Introduction
This program aims to identify possible donors for a variety of upcoming election campaigns.

### Data source
The Federal Election Commission regularly publishes [campaign contributions](http://classic.fec.gov/finance/disclosure/ftpdet.shtml).
This program focus on their 2015 data.

### Output
1. `medianvals_by_zip.txt`: contains a calculated running median, total dollar amount and total number of contributions by recipient and zip code

2. `medianvals_by_date.txt`: has the calculated median, total dollar amount and total number of contributions by recipient and date.



# Approach summary

### Batch processing
Batch reads from file and batch writes to file. Since it is reasonably to assume the size of input file is large (more than 1GB), reading one line at a time will result in longer time in total. Thus, I set the buffer size to 20MB to read from the input file, rather than reading single line at each time. Similarly, writing the median values to the file, `medianvals_by_zip.txt`, is done after a trunk of transactions has been read and processed.

### Maintaining Dictionaries
For each output file, I maintain a dictionary for each unique key pair, e.g. `(CMTE_ID, ZIP_CODE)` for `medianvals_by_zip.txt` and `(CMTE_ID, TRANSACTION_DT)` for `medianvals_by_date.txt`, with a pair containing a MedianSearch object and total amount as value. As a result, accessing each key is very fast and easy to maintain the data in a structured manner.

### Median Searching
Leveraging MaxHeap and MinHeap can largely improve the runtime of median searching. Since finding median can be time consuming. In order not to make it take `O(N)` time, where `N` is the total numbers of elements, maintaining two heap can make it reach `O(logN)` runtime. Keeping half smallest elements in a MaxHeap and the other half in MinHeap takes `O(logN)` time, and always keep the size of MinHeap no larger than size of MaxHeap plus one. If the sizes of the two heaps are the same, the median is the average of the top element of MaxHeap and that of MinHeap. If the size of the MinHeap equals to MaxHeap plus one, the median is the the top element of MinHeap.

### Runtime Analysis
The overall runtime is `O(N logN)`, where `N` is the total lines in the input file.
##### Breakdown analysis:
Reading `N` transactions takes `O(N)`:
  *  For each line:
        *  Takes `O(1)` to verify whether it is a valid transaction
        *  Takes `O(logN)` to insert into the MedianSearch
        *  Takes `O(1)` to put the transaction detail into the dictionary
        *  Takes `O(1)` to find the median value

Therefore, it takes overall `O(N logN)` runtime.

##### Empirical runtime
This program has been tested running on a 3.83GB input file download from the [website](http://classic.fec.gov/finance/disclosure/ftpdet.shtml). It takes around 12 minutes on a Macbook Air 2014 with
Intel Core i5 CPU 1.4 GHz, and 8GB memory.


# Dependencies and Run Instructions
This program should be run with the following requirement:
* Python Version: Python 2.7
* Required Module: sys, heapq

Run the program with the following command within the root folder:

    ~$ ./run.sh



# Testing
Run the test with the following command within the `insight_testsuite` folder:

    ~$ ./run_tests.sh

On a failed test, the output of `run_tests.sh` would be:

    [FAIL]: test_1
    [Thu Mar 30 16:28:01 PDT 2017] 0 of 1 tests passed

On success:

    [PASS]: test_1
    [Thu Mar 30 16:25:57 PDT 2017] 1 of 1 tests passed



# Directory Structure

    ├── README.md
    ├── run.sh
    ├── src
    │   └── find_political_donors.py
    ├── input
    │   └── itcont.txt
    ├── output
    |   └── medianvals_by_zip.txt
    |   └── medianvals_by_date.txt
    ├── insight_testsuite
        └── run_tests.sh
        └── tests
            └── test_1
            |   ├── input
            |   │   └── itcont.txt
            |   |── output
            |   │   └── medianvals_by_zip.txt
            |   |__ └── medianvals_by_date.txt
            ├── test_2
            |   ├── input
            |   │   └── itcont.txt
            |   |── output
            |      └── medianvals_by_zip.txt
            |      └── medianvals_by_date.txt
            .
            .
            .
            ├── test_10
