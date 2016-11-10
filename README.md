# PayMo 

PayMo is a "digital wallet" company called PayMo that allows users to easily request and make payments to other PayMo users. The team at PayMo has decided they want to implement features to prevent fraudulent payment requests from untrusted users.

1. [Design Summary] (README.md#design-summary)
2. [Details of Implementation] (README.md#details-of-implementation)
3. [Repo directory structure] (README.md#repo-directory-structure)

## Design Summary

We need to find 4th degree of connections in a most efficient matters.  Also, anticipate that the code can be run in paraellel, distributed algorithm on a cluster, where the processing and generating of data can doney simultaneously.  The code uses divide and conquer, hashmap like data structure to cache results for subsequent lookup.

## Details of Implementation

<img src="./images/fourth-degree-friends2.png" width="600">

In the above diagram, payments have transpired between User

* A and B 
* B and C 
* C and D 
* D and E 
* E and F

The code first build the 1st degree of connections (transactions) of the batch dataset, store them in a hashmap with key, pair value.  The key is the userid and the value is the set of id being connected.

Once the dataset parse commplete, we can run thru the streaming dataset.  Lookup if they are first degree connected.
For 2nd degree connections, we first lookup if they are 1st degree connected, if not, we can lookup the 2nd degree connections for both IDs, if the value, i.e. the set of IDs being cached in the hashmap, check to see if A's id is in Set B or B's ids is in Set A.  If the set of IDs does not exists in the hashmaps, build it.  It is build by union of set of the 1st degree connects' connections and the id of the 1st degree connection set.  Cache the findings in the hashmap so that subsequent lookup can be done with building the set again.

For 4th degree, repeat the process, do 1st degree lookup, 2nd degree lookup, and both turn negative, check if they are 4th degree connected.  The way to do it is to check if A's id in in B's 2nd connection set or B's id in A's 2nd connection set.  Also, check if both id's 2nd degree connection set intersect each other.

[Back to Table of Contents] (README.md#table-of-contents)

### Input

We assume that each new line of `stream_payment.txt` corresponds to a new, valid PayMo payment record -- regardless of being 'unverified'

### Output

For example, if there were 5 lines of transactions in the `stream_payment.txt`, then the following `output1.txt` file for Feature 1 could look like this: 

	trusted
	trusted
	unverified
	unverified
	trusted


For example, the first 10 lines (including the header) of `batch_payment.txt` or `stream_payment.txt` could look like: 

	time, id1, id2, amount, message
	2016-11-02 09:49:29, 52575, 1120, 25.32, Spam
	2016-11-02 09:49:29, 47424, 5995, 19.45, Food for 🌽 😎
	2016-11-02 09:49:29, 76352, 64866, 14.99, Clothing
	2016-11-02 09:49:29, 20449, 1552, 13.48, LoveWins
	2016-11-02 09:49:29, 28505, 45177, 19.01, 🌞🍻🌲🏔🍆
	2016-11-02 09:49:29, 56157, 16725, 4.85, 5
	2016-11-02 09:49:29, 25036, 24692, 20.42, Electric
	2016-11-02 09:49:29, 70230, 59830, 19.33, Kale Salad
	2016-11-02 09:49:29, 63967, 3197, 38.09, Diner
	 

## Repo directory structure
[Back to Table of Contents] (README.md#table-of-contents)

Example Repo Structure

	├── README.md 
	├── run.sh
	├── src
	│  	└── antifraud.java
	├── paymo_input
	│   └── batch_payment.txt
	|   └── stream_payment.txt
	├── paymo_output
	│   └── output1.txt
	|   └── output2.txt
	|   └── output3.txt
	└── insight_testsuite
	 	   ├── run_tests.sh
		   └── tests
	        	└── test-1-paymo-trans
        		│   ├── paymo_input
        		│   │   └── batch_payment.txt
        		│   │   └── stream_payment.txt
        		│   └── paymo_output
        		│       └── output1.txt
        		│       └── output2.txt
        		│       └── output3.txt
        		└── your-own-test
            		 ├── paymo_input
        		     │   └── batch_payment.txt
        		     │   └── stream_payment.txt
        		     └── paymo_output
        		         └── output1.txt
        		         └── output2.txt
        		         └── output3.txt

