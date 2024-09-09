## Working Principle
### Commit Node Structure
The Pastport VCS system follows a **linear-direct sequential** structure, as depicted in the accompanying diagram. 

Each node in the diagram signifies a commit made, preserving essential data. This data enables the regeneration of files committed at that specific point in time. The initial commit, designated as **'Commit 0'** saves entire files in their original state. Subsequent commits, starting from **'Commit 1'** and onwards, are built upon the foundation of "Commit 0."
The commit node structure, illustrated in the aforementioned image, comprises four commits: **'Commit 0'**, **'Commit 1'**, **'Commit 2'**, and **'Commit 3'**. Commit 0 holds particular significance as the starting point, storing complete files precisely as they were during the initial commit. Reverting back to a prior commit, such as Commit 1 from Commit 3, involves retracing the steps back to Commit 0. From there, files are regenerated using the data from Commit 1.

The structure of the commit node system is delineated as follows (please refer to the image above): there are four commits denoted as commit 0, commit 1, commit 2, and commit 3. Commit 0 holds a distinct status as the initial point, preserving complete files in their original form (the method of data storage will be elaborated upon as we progress). Subsequent commits are all derived from commit 0.

> Consider the scenario where the system is presently at commit 3, and there is a desire to revert back to commit 1. To achieve this, one simply needs to return to commit 0, where the original data from the initial commit is stored. From this point, the files can be regenerated utilizing the data from commit 1.

### Commit Data Structure
The critical question arises: what information should each node store? Specifically, what constitutes the contents of commit data? 
#### Example: OT(Old Text) and NT(New Text) Transformation
This can be elucidated through an example involving **old text (OT)** and **new text (NT)** transformation. 
Let's say
<div align="center">
    
**OT**: "Hello I am Khritish,"\
**NT**: "Hello I Romen" 
</div>

The transformation involves deleting ["am", "Khritish"] from OT and inserting ["Romen"] 
The common part, "Hello I," remains untouched.

To extract deletion and insertion information, a straightforward approach is employed. 
Firstly, identify the common part ("Hello, I"). 
Anything in OT remaining after removing the common part necessitates deletion, as it does not exist in NT. 
Conversely, anything in NT after removing the common part requires insertion. 

For the provided example:\
**Common part**: "Hello, I"\
**Deletion**: OT - common part = "am," "Khritish"\
**Insertion**: NT - common part = "Romen"
<div align="center">
    
**New Text = (Old Text - deletions) + insertions**
</div>

Consequently, within each commit, the data stored in a node comprises the necessary insertion and deletion information. These details delineate the modifications required on commit 0 to generate the new text.

### Longest Common Subsequences (LCS)
Indeed, it is evident that identifying the common elements between two texts is crucial. To achieve this, we employ a ‘difference algorithm’, specifically the **Longest Common Subsequence (LCS)** algorithm. LCS determines the length of the longest sequence shared by both texts. This method employs Dynamic Programming and backtracking. A slight modification involves utilizing sequences of words instead of individual letters.

Allow me to illustrate this process using an example:

Consider the following texts:
<div align="center">
    
**Old Text (OT)**: "How are you doing"\
**New Text (NT)**: "How you doin’"
</div>

#### Step 1: Tokenize the sentences
<div align="center">

**Tokenized Old Text (TOT)**: ["How", "are", "you", "doing"]\
**Tokenized New Text (TNT)**: ["How", "you", "doin’"]
</div>

#### Step 2: Set up the DP matrix
Create a DP matrix of size **len(TOT) + 2  ✕  len(TNT) + 2**, filling it with **0**'s, where TOT represents Tokenized Old Text and TNT represents Tokenized New Text.
|       | Ø  | How | you | doin |
|-------|----|-----|-----|------|
| Ø     | 0  | 0   | 0   | 0    |
| How   | 0  | 0   | 0   | 0    |
| are   | 0  | 0   | 0   | 0    |
| you   | 0  | 0   | 0   | 0    |
| doing | 0  | 0   | 0   | 0    |

#### Step 3: Populate the DP matrix using the algorithm below
```
For i : 1 to length(TOT) - 1 (Inclusive range)
    For j : 1 to length(TNT) - 1 (Inclusive range)
        If TOT[i] == TNT[j]:
            DP[i][j] = DP[i-1][j-1] + 1
        Else:
	        DP[i][j] = max(DP[i][j-1], DP[i-1][j])
```
This algorithm sets up the DP matrix to extract the longest common subsequence.
|       | Ø  | How | you | doin |
|-------|----|-----|-----|------|
| Ø     | 0  | 0   | 0   | 0    |
| How   | 0  | 1   | 1   | 1    |
| are   | 0  | 1   | 1   | 1    |
| you   | 0  | 1   | 2   | 2    |
| doing | 0  | 1   | 2   | 2    |


#### Step 4: Backtrack the DP matrix to obtain the longest common words using the following algorithm
```
Initialize an empty list LCS  = []
i = length(DP) - 1, j = length(DP[0]) - 1
While i != 0 and j != 0:
	If TOT[i] == TNT[j]:
		LCS = [TOT[i], i, j] + LCS
	Else : 
		If DP[i][j - 1] >= DP[i - 1][j]:
			j = j - 1
		Else if DP[i][j - 1] < DP[i - 1][j]:
			i = i – 1
```
In the resulting LCS list, each element is a tuple containing the common word, the index corresponding to the old text (index_old), and the index corresponding to the new text (index_new).
<div align="center">
    
**LCS = [common word, old_index, new_index]**
</div>

**Old_index**: Refers to the index of the word in the Tokenized Old Text (TOT), indicating its position within the original text.

**New_index**: Denotes the index of the word in the Tokenized New Text (TNT), representing its location within the modified or new text.


> Note\
If **TNT** is empty, new_index is set to “None”.\
If **TOT** is empty, old_index is set to “None”.



### Generating the Commit Data
Using the Longest Common Subsequences (LCS) method, the process involves identifying common words and determining **insertions** and **deletions**, incorporating index values for precision. Allow me to elucidate this process with an example:

Let's consider:
<div align="center">
    
**TOT** = ["Hello", "I", "am", "Khritish"]\
**TNT** = ["Hello", "I", "Romen"]
</div>

#### Step 1: Generate the Longest Common Subsequence, LCS
<div align="center">
    
**LCS** = [("Hello", 0, 0), ("I", 1, 1)]
</div>
Here, the LCS tuple ("Hello", 0, 0) signifies that the common word "Hello" appears at index 0 in both TOT and TNT.
("Hello", Index in TNT, Index in TOT)

#### Step 2: Obtain the Deletion Data
<div align="center">
 
**Deletion** = TOT - LCS\
**Deletion** = ["Hello", "I", "am", "Khritish"] - [("Hello", 0, 0), ("I", 1, 1)]\
**Deletion** = [("am", 2), ("Khritish", 3)]
</div>
In the deletion data, each tuple contains the word to be deleted and its corresponding index in TOT.

#### Step 3: Extract the Insertion Data
<div align="center">
 
**Insertion** = TNT - LCS\
**Insertion** = ["Hello", "I", "Romen"] - [("Hello", 0, 0), ("I", 1, 1)]\
**Insertion** = [("Romen", 2)]
</div>

Similarly, in the insertion data, each tuple contains the word to be inserted and its corresponding index in TNT.

Commit Data Format:
The final data stored in each commit is represented as a hashmap, where the key denotes the line number, and the corresponding value is a tuple containing insertion and deletion data.

<div align="center">
 
**Commit Data** = {Line number: (Insertion, Deletion)}
</div>

>Where:\
Insertion = [(word to be inserted, corresponding index in TNT)]\
Deletion = [(word to be deleted, corresponding index in TOT)]

This structured approach ensures precise recording of insertion and deletion operations, facilitating accurate reconstruction of texts during version control operations.




### Reconstruction Mechanism

The reconstruction process involves building files for a specified commit using the initial or 0th commit, leveraging commit data. As previously outlined, commit data encapsulates structured information facilitating the transformation of an old text file into a new text file.

To illustrate, consider the task of constructing a file, say "new.txt," from commit 3. This can be accomplished by using the initial version of "new.txt" (old.txt) found in commit 0, along with the commit data stored in commit 3. Each line in "old.txt" is converted to its corresponding line in "new.txt."

Here is a step-by-step breakdown of the reconstruction process:

- Create an empty list/array of length L, where L is given by the formula
> L = length( old_line ) + Li − Ld\
Li = length ( insertion_array_in_commit_data)\
Ld=length(deletion_array_in_commit_data)
This list represents the corresponding lines in "new.txt."
- Since the newly generated list mirrors the lines in the new file, insert the insertion word at the new file index (available in the commit data) to avoid word collisions.
- Delete the word from the old file line based on the deletion word (available in the commit data) at the old file index.
- After deletion, insert the remaining words from the old line in a first-come-first-serve basis at the empty places in the generated list. This completes the generation of the final new line.

**For example:**

**Old line**: "Words are good but not bad"\
**New line**: "Words will be good sword"

**OLD (Tokenized)**: ["Words", "are", "good", "but", "not", "bad"]\
**NEW (Tokenized)**: ["Words", "will", "be", "good", "sword"]


Corresponding commit data for the conversion from OLD to NEW:
<div align="center">
 
**Commit data**: ( [(will, 1), (be, 2), (sword, 4)], [(are, 1), (but, 3), (not, 4), (bad, 5)] )
</div>
Here,

Insertion array: [(will, 1), (be, 2), (sword, 4)]\
> Li = length(Insertion array) = 3

Deletion array: [(are, 1), (but, 3), (not, 4), (bad, 5)]\
> Ld = length(Deletion array) = 4

L = length(OLD) + Li − Ld = 6+3−4=5

#### Step 1: Empty list of length L, ARR
<div align="center">
 
ARR = [ Ø , Ø , Ø, Ø, Ø]
</div>
> (Ø represents an empty place)

#### Step 2: Insert the word into ARR
<div align="center">
 
ARR = [Ø , will, be, Ø, sword]
</div>

#### Step 3: Deletion of words from OLD
<div align="center">
 
OLD = ["Words", "are", "good", "but", "not", "bad"]\
OLD = ["Words", "good"]
</div>

#### Step 4: Insert the leftover words in OLD in a first-come-first-insert basis into the empty slots of ARR
<div align="center">
 
ARR = ["Words", "will", "be", "good", "sword"]
</div>
This reconstruction process successfully transforms the new line from the old line with the aid of commit data.

## File Structures:
### Commit Data Line
**Structure: [&lt; insertion array &gt;, &lt; deletion array &gt;]** (List Data Structure used)

**&lt; insertion array &gt;** = [(&lt; word to be inserted &gt;, &lt; index in new line &gt)]

**&lt; deletion array &gt;** = [(&lt; word to be deleted &gt;, &lt; index in old line &gt)]

**Example:**

&lt; insertion array &gt; = [(‘hi’,0), (‘there’,5)]

&lt; deletion array &gt; =  [(‘why’,2)]

Commit Data Line = [ [(‘hi’,0), (‘there’,5)], [(‘why’,2)] ]

### Commit Data File
**Structure = {key=&lt;line no.&gt;, value=&lt;commit data line&gt;}** (Hashmap or Dictionary Data Structure used)

**Example**

{1: [ [(‘hi’,0), (‘there’,5)], [(‘why’,2)] ]}

### Track file
**Structure: &lt; commit id &gt; \u00b6 &lt; commit data &gt;**

&lt; commit data &gt; : &lt; line number &gt; \u00b6 &lt; insertion length &gt; \u00b6 &lt; deletion length &gt; \u00b6 &lt; ins_word1 &gt; \u00b6 &lt; ins_index1 &gt; ...\u00b6 &lt; del_word1 &gt; \u00b6 &lt; del_index1 &gt; ...

**Example:**

Let Commit Data:

0: [ [(‘hi’,0),(‘hello’,2)], [(‘there’,3),(‘where’, 4)] ]

1: [ [(‘why’,3),(‘quit’,5)], [(‘since’,2),(‘sleep’, 6)] ]

Let commit id = 3

3¶0¶2¶2¶hi¶0¶hello¶2¶there¶3¶where¶4¶1¶why¶3¶quit¶5¶since¶2¶sleep¶6\n

## Documentation
### File: `lcs.py`
#### Function:
```
def LongestCommonSubsequences(old_line, new_line):
    """
    This function finds the Longest Common Subsequences (LCS) between two lines of text,
    and generates commit data based on the changes between the lines.

    Args:
        old_line (str): The original line of text.
        new_line (str): The modified line of text.

    Returns:
        tuple: A tuple containing two elements:
            - lcs (list): A list of tuples representing the LCS. Each tuple contains:
                - common_word (str): The common word between the lines.
                - old_line_index (int): The index of the common word in the old line.
                - new_line_index (int): The index of the common word in the new line.
            - commit_data (list): A list containing two lists:
                - insertions (list): A list of tuples representing inserted words. Each tuple contains:
                    - word (str): The inserted word.
                    - index (int): The index where the word was inserted in the new line.
                - deletions (list): A list of tuples representing deleted words. Each tuple contains:
                    - word (str): The deleted word.
                    - index (int): The index where the word was present in the old line.
    """
```
#### Description:

This function implements the Longest Common Subsequence (LCS) algorithm to find the longest sequence of words that appear in both the `old_line` and the `new_line`. It then uses the LCS information to generate commit data that reflects the changes made between the two lines.
The commit data consists of two lists:
- `insertions`: A list of tuples containing the words that were inserted in the new_line compared to the old_line.
- `deletions`: A list of tuples containing the words that were deleted from the old_line when compared to the new_line.

#### Algorithm:

1. **Split Lines**: The function first splits both `old_line` and `new_line` into lists of individual words.
2. **Dynamic Programming**: It then uses a dynamic programming approach to calculate the length of the LCS. A 2D DP table (`dp`) is used to store the LCS length for all possible sub-problems.
3. **Backtracking**: After finding the LCS length, the function backtracks through the DP table to reconstruct the actual LCS sequence. It retrieves the common words along with their corresponding indices in both the original and modified lines.
4. **Generate Commit Data**: Finally, it uses the LCS information to identify insertions and deletions. Words present in the `new_line` but not in the LCS are considered insertions, while words present in the `old_line` but not in the LCS are considered deletions.

#### Example Usage:
```
old_line = "This is the old line."
new_line = "This is a modified line."

lcs, commit_data = LongestCommonSubsequences(old_line, new_line)
print("Longest Common Subsequence:", lcs)
print("Commit Data:", commit_data)
```
This indicates that "a modified" were inserted in the new line, while "old" was deleted from the old line.

---
### File: `reconstruct.py`
This file defines functions for reconstructing new versions of files based on their original content and commit data generated by the `passport` system.

#### Functions
- **reconstruct(old_line, commit_data_line):**
  - **Description:**
    - Takes the original line of text (`old_line`) and its corresponding commit data (`commit_data_line`) as input.
    - Generates the new line of text after applying the changes specified in the commit data.
  - **Parameters:**
    - `old_line` (str): The original line of text.
    - `commit_data_line` (list): A list containing two lists:
      - `insertions` (list): A list of inserted words in the new line.
      - `deletions` (list): A list of deleted words from the old line.
  - **Return Value:**
    - `str`: The reconstructed line of text with insertions and deletions applied.
- **reconstruct_file(old_file_location, commit_data):**
  - **Description:**
    - Reconstructs a new version of a file based on its original location (`old_file_location`) and the commit data (`commit_data`) associated with that file.
  - **Parameters:**
    - `old_file_location` (str): The path to the original file.
    - `commit_data` (list): A list of commit data lines corresponding to each line in the original file.
  - **Return Value:**
    - `list`: A list of strings representing the reconstructed lines of the new file

#### Notes:
- Both functions assume that the `commit_data` format is valid and aligns with the structure generated by the `lcs.LongestCommonSubsequences` function.
- The `reconstruct_file` function handles cases where the lengths of the original lines and the commit data might differ due to insertions or deletions.
- The `reconstruct_file` function includes basic error handling to print an error message in case of unexpected issues.

#### Example Usage:
```
# Assuming you have commit data generated for a file

old_file_location = "my_file.txt"
commit_data = [# List of commit data lines for each original line in the file]

new_file_content = reconstruct_file(old_file_location, commit_data)

# Write the reconstructed content to a new file (optional)
with open("my_file_new.txt", "w") as f:
    f.writelines(new_file_content)
```
---
### File: `commit_data_file.py`
```
def commit_data_file(old_file_location, new_file_location):
    """
    This function generates commit data for a file based on the differences between its original and modified versions.

    Args:
        old_file_location (str): The path to the original file.
        new_file_location (str): The path to the modified file.

    Returns:
        dict: A dictionary mapping line numbers (integers) to their corresponding commit data (lists). The commit data list contains two sub-lists:
            - insertions (list): A list of inserted words in the new line.
            - deletions (list): A list of deleted words from the old line.

    Raises:
        SystemExit: If either the original or modified file location is invalid.
    """
```
#### Description:
This function takes the paths to the original and modified versions of a file as input. It then performs the following steps:
1. **Validate File Locations:**
   - Uses `os.path.abspath` to ensure absolute paths for both files.
   - Checks if both files exist using `os.path.exists`.
   - If either file is not found, displays an error message using the `terminal_output` module (assumed) and exits the program.
2. **Read File Contents:**
   - Opens the original and modified files using `open`.
   - Reads the lines from each file and removes trailing newline characters using `rstrip("\n")`.
   - Closes the files.
4. **Generate Commit Data:**
   - Initializes an empty dictionary `commit_data` to store line-wise commit data.
   - Iterates through a maximum of the lengths of the original and modified lines:
     - Handles potential index errors by using `try-except` blocks.
     - Gets the corresponding lines from the original (`old_line`) and modified (`new_line`) files.
     - Calls the `LCS.LongestCommonSubsequences` function from the `lcs` module to find the LCS and generate commit data (`cd`).
     - Stores the commit data for the current line (`i`) in the `commit_data` dictionary.
6. **Return Commit Data:**
   - Returns the `commit_data` dictionary containing commit data for each line.
#### Example Usage:
```
old_file_location = "path/to/old_file.txt"
new_file_location = "path/to/new_file.txt"

commit_data = commit_data_file(old_file_location, new_file_location)

# Use the commit_data for further processing or storage within the "passport" system
```
This example demonstrates how to use the commit_data_file function to generate commit data for a file based on its original and modified versions.

---
### File: `cli.py`
This code implements the command-line interface (CLI) for PASTPORT.

#### Initialization:
- The `welcome_mssg` function displays a welcome message with colored text using the `terminal_output` module.
- The script prompts the user for the location of the PASTPORT directory. It validates the existence of the directory and exits if not found.
- The location is converted to an absolute path using `os.path.abspath`.

#### Main Loop:
- The script enters a loop that continuously prompts the user for commands.
- User input is split into a list of arguments using shlex.split.
- The first element is considered the main command, and the remaining elements are arguments.

#### Available Commands
- **q or quit:** Exits the PASTPORT CLI.
- **h or help:** Displays help information using the `help.help` function.
- **init:** Initializes PASTPORT in the specified location using init.pastport_init.
- **add:**
  - Supports two flags:
    -  `-a`: Adds all untracked files in the current directory to the staging area using `stage.pastport_stage`.
    -  `-p`: Prompts the user for specific files to add to the staging area using `stage.pastport_stage`.
  -  Displays a success message if files are added successfully.
- **status**
  -  Uses `status.pastport_status` to retrieve information about untracked, deleted, and modified files.
  -  Shortens path lengths using `path_shorten.path_shorten` for better display.
  -  Prints the status information with colors for easy identification.
- **commit**
  - Checks if PASTPORT is already initialized in the directory.
  -  Supports an optional commit message argument (`-m`).
  -  Reads the `.stage` file to get file paths and commit IDs for staged files.
  -  Performs the commit operation for each staged file using `commit.pastport_commit`.
  -  Copies the staging information to the `.stagelog` file and empties the `.stage` file.
  -  Displays a success message after a successful commit.
- **log**
  -  Supports optional flags:
    -  `-lp`: Lists all commits in detail (long format).
    -  `-sp`: Lists commits with shortened paths (short format).
  -  Reads the `.stagelog` file to retrieve commit history data.
  -  Presents the commit information in a table format using the `terminal_output` module.
- **checkout**
  -  Supports two flags:
    -  `-p`: Checks out specific files to a particular commit version based on provided paths and commit IDs. Uses `chk.pastport_checkout` for checkout operation.
    -  `-s`: Checks out the entire working directory to a specific stage version based on the stage ID. Uses `chk.pastport_checkout` for checkout operation.
  -  Validates user input and handles errors for invalid paths, commit IDs, or stage IDs.

#### Error Handling:
  - The script displays error messages using the `terminal_output` module with red color for better visibility.
  - It exits the program if the PASTPORT directory is not found during initialization.

Overall, this code provides a functional CLI for PASTPORT with basic functionalities like initialization, adding/staging files, committing changes, viewing commit history, and checking out specific versions of files.

---
### File: `init.py`
#### Functions
1. **pastport_init(location):**
   - Initializes PASTPORT in the specified location.
   - Creates a metadata directory named `.pastport\u00b6` within the location.
   - Stages all files in the current directory and subdirectories using `stage.pastport_stage`.
   - Performs an initial commit for all staged files using `commit.pastport_commit`.
   - Sets a global `success_status` flag to indicate success or failure of the initialization process.

2. **create_metadata(location):**
   - Recursively creates the `.pastport\u00b6` metadata directory in all subdirectories.
   - Excludes the `.pastport\u00b6` directory itself from recursion.
   - Stages all files in the current directory using `stage.pastport_stage`.
   - Performs an initial commit for all staged files using `commit.pastport_commit`.
   - Handles potential exceptions during the initialization process and sets the `success_status` flag accordingly.

#### Example Usage:
To use this code, you would call the `pastport_init` function with the desired location:
```
import init

location = "/path/to/your/project"
init.pastport_init(location)
```

---
### File: `commit.py`

#### Functionality:
The `pastport_commit` function is responsible for committing changes to a file within the PASTPORT system. It performs the following key tasks:
1. **Retrieves Old and New File Locations:**
   - Determines the absolute path of the new file location.
   - Finds the corresponding old file location within the `.pastport\u00b6` directory.
2. **Generates Commit Data:**
   - Uses the `commit_data_file` module to calculate the commit data for the modified lines between the old and new files.
3. **Updates Track File:**
   - If the old file exists:
     - Reads the existing track file to determine the last commit ID.
     - Appends the new commit data to the track file, including the commit ID, line-based commit data, and commit message.
   - If the old file doesn't exist (new file):
     - Creates a new track file.
     - Writes the initial commit ID (0) and commit message.
     - Appends the commit data for the entire file.
#### Example Usage:
```
import pastport

file_location = "path/to/your/file.txt"
pastport.pastport_commit(file_location, commit_message="My first commit")
```
---
### File: `stage.py`
This code defines the `pastport_stage` function, which is responsible for staging files in the PASTPORT version control system.

#### Functions
1. **Retrieves Absolute Path:**
   - Converts the provided `pastport_root_location` to an absolute path for consistency.
2. **Processes Based on Flag:**
   - `-p` **(path)**:
     - Prompts the user for individual file paths until they confirm with "y/Y".
     - Validates each path:
       - Ensures the path exists.
       - Checks if the path is within the PASTPORT root location.
     - Calls get_last_commit_id to retrieve the last commit ID for each valid file.
   - `-a` **(add all)**:
     - Uses a recursive function stage_recursion to traverse the PASTPORT root directory and its subdirectories (excluding the .pastport\u00b6 directory itself).
     - For each file encountered, calls get_last_commit_id to retrieve a commit ID (0 for new files).
3. **Generates Stage Data:**
   - Determines the stage ID by reading the last line of the `.pastport\u00b6/pastport.stagelog` file (if it exists) and incrementing it.
   - Creates a dictionary `file_paths_commit_ids` to store file paths as keys and corresponding commit IDs as values.
4. **Writes Stage Information:**
     - Creates the `.pastport\u00b6/pastport.stage` file:
       - If any files were staged (`len(file_paths_commit_ids`) != 0):
         - Writes the stage ID.
         - Writes each file path and its commit ID separated by a delimiter (`\u00b6`).
       - If no files were staged (`else` block for `-a` flag):
         - Writes 0 as the stage ID for new files.
         - Writes each file path and 0 as the commit ID.
         - Optionally writes "Pastport Initiation" as the initial commit message (assuming this happens during initialization in `init.py`).
     - Closes the `.pastport\u00b6/pastport.stage` file.
5. `get_last_commit_id` **Function (Helper):**
   - Takes a file path as input.
   - Constructs the corresponding track file path within the `.pastport\u00b6` directory.
   - If the track file exists:
     - Reads the last line and extracts the commit ID.
     - Returns the commit ID.
   - If the track file doesn't exist (new file):
     - Returns -1, indicating an untracked file (commit ID will become 0 on the next commit).

---
### File: `status.py`
This code defines the `pastport_status` function, which helps determine the status of files within a PASTPORT repository.

#### Functions
1. **Lists:**
   - Initializes empty lists to store untracked, deleted, and modified files.
2. **Recursive Status Check:**
   - Defines the `status_recursion` function to traverse the PASTPORT root directory and its subdirectories (excluding the `.pastport\u00b6` directory itself).
   - **Untracked Files:**
     - Checks for files in the current directory that are not present in the .pastport\u00b6 directory.
     - If found, adds the file path to the untracked_files list.
   - **Modified Files:**
     - Checks for files that exist in both the current directory and the `.pastport\u00b6` directory.
     - Attempts to read the corresponding `.track` file (error handling included).
     - Extracts commit data using the `checkout.extract_commit_data` function.
     - Reconstructs the file content based on the track data using the `reconstruct.reconstruct_file` function.
     - Compares the reconstructed and actual file content using the `check_equal` function.
     - If the content differs, adds the file path to the `modified_files` list.
   - **Deleted Files:**
     - Iterates through the files within the `.pastport\u00b6` directory.
     - Excludes system files like `.stagelog`, `.stage`, and `.track`.
     - If a deleted file is found, adds its path to the `deleted_files` list.
   - **Recursion:**
     - For subdirectories, calls status_recursion recursively to continue the status check.
3. **Returns Status:**
   - After traversing the entire directory structure, returns the lists of untracked, deleted, and modified files.

---
### File: `checkout.py`
This code defines the `pastport_checkout` function, which allows users to retrieve specific versions of files from the PASTPORT repository.

#### Functions
1. **Checks Existing File:**
   - Determines the file name with extension and the corresponding old file location within the `.pastport\u00b6` directory.
   - If the new file location already exists:
     - Calls the `normal_checkout` function to handle the checkout process.
   - If the new file location doesn't exist:
     - Checks if the old file location exists (deleted file scenario).
     - If the old file location exists:
       - Calls the `deleted_checkout` function to reconstruct the file based on the specified commit ID.
     - If neither the new nor the old file location exists:
       - Displays an error message indicating an unknown and untracked file.
2. `normal_checkout` **Function:**
   - Handles checkout for existing files:
     - If the commit ID is 0 (initial commit), copies the old file to the new location.
     - Otherwise:
       - Extracts the track file location based on the new file location.
       - Reads the specified line (commit ID) from the track file (error handling included).
       - Extracts commit data using the `extract_commit_data` function.
       - Reconstructs the file content using `reconstruct.reconstruct_file`.
       - Writes the reconstructed content to the new file location.
3. `deleted_checkout` **Function:**
   - Handles checkout for deleted files:
     - If the commit ID is 0 (initial commit), copies the old file to a new location with the original name (assuming it was deleted).
     - Otherwise:
       - Extracts track file and new file locations based on the old file location.
       - Reads the specified line (commit ID) from the track file (error handling included).
       - Extracts commit data using the `extract_commit_data` function.
       - Reconstructs the file content using `reconstruct.reconstruct_file`.
       - Writes the reconstructed content to the new file location.
4. `extract_commit_data` **Function:**
   - Takes a line from the track file as input.
   - Splits the line based on a delimiter (`\u00b6`).
   - Extracts the commit message from the last element.
   - Iterates through the remaining elements to parse commit data for each line:
     - Extracts line number, insertion length, and deletion length.
     - Processes insertions: extracts the inserted word and its index.
     - Processes deletions: extracts the deleted word and its index.
   - Builds a dictionary containing line-based insertion and deletion information.
   - Returns the constructed commit data dictionary.

---
### File: `path_shorten.py`
This code defines a class-based approach for shortening file paths.

**Classes:**
- **PathNode:**
  - Represents a single directory node in a tree structure.
  - Stores:
    - `dir_name`: The name of the directory.
    - `path_tag`: Boolean flag indicating if this node represents a significant part of the path to keep.
    - `sub_dir`: Dictionary mapping subdirectory names to child PathNode objects.
- **PathShortener:**
  - Takes a list of paths as input during initialization.
  - Maintains a `root` node representing the starting point of the tree structure.
  - `addPath` function:
    - Splits the path into a list of directories using `os.path.basename` and `os.path.dirname`.
    - Iterates through the list from the end (deepest directory):
      - Creates `PathNode` objects for encountered directories if they don't exist.
      - Sets the `path_tag` to `True` for the first directory, the second-to-last directory, and the last directory in the path (representing significant parts to keep).
  - `destroy` function:
    - Resets the `root` node back to an empty state.
  - `getPaths` function:
    - Initializes an empty list `self.res` to store shortened paths.
    - Defines a recursive helper function `f`:
      - If the current node's `path_tag` is `True`:
        - Appends the directory name with ">>" to the current path.
      - Recursively calls `f` for each child node.
      - If there are no child nodes (leaf node):
        - Appends a shortened version of the current path to `self.res`. It keeps the first two characters (likely drive letter for absolute paths), an ellipsis ("...") indicating omitted directories, and the last two characters (likely filename extension).
    - Calls `f` with the `root` node and an empty string as initial path.
    - Returns the list of shortened paths (`self.res`).
**Function**
  - `path_shorten` function
    - Creates a PathShortener object with the provided list of paths.
    - Calls getPaths on the object to obtain shortened paths.
    - Calls destroy on the object (optional, presumably for memory management).
    - Returns the list of shortened paths.

**Functionality:**
This code builds a tree structure representing the directory hierarchy of the provided paths. It then identifies and marks specific directories to keep based on their position within the path (first, second-to-last, and last). Finally, it traverses the tree and creates shortened paths by keeping the marked directories and using "..." to represent omitted directories in between.


---
### File: `terminal_output.py`
This code defines a function `output` for printing messages to the terminal with optional color and line ending control.

**Functionality:**
- Takes three arguments:
  - `message`: The text to be printed.
  - `color` (optional): A string representing the desired color for the message (default is no color).
  - `ends` (optional): A string specifying the character(s) to print at the end of the line (default is newline \n).
- Checks the provided `color` (converted to lowercase) and prints the message with ANSI escape sequences to achieve the desired terminal color.
  - Supports the following colors:
    - red (r)
    - green (g)
    - amber (a)
    - blue (b)
    - pink (p)
    - cyan (c)
- If no color is specified or an invalid color is provided, the message is printed with a default white text color.
- Prints the message with the specified `ends` character(s).

---
### File: `help.py`
This code defines functions for displaying help messages for a command-line interface (CLI) application.

**Functionality:**

- `print_message` **Function:**
  - Takes various arguments to format and print a help message for a single command.
    - `count`: An optional integer to number the commands sequentially.
    - `command`: The name of the command.
    - `description`: A description of the command's purpose.
    - `sub_commands_description`: A dictionary containing descriptions for sub-commands (optional).
    - `example`: A list of example usage strings for the command.
  - Uses `terminal_output` to print colored and formatted text elements.
  - Displays information in a structured format, including command name (cyan), description (green), sub-command descriptions (blue), and examples (indented with a diamond bullet point).
- `help` **Function**:
  - Defines help messages for various commands in the PASTPORT system.
  - For each command:
    - Sets `command`, `description`, and optionally `example` arguments.
    - Creates a dictionary `sub_commands_description` for sub-commands with explanations (if applicable).
    - Calls `print_message` with the prepared information to display the formatted help message.
