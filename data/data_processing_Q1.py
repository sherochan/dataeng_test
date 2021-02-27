import pandas as pd
import os, sys

FINAL_FOLDER = "/data/completed/"

def get_first_last_name(_name):
    """
    Assume all english, separated by white space , get first name and last_name
    
    Params:
    -------
    _name: string 
    
    Returns:
    --------
    a list, representing the [first name, last_name ]
    """
    return _name.split(" ")

def rm_preprended_zeros_price(_price):
    """
    remove whitespaces prepended to price 
    
    Params:
    -------
    _price: obj , assumed either int/float, string
    
    Returns:
    --------
    edited string with whitespaces removed, or float as it is  
    """
    if type(_price) == str:
        return _price.lstrip()
    else:
        return _price

def data_preprocess(fp):
    """
    Given absolute fp for the dataset to be processed,
    Run the processing tasks by:
        1. Delete any rows which do not have a name - drop rows where column name is empty
        2. split name field to first_name and last_name - use helper function - get_first_last_name
        3. rm any zeros prepended to the price field - use helper function - rm_preprended_zeros_price
        4. create new col if price > 100
    
    Params:
    -------
    fp: absolute file path
    
    Returns:
    --------
    dataframe or string 
    """
    # read in the file 
    print("fp = {} of type = {}".format(fp, type(fp)))
    print(os.path.isfile(fp))
    if os.path.isfile(fp):
        
        dataset = pd.read_csv(fp)
        # step 1: drop na + rm empty string
        dataset_nona = dataset.dropna(axis = 0, subset = ["name"])
        dataset_nona_no_emp_str = dataset_nona[dataset_nona["name"] != ""]

        # step 2:
        dataset_nona_no_emp_str["name"] = dataset_nona_no_emp_str["name"].apply(lambda x: get_first_last_name(x))

        #step 3:
        dataset_nona_no_emp_str["price"] = dataset_nona_no_emp_str["price"].apply(lambda x: rm_preprended_zeros_price(x))

        #step 4:
        dataset_nona_no_emp_str["above_100"] = dataset_nona_no_emp_str["price"].apply(lambda x: True if float(x) > 100 else False)
      
        return dataset_nona_no_emp_str
    else:
        return "file does not exist!"
    
if __name__ == "__main__":
    datafilepath = sys.argv[1]
    filename = os.path.split(datafilepath)[-1]
    final_path = os.path.join(FINAL_FOLDER, filename)
    if not os.path.exists(FINAL_FOLDER):
        # create folder
        os.makedirs(FINAL_FOLDER) 

    final_processed_output = data_preprocess(datafilepath)
    if type(final_processed_output) != str:
        final_processed_output.to_csv(final_path)