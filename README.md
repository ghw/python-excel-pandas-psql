# python-excel-pandas-psql
Excel - Pandas - PostgreSQL connector.


## Getting Started

First, clone the project:
```bash
$ git clone https://github.com/srtamrakar/python-excel-pandas-psql.git
```

### Prerequisites

#### 1. Ubuntu 16.X+ / MacOS X+
#### 2. Python 3.X+
```bash
$ sudo apt-get update
$ sudo apt-get -y upgrade
$ sudo apt-get install python3.X
$ sudo apt-get install -y python3-pip
```

### Repository Structure

```
.
├── README.md                    # Contains step-by-step guidelines
├── src/                         # Contains source code
│   └── general/                 # Contains classes with some frequently used functions on general objects
├── test/                        # Contains unit tests
└── requirements.txt             # Necessary python libraries
```

### Using the modules

#### _ExcelPandas()_
A class that contains functions to connect pandas dataframes and excel sheets:
1. get sheetnames in excel file
1. get dataframe from excel file
1. send dataframe to excel file

#### _PostgresPandas()_
A class that contains functions to connect pandas dataframes and psql database:
1. get psql query results as dataframe
1. send dataframe to psql database

#### _ExcelPostgres()_
A class that contains functions to connect psql database and excel sheets:
1. get psql query results excel sheets
1. send excel to psql database table

#### _DateFunc()_
A class that contains functions with some frequent operations on date objects (datetime and pandas.*.Timestamp):
1. get year from the object
1. create datetime object from text
1. get different in year between two dates

#### _DirFunc()_
A class that contains functions with some frequent operations on directories:
1. get location directory from a filepath
1. get basename from a filepath
1. get file extension
1. check if folder exists
1. filter temporary files from list of filenames
1. get all files from a directory
1. get latest file from a directory
1. get absolute path of a file

#### _ListFunc()_
A class that contains functions with some frequent operations on lists:
1. get filtered list with unique elements
1. get common items between two lists
1. get all items of two lists
1. get flattened list

#### _StrFunc()_
A class that contains functions with some frequent operations on string objects:
1. check if string is camelCase
1. remove accent
1. clean snake case
1. remove non-alpha numeric characters
1. convert text to camel case
1. convert camel case to snake case
1. convert text to snake case

#### _PandasFunc()_
A class that contains functions with some frequent operations on pandas dataframe:
1. get row count
1. get dictionary based on two columns
1. get dataframe with all permutations from a dictionary with list values
1. set column as index
1. get column names and type as dictionary
1. get column names by type
1. check if float column has only integers and nan
1. change column names to alpha numeric
1. change column names to snake case
1. check if there are any unnamed headers
1. check if a column exists
1. get maximum length of objects in a column

## Author

* **&copy; Samyak Ratna Tamrakar** - [Github](https://github.com/srtamrakar), [LinkedIn](https://www.linkedin.com/in/srtamrakar/).