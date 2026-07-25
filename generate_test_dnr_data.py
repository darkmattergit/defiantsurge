import csv

# This script creates 3 CSV files that contain test data is used to test DEFIANTSURGE during development as well as to
# provide users a way to learn to use DEFIANTSURGE

# Alice test data
ALICE_DNR_DATA = [
    ["alice", "bob",],
    ["carol", "alice",],
    ["alice", "carol",],
    ["bob", "alice",],
    ["reallysuperduperlongername", "alice"],
    ["  ", "alice"],
    ["alice", "eve"],
    ["alice", "bob2"],
]

# Bob test data
BOB_DNR_DATA = [
    ["bob", "alice",],
    ["alice", "bob",],
    ["carol", "bob",],
    ["bob", "longname"],
    ["longername", "bob"],
    ["  ", "bob"],
]

# Carol test data
CAROL_DNR_DATA = [
    ["alice", "carol",],
    ["carol", "alice",],
    ["longname", "carol",],
    ["bob", "carol"],
    ["longername", "carol"],
    ["carol", "reallysuperduperlongername"],
    ["carol", "eve"],
]

# List of target identifiers and their respective file paths
LIST_OF_TARGETS_AND_PATHS = [
    ["alice", "alice_test.csv"],
    ["bob", "bob_test.csv"],
    ["carol", "carol_test.csv"],
]

# Write Alice test data
with open("alice_test.csv", "w") as aw:
    alice_csv = csv.writer(aw)
    alice_csv.writerows(ALICE_DNR_DATA)

print("[+] Wrote Alice test data to 'alice_test.csv'")

# Write Bob test data
with open("bob_test.csv", "w") as bw:
    bob_csv = csv.writer(bw)
    bob_csv.writerows(BOB_DNR_DATA)

print("[+] Wrote Bob test data to 'bob_test.csv'")

# Write Carol test data
with open("carol_test.csv", "w") as cw:
    carol_csv = csv.writer(cw)
    carol_csv.writerows(CAROL_DNR_DATA)

print("[+] Wrote Carol test data to 'carol_test.csv'")

# Write CSV that contains target identifiers and their respective file paths for use with -l, --list arg
with open("dnr_path_list.csv", "w") as dw:
    list_csv = csv.writer(dw)
    list_csv.writerows(LIST_OF_TARGETS_AND_PATHS)

print("[+] Wrote target identifier and file path list to 'dnr_path_list.csv'")
