# DEFIANTSURGE
DEFIANTSURGE is a command line-based Mutual Contacts Discovery tool written in Python. It uses Graph Theory analytics to uncover
hidden and indirect relationships between two or more targets by looking for mutual contacts between them.

> [!TIP]
> While DEFIANTSURGE was originally created to analyze Dialed Number Record (DNR) data, it can also be used to analyze 
> other types of data as well, such as financial transactions, online messaging records, Online Social Network (OSN)
> following/follower lists, GPS records, etc. 

## Compatability
DEFIANTSURGE is compatible with Python 3.10 and upwards, and is also OS independent, meaning that it can operate on 
Linux, Windows and Mac machines. Additionally, it relies only on Python's standard library and does not require any
additional packages.

## Usage
DEFIANTSURGE is used via the command line:
Linux and Mac:
`python3 defiantsurge.py`

Windows:
`py defiantsurge.py`

The following arguments are also available:
* `-e, --export`: Export the results to a CSV file - OPTIONAL
* `-s, --single`: A special argument that is used to specify that only the data in the first column should be analyzed, or 
that the record files only contain one column. - OPTIONAL
* `-l, --list`: Use a CSV containing the target identifiers and their respective file paths to skip adding them manually. - OPTIONAL
* `-g, --gpl`: Displays a small blurb about the GPLv3 license. - OPTIONAL
* `-h, --help`: Display the help banner. - OPTIONAL

> [!IMPORTANT]
> When the `-s, --single` argument is used, it applies to **ALL** of the files used in the analysis. This means that even
> if some of the files contain data in two columns, only the data in the first column will be analyzed. 

## Formatting Requirements
For DEFIANTSURGE to analyze the DNR data, it must be follow certain formatting requirements:
* The DNR data must be in `Comma Separated Value (CSV)` format
* The first two columns must be the `Calling` and `Called` data
* All of the identifiers, including those of the targets, must be formatted in the same way across all DNR files, meaning if `Alice` is formatted as `123-456-7890 (Alice)` in one file, it must be formatted the same way in the others.

> [!TIP]
> To make it easier to identify targets and mutual contacts, it is recommended to combine numbers and names
> where possible (ex. `999-999-9999 (Alice)`, `Bob (123-456-7890)`, etc.). Additionally, this alleviates the
> drawback of using only names, as it will ensure that every contact is unique and recognizable.

> [!NOTE]
> Because DEFIANTSURGE is only interested in the first two columns, it does not matter if a DNR (or other type of record) file
> more than two columns, as the rest are ignored.

## Adding Dialed Number Records (DNR) to analyze
When DEFIANTSURGE is started, it will enter a loop that will ask the user to first enter the number of target.
Example:
```
[*] Enter the identifier of the target the DNR data pertains to
>> alice
```

> [!IMPORTANT]
> When adding target identifiers, ensure that they are entered in the exact same way as they appear in the DNR data.
> Otherwise, it may lead to self-pointing.

After checking that the target is not already entered, the user is asked to provide the absolute or relative path of the
target's DNR file that is to be analyzed.
Example:
```
[*] Enter the absolute or relative path of the DNR file for `alice`
>> alice_test.csv
```

The loop will continue until the user enters `q`, either during the target identifier prompt or the DNR file path prompt. Once out
of the prompt loop, the user will be shown the identifiers of the targets and their corresponding DNR file paths and is asked to
confirm if the information is correct. If the user confirms, DEFIANTSURGE will begin to analyze the data. If the user indicates
that the information is incorrect, DEFIANTSURGE will then exit.

> [!NOTE]
> Analysis times may vary based on the number and size of data sets.

### Types of Analysis 

#### Mutual Contacts Analysis
The Mutual Contacts Analysis section is the main analytical section of DEFIANTSURGE. This is where the user is shown
the results of the analysis. An example of what the results look like for a single target is shown below:
```
-------------------- carol --------------------

 carol -----> reallysuperduperlongername <----- alice
 carol -----> eve <----- alice
 carol -----> longname <----- bob
 carol -----> longername <----- bob

[*] Number of mutual contacts: 4
```

Each target has their own section that displays any mutual contacts that were found. The identifiers in the middle are the 
contacts that are shared between the two targets shown on either side of them. Below the results is a count of the total number 
of mutual contacts found for that target. If there are no mutual contacts found for a specific target, then the user is informed 
that the target shares no contacts with any other targets.

#### Target Communication Counts
The Target Communication Counts section provides the user a quick way to identify key contacts of interest by showing them
a counts of how many targets a contact is in communication with as well as which targets a contact communicates with. Below 
is an example of what this section looks like:
```
 Contact Identifier             Target Communication Counts
 ------------------             ---------------------------
 reallysuperduperlongername:    2/3
  * alice
  * carol

 longname:                      2/3
  * bob
  * carol

 longername:                    2/3
  * bob
  * carol

 eve:                           2/3
  * alice
  * carol

 bob2:                          1/3
  * alice
```

The `Target Communication Counts` column shows how many targets out of the total number of targets that specific contact
is in communication with and underneath each contact identifier is shown which targets they communicate with.

## Exporting Results
If you would like export the results of the analysis to a CSV file, use the `-e, --export` argument.
Example:
`python3 defiantsurge.py -e "results_export.csv"`

> [!NOTE]
> Only the results from the `Mutual Contacts Analysis` section are exported to the CSV file.

## Generating Test Data
The `generate_test_dnr_data.py` file is used to generate a small amount of fictional test data that is used to test DEFIANTSURGE 
during development. However, it is also meant to be used by users as a way to learn how to use DEFIANTSURGE as well. The script 
creates 4 CSV files:
* `alice_test.csv`
* `bob_test.csv`
* `carol_test.csv`
* `dnr_path_list.csv`

The first 3 files contain test data for their respective targets, while `dnr_path_list.csv` is a "list file" that can be used
with the `-l, --list` arg.  

## Terminology
This section provides a list of terminology used in DEFIANTSURGE and their definitions:
* `Dialed Number Record (DNR)`: A file containing the phone record metadata.
* `Self-pointing`: False positive results where a target is shown as a mutual contact to themselves (ex. Alice --> Alice <-- Bob).
* `Mutual contact`: An individual who is in contact with two or more targets (ex. Alice --> Carol <-- Bob).
* `Target`: The identifier of the target that the DNR data pertains to.

## Errors
The following is a list of all error names, their descriptions, and what might cause them:
* `emptyPathError`: `No file path entered`. This error occurs when an empty string is passed to DEFIANTSURGE when it asks for the path to a target's DNR file.
* `pathError`: `Could not find 'TARGET FILE PATH', check path and try again`. This error occurs when DEFIANTSURGE cannot find the the target's DNR file at the specified path. Check that you entered the path correctly and try again.
* `emptyExportPathError`: `No CSV export file path entered, analysis results will not be exported`.
* `exportFileError`: `Could not open 'CSV EXPORT PATH' for writing, analysis results were not exported`. This error could occur either because the directory you wish to create the export file in does not exist or because you do not have `write` privileges for that directory. Check that you entered the path correctly and that you have the required privileges.

## Branches
This repository has 2 branches: `master` and `dev`. The `master` branch holds all of the stable code and is updated 
whenever a new stable version of DEFIANTSURGE is released. The `dev` branch on the other hand is updated more often, with
new changes being committed to it first.

## License
DEFIANTSURGE is licensed under GPLv3. The full license can be found in the `LICENSE` file.

## Contributing
Interested in contributing to DEFIANTSURGE? Check out the `CONTRIBUTING.md` file to find out how.

