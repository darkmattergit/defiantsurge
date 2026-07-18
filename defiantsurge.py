"""
DEFIANTSURGE\n
v1.0.0\n
`Mutual Contacts Discovery tool`\n
`Copyright (C) 2026 darkmattergit`\n
--------------------------------------------\n
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.\n

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.\n

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import glob
import csv
import argparse
import sqlite3

# Handle exception raised on Windows-based machines
try:
    import readline
except ImportError:
    pass

# DEFIANTSURGE version number const
DEFIANTSURGE_VERSION = "1.0.0"

# DEFIANTSURGE opening banner art const
DEFAINTSURGE_BANNER = r"""
   _____    ______   ______   ________      ____      ___   __   ________                  
  |     \  |   ___| |   ___| |__    __|    /    \    |   \ |  | |__    __|               
  |  ||  | |      | |   ___|    |  |      /  []  \   |    \|  |    |  |            
  |  ||  | |   ___| |  |      __|  |__   /  ____  \  |  |\    |    |  |        
  |_____/  |______| |__|     |________| /__/    \__\ |__| \___|    |__|                   
              ______   __     __   ______     _____   ______          
             /   __/  |  |   |  | |      \   /  ___| |    __|    
             |      | |  |   |  | |  []  /  |  / ___ |      |   
             |___   | |  |___|  | |  |\  \  |  \|  | |    __|  
              /____/   \_______/  |__| \__\  \_____| |______| 
"""

# Short GLPv3 blurb
GPL_BLURB = """This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

# Constant for name of SQLite file
DEFIANTSURGE_SQL = ".defiantsurge_dnr.db"


def get_targets_dict_list(csv_list: str = None) -> dict:
    """
    Reads in a list of target identifiers and their respective file paths from a CSV file so that the user does not have
    to enter them manually.
    :param csv_list: The absolute or relative path of the CSV file containing the list of target identifiers and DNR
    paths.
    :return: dict
    """
    csv_contents = {}
    try:
        with open(csv_list, "r") as cr:
            csv_read = csv.reader(cr)
            for target_identifiers, target_paths in csv_read:
                csv_contents[target_identifiers] = target_paths

    except FileNotFoundError:
        print(f"[!] pathError :: Could not find '{csv_list}', check path and try again")

    return csv_contents


def get_targets_dict_prompt() -> dict:
    """
    Prompt the user to provide the names of the targets and their associated DNR file paths.
    :return: dict
    """
    # Initialize dict to hold target names and their respective DNR file paths
    targets_dict = {}

    print()
    # Provide user instruction on how to add targets
    print("[*] Enter the identifiers of the targets and the absolute or relative paths to their respective Dialed "
          "Number Record (DNR) files")
    print("[*] use 'q' once you have added all targets\n")

    # Enter loop prompting user for target names and the DNR file paths
    while True:
        print("==================== ADD TARGET ====================\n")

        print("[*] Enter the identifier of the target the DNR data pertains to")
        target_name = str(input(">> "))

        # Break out of loop using "q"
        if target_name.lower().strip() == "q":
            break

        # Nothing entered, show message and start at beginning of loop
        if target_name == "" or target_name.isspace():
            print("[!] emptyIdentifierError :: No name entered")
            continue

        # Target name is already in use, show message and start at beginning of loop
        if target_name in targets_dict:
            print()
            print(f"[!] identifierInUseError :: Target identifier '{target_name}' already in use\n")
            continue

        # Prompt use for target's DNR file path
        print()
        print(f"[*] Enter the absolute or relative path of the DNR file for `{target_name}`")
        target_file_path = str(input(">> "))

        # Break out of loop using "q"
        if target_file_path.lower().strip() == "q":
            break

        # Nothing entered, show message and start at beginning of loop
        if target_file_path == "" or target_file_path.isspace():
            print("[!] emptyPathError :: No file path entered")
            continue

        # Check for existence of target's DNR file
        if glob.glob(target_file_path):
            # Add the file path as the value to the target's name key
            targets_dict[target_name] = target_file_path
            print()
            print(f"[+] Successfully added '{target_name}'\n")
            continue

        # Could not find the target's DNR file, inform user
        else:
            print()
            print(f"[!] pathError :: Could not find '{target_file_path}', check path and try again")
            print()
            continue

    return targets_dict


def confirm_target_dict(target_dict: dict = None) -> bool:
    """
    Ask user to confirm that target names and file paths are correct.
    :param target_dict: The dict returned by the `get_targets_dict` function.
    :return: bool
    """
    print()
    print("==================== CONFIRM ====================")
    print()

    # Initialize int to hold len of the longest target's name
    longest_name = 0

    # Get the len of the longest target's name
    for len_check in target_dict:
        if len(len_check) > longest_name:
            longest_name = len(len_check)

    # Display names and paths to respective DNR files for user to double-check and confirm
    print(" Target Identifiers and DNR File Paths")
    print(" -------------------------------")

    for targets_confirm in target_dict:
        formatted_name = f"{targets_confirm}:"
        spacing_required = longest_name - len(targets_confirm) + 2
        print(f"{'':{spacing_required}}{formatted_name} '{target_dict[targets_confirm]}'")

    # Prompt user for confirmation
    print()
    print(f"[*] Total number of targets/DNR files: {len(target_dict)}")
    print("[?] Are the targets and their respective file paths correct [Y/n]")
    user_confirmation = str(input(">> ")).lower().strip()

    if user_confirmation == "y" or user_confirmation == "" or user_confirmation.isspace():
        return True

    else:
        return False


def read_in_target_contacts(target_dict: dict = None, single_column_only: bool = None) -> None:
    """
    Read-in the contacts from the target's files and return a dict where the key is the target names and the values are
    lists holding the unique contacts found in the files.
    :param target_dict: The dict returned by the `get_targets_dict` function.
    :param single_column_only: A bool determining whether to read-in data from the first two columns or only the first.
    :return: dict
    """
    print()
    print("[*] Reading in DNR data")

    # Create SQLite db that will be used to carry out additional types of analysis
    conn = sqlite3.connect(DEFIANTSURGE_SQL)
    crsr = conn.cursor()

    # Create table
    crsr.execute("CREATE TABLE IF NOT EXISTS dnr_contacts (target_identifier TEXT, contact_identifier TEXT)")
    conn.commit()

    for dnr_paths in target_dict:
        target_contacts_list = []

        with open(target_dict[dnr_paths], "r") as dr:
            dnr_read = csv.reader(dr)

            for event_contacts in dnr_read:
                    # Read in and check the first element to make sure that it does not exist in the list already and
                    # that it is not a blank element
                    if (event_contacts[0].strip() not in target_contacts_list and event_contacts[0].strip()
                            not in target_dict and event_contacts[0] != "" and event_contacts[0].isspace() is False):

                        # Add contact to list
                        target_contacts_list.append(event_contacts[0].strip())
                        # Add contact to table
                        crsr.execute("INSERT INTO dnr_contacts VALUES (?, ?)", (dnr_paths,
                                                                                event_contacts[0]))
                        conn.commit()

                    # Read in and check the second element to make sure that it does not exist in the list already and
                    # that it is not a blank element. If the user has specified that only the first element is to be
                    # used, this part is skipped
                    if single_column_only is False:
                            if (event_contacts[1].strip() not in target_contacts_list and
                                    event_contacts[1].strip() not in target_dict and event_contacts[1] != "" and
                            event_contacts[1].isspace() is False):
                                # Add contact to list
                                target_contacts_list.append(event_contacts[1].strip())
                                # Add contact to table
                                crsr.execute("INSERT INTO dnr_contacts VALUES (?, ?)", (dnr_paths,
                                                                                        event_contacts[1]))
                                conn.commit()

    crsr.close()
    conn.close()


def discover_mutual_contacts(target_dict: dict = None) -> dict:
    """
    Analyze the combined data in the SQLite file to find mutual contacts.
    :param target_dict: The dict returned by the `get_targets_dict` function.
    :return: dict
    """
    print("[*] Analyzing data, looking for mutual contacts")

    mutual_contacts_dict = {}

    conn = sqlite3.connect(DEFIANTSURGE_SQL)
    crsr = conn.cursor()

    for target_identifiers in target_dict:
        crsr.execute("SELECT target_identifier, contact_identifier FROM dnr_contacts WHERE target_identifier != ? "
                     "AND contact_identifier IN (SELECT contact_identifier FROM dnr_contacts WHERE "
                     "target_identifier = ?)",(target_identifiers, target_identifiers))

        mutual_contacts_dict[target_identifiers] = crsr.fetchall()

    crsr.close()
    conn.close()

    print()
    print("[+] Analysis complete")

    return mutual_contacts_dict


def display_mutual_contacts_results(mutual_contacts_dict: dict = None) -> None:
    """
    Displays the results from the `discover_mutual_contacts` function.
    :param mutual_contacts_dict: The dict returned by the `discover_mutual_contacts` function.
    :return: None
    """
    print()

    print("=================================== MUTUAL CONTACTS ANALYSIS ===================================")
    print()

    for dnr_targets in mutual_contacts_dict:
        print(f"-------------------- {dnr_targets} --------------------")
        print()

        if len(mutual_contacts_dict[dnr_targets]) == 0:
            print(f"[*] No mutual contacts found for '{dnr_targets}'")
            print()
            continue

        else:
            for mutual_contact in mutual_contacts_dict[dnr_targets]:
                print(f" {dnr_targets} -----> {mutual_contact[1]} <----- {mutual_contact[0]}")
        print()
        print(f"[*] Number of mutual contacts: {len(mutual_contacts_dict[dnr_targets])}")
        print()


def get_contact_counts(mutual_contacts_dict: dict = None) -> None:
    """
    Count the number of targets that a contact is in communication with.
    :param mutual_contacts_dict: The dict containing the targets and their respective contacts.
    :return: None
    """
    conn = sqlite3.connect(DEFIANTSURGE_SQL)
    crsr = conn.cursor()

    # Get the total number of targets
    total_target_number = len(mutual_contacts_dict)

    # Get the total number of time each contact appears which will indicate the number of targets they are in
    # communication with
    crsr.execute("SELECT contact_identifier, COUNT(contact_identifier) FROM dnr_contacts GROUP BY 1 ORDER BY 2 DESC")
    count_results = crsr.fetchall()

    print("=================================== CONTACT OCCURRENCE COUNTS ===================================")
    print()

    # Initialize int to hold len of longest contact name
    longest_name = 0

    for contact_lens in count_results:
        if len(contact_lens[0]) > longest_name:
            longest_name = len(contact_lens[0])

    # Add additional buffer spacing depending on the len of the longest name
    if longest_name < 12:
        longest_name += 19
    else:
        longest_name += 2

    # Calculate the spacing needed between the two headers
    header_spacing = longest_name - 17

    # Display results
    print(f" Contact Identifier {'':{header_spacing}} Occurrence Counts")
    print(f" ------------------ {'':{header_spacing}} -----------------")
    for contacts_name, contacts_count in count_results:
        spacing_required = longest_name - len(contacts_name)
        print(f" {contacts_name}: {'':{spacing_required}} {contacts_count}/{total_target_number}")

    print()

    # Clear data from SQLite file
    crsr.execute("DELETE FROM dnr_contacts")
    conn.commit()

    crsr.close()
    conn.close()


def export_analysis_results_csv(csv_export_path: str = None, mutual_contacts_dict: dict = None) -> None:
    """
    Exports analysis results to a CSV file.
    :param csv_export_path: The absolute or relative path of the CSV file to export the results to.
    :param mutual_contacts_dict: The dict containing the analysis results.
    :return: None
    """
    # The specified path is empty or only consists of spaces/tabs, inform user of error
    if csv_export_path == "" or csv_export_path.isspace():
        print("[!] emptyExportPathError :: No CSV export file path entered, analysis results will not be exported")

    else:
        try:
            # Create the CSV export file
            with open(csv_export_path, "w") as cw:
                cwx = csv.writer(cw)

                for dnr_targets in mutual_contacts_dict:
                    # If there are no mutual contacts for a target, then move to next target
                    if len(mutual_contacts_dict[dnr_targets]) == 0:
                        pass

                    # Write mutual contacts to CSV
                    else:
                        for mutual_data in mutual_contacts_dict[dnr_targets]:
                            constructed_row = (dnr_targets, mutual_data[1], mutual_data[0])
                            cwx.writerow(constructed_row)

            print(f"[+] Successfully exported analysis results to '{csv_export_path}'")

        # Could not create the CSV file, inform user of error
        except FileNotFoundError:
            print(f"[!] exportFileError :: Could not open '{csv_export_path}' for writing, analysis results were "
                  f"not exported")
            print()


parser = argparse.ArgumentParser(prog="defiantsurge.py")

parser.add_argument("-e", "--export", help="Export results to a CSV file", default=None)
parser.add_argument("-s", "--single", help="A special argument that can be used to specify that only "
                                             "the data in the first column should be analyzed",
                      action="store_true")
parser.add_argument("-l", "--list", help="Use a CSV containing the target identifiers and their "
                                         "respective file paths to skip adding them manually", default=None)
parser.add_argument("-g", "--gpl", help="Print GPLv3 blurb and exit", action="store_true")

args = parser.parse_args()

# Display GPLv3 blurb if specified by user and exit
if args.gpl:
    print(GPL_BLURB)
    exit()

# Construct the opening banner
print(DEFAINTSURGE_BANNER)
print("  Mutual Contacts Discovery Tool")
print(f"  Version: {DEFIANTSURGE_VERSION}")
print(f"  License: GPLv3")

# Initialize empty dict to hold target identifiers and their respective DNR file paths
targets_dnr_dict = {}

if args.list is not None:
    # Read in target identifiers and paths from the CSV list file
    targets_dnr_paths_dict = get_targets_dict_list(args.list)

else:
    # Get user to enter the names and DNR files of targets
    targets_dnr_paths_dict = get_targets_dict_prompt()

# No targets entered, exit
if len(targets_dnr_paths_dict) == 0:
    print()
    print(f"[!] emptyTargetDict :: Target dict is empty, nothing to do")
    exit()

# Only one target entered, exit
if len(targets_dnr_paths_dict) == 1:
    print()
    print(f"[!] oneTargetSpecified :: Only one target specified, no mutual contacts to discover")
    exit()

# Choices not confirmed, exit
if not confirm_target_dict(targets_dnr_paths_dict):
    print()
    print(f"[*] Exiting")
    exit()

# Get the unique contacts from each target's DNR file
read_in_target_contacts(targets_dnr_paths_dict, args.single)

# Analyze the unique contacts
mutual_contacts = discover_mutual_contacts(targets_dnr_paths_dict)

# Display the analysis results
display_mutual_contacts_results(mutual_contacts)

# Get number of targets a contact is found communicating with
get_contact_counts(mutual_contacts)

# Export analysis results if the -e, --export arg is used
if args.export is not None:
    export_analysis_results_csv(args.export, mutual_contacts)

print(f"[+] Done")
