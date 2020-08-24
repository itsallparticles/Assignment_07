#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# BWayward, 2020-Aug-15 Created write_file and remove_inventory function, added DocStrings to both
# BWayward, 2020-Aug-16 Cleaned up write to file and Delete codebase, attempted to create add_inventory function(Failed)
# BWayward, 2020-Aug-17 Revisited add inventory function. added IO.addCD and DataProcessor.add_inventory
# BWayward, 2020-Aug-18 After class, added file check to ensure text file exists.
# DKlos, 2020-Aug-20, Corrections
# BWayward, 2020-Aug-21, modified txt to .dat, import pickle, Added information to read and write functions re: Binary file handling
# BWayward, 2020-Aug-22, added error handling for file missing and int check for deletion request
#------------------------------------------#
import pickle


# -- DATA -- #

strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object

# -- PROCESSING -- #
class DataProcessor:

    @staticmethod
    def remove_inventory(selectID, table):
        """ Function to manage removal of items from table in memory
        
            Args: 
                None
                
            Returns: 
                prints 'The CD was removed', and displays current inventory with item deleted
                """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == selectID:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The Compact Disc was removed')
        else:
            print('Could not find this Compact Disc!')

    @staticmethod       
    def add_inventory(strID, strTitle, strArtist, table):
        """ Processing user input into list of dicts
        
        Args: 
            userInput: Conversion of strID from string to intenger.
            dictionary: dictionary where the user input data is stored
            table: Table where dictionary is written
        Returns: 
            None """
        intID = int(strID)
        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist}
        table.append(dicRow)
        

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file

        try:
            objFile = open(file_name, 'rb') #Reads from binary file in.
            # Retrieve the preserved data (list of dictionaries) from previous write session
            data = pickle.load(objFile)
            table.extend(data)
            objFile.close()
        except FileNotFoundError as e: 
            print("\nNo Database file currently exists.  Please add and save compact disc information to create a file.\n")
            print(type(e), e, e.__doc__, sep='\n')     

    @staticmethod
    def write_file(file_name, table):
        """ Function to write data to pickled file.
            
        Writes the data to a specified file identified by file_name and 2d table.
        
        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure tha holds data during runtime
            
        Returns: 
            None.
            """

        objFile = open(file_name, 'wb')
        pickle.dump(table, objFile)
        objFile.close()
        


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')
    
    # Missing staticmethod
    @staticmethod
    def addCD():
        """ Process user input to add data 
        
        Args: 
            none
        Returns:
            none
        """

        # This is all good.    
        strID = input('Enter ID: ').strip()
        strTitle = input('What is the CD\'s title? ').strip()
        stArtist = input('What is the Artist\'s name? ').strip()
        return strID, strTitle, stArtist

# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)


# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl) #Calls function that loads text file containing CD inventory into runtime. 
            IO.show_inventory(lstTbl) #Calls function that displays inventory to user
        else:
            input('cancelling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl) #Calls function that displays inventory to user
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Calls function that asks user for new ID, CD Title and Artist
        strID, strTitle, strArtist = IO.addCD()  
        # 3.3.2 Calls the function that adds item to the table
        DataProcessor.add_inventory(strID, strTitle, strArtist, lstTbl)
        #Calls function that displays inventory with added CD
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl) # Calls function that displays current inventory
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 Calls function that displays inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        try: intIDDel = int(input('Which ID would you like to delete? ').strip()) 
        except ValueError:  
            print("\nYou must enter ID as a integer. Deleting CD failed.\n")
        # 3.5.2 Calls function that searches thru table and deletes CD
        else:  
            DataProcessor.remove_inventory(intIDDel, lstTbl)
            IO.show_inventory(lstTbl) #Calls function that displays inventory to user
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Calls function that displays current inventory. 
        IO.show_inventory(lstTbl) 
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower() #asks user for confirmation to save
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 Calls function that saves data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




