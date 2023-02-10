from selenium import webdriver
import time
import os
import pandas as pd
import sqlite3

def main():
    current_directory = os.getcwd()
    options = webdriver.ChromeOptions();
    prefs = {"download.default_directory":"{}".format(current_directory)};
    options.add_experimental_option("prefs", prefs);
    driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options = options);

    try:
        driver.get('https://jobs.homesteadstudio.co/data-engineer/assessment/download/');
        downloadcsv = driver.find_element("xpath",'/html/body/div/div/div/div/div/div[1]/article/div/div/div/a');
        downloadcsv.click();
        time.sleep(5)
        driver.close()

    except:
        print("Invalid URL")

    print("current directory is {}".format(current_directory))

    pivot_table = convert_data_to_pivot_table(current_directory)
    insert_table_to_database(pivot_table)

def convert_data_to_pivot_table(current_directory):
    # read the data from an XLSX file
    data = pd.read_excel("{}\skill_test_data.xlsx".format(current_directory), sheet_name="data")

    # create the pivot table
    pivot_table = data.pivot_table(index=["Platform (Northbeam)"],  
                                    values=["Spend","Attributed Rev (1d)", "Imprs", "Visits", "New Visits",  "Transactions (1d)", "Email Signups (1d)"], 
                                    aggfunc="sum").reset_index()

    # sort by revenue in descending order
    pivot_table = pivot_table.sort_values(["Attributed Rev (1d)"], ascending=False)

    print(pivot_table)
    return pivot_table

def insert_table_to_database(pivot_table):
    # connect to a new SQLite database or create it if it doesn't exist
    conn = sqlite3.connect("skill_test.db")

    # insert the pivot table into the database as a new table named "pivot_table"
    pivot_table.to_sql("pivot_table", conn, if_exists="replace")

    # commit the changes and close the connection
    conn.commit()
    conn.close()
    print("Successfully added to database")
    return

if __name__ == "__main__":
    main()
