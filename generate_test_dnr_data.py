import csv

# This script creates 9 CSV files that contain test data is used to test DEFIANTSURGE during development as well as to
# provide users a way to learn to use DEFIANTSURGE

# Alice test data
ALICE_DNR_DATA = [
    ["alice", "eve",],
    ["peggy", "alice",],
    ["alice", "bob",],
    ["bob", "alice",],
    ["george", "alice"],
    ["  ", "alice"],
    ["alice", "eve"],
    ["alice", "irene"],
]

# Bob test data
BOB_DNR_DATA = [
    ["bob", "eve",],
    ["george", "bob",],
    ["irene", "bob",],
    ["bob", "eve"],
    ["george", "bob"],
    ["  ", "bob"],
]

# Carol test data
CAROL_DNR_DATA = [
    ["alice", "carol",],
    ["carol", "george",],
    ["george", "carol",],
    ["irene", "carol"],
    ["stanley", "carol"],
    ["carol", "juliet"],
    ["carol", "stanley"],
]

# Dave test data
DAVE_DNR_DATA = [
    ["dave", "bob",],
    ["victor", "dave",],
    ["dave", "juliet",],
    ["maria", "dave",],
    ["  ", "dave",],
]

# Trent test data
TRENT_DNR_DATA = [
    ["alice", "trent",],
    ["trent", "bob",],
    ["trent", "carol",],
    ["dave", "trent",],
]

# Walter test data
WALTER_DNR_DATA = [
    ["eddy", "walter",],
    ["hector", "eddy",],
    ["walter", "victor",],
    ["yvette", "walter",],
]

# Peggy test data
PEGGY_DNR_DATA = [
    ["sally", "peggy",],
    ["george", "peggy",],
    ["peggy", "irene",],
    ["peggy", "eve",],
    ["  ", "peggy"],
    ["maria", "peggy",],
    ["peggy", "juliet",],
]

# Victor test data
VICTOR_DNR_DATA = [
    ["eve", "victor",],
    ["victor", "stanley",],
    ["george", "victor",],
    ["sally", "victor",],
    ["victor", "maria",],
    ["victor", "irene",],
]

DICT_OF_TARGET_PATHS_AND_DATA = {
    "alice_test.csv": ALICE_DNR_DATA,
    "bob_test.csv": BOB_DNR_DATA,
    "carol_test.csv": CAROL_DNR_DATA,
    "dave_test.csv": DAVE_DNR_DATA,
    "trent_test.csv": TRENT_DNR_DATA,
    "walter_test.csv": WALTER_DNR_DATA,
    "peggy_test.csv": PEGGY_DNR_DATA,
    "victor_test.csv": VICTOR_DNR_DATA,
}

# List of target identifiers and their respective file paths
LIST_OF_TARGETS_AND_PATHS = [
    ["alice", "alice_test.csv"],
    ["bob", "bob_test.csv"],
    ["carol", "carol_test.csv"],
    ["dave", "dave_test.csv"],
    ["trent", "trent_test.csv"],
    ["walter", "walter_test.csv"],
    ["peggy", "peggy_test.csv"],
    ["victor", "victor_test.csv"],
]

for dnr_data in DICT_OF_TARGET_PATHS_AND_DATA:
    with open(dnr_data, "w") as wc:
        wr_csv = csv.writer(wc)
        wr_csv.writerows(DICT_OF_TARGET_PATHS_AND_DATA[dnr_data])
        print(f"[+] Wrote '{dnr_data}'")

# Write CSV that contains target identifiers and their respective file paths for use with -l, --list arg
with open("dnr_path_list.csv", "w") as dw:
    list_csv = csv.writer(dw)
    list_csv.writerows(LIST_OF_TARGETS_AND_PATHS)

print("[+] Wrote target identifier and file path list to 'dnr_path_list.csv'")
