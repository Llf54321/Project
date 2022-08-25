# Individual Research Project

## Project Description
In this project, mass spectrum, appearance energy and total ionization cross section data are crawled from two web database, NIST Chemistry Webbook and Electron-Impact Cross Sections for Ionization and Excitation Database. Based on these data, the optional fragments, branching ratios and partial ionization cross sections are obtained. A SQL database is built to store these data. Besides, the correlation between branching ratio and appearance energy is discussed in this project.

## Enviroment
This program is written by Python 3.9.0 on Windows system.  
The Chrome driver path is C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe

## Required Dependencies
The dependencies are as followings:
1. numpy
2. jcamp
3. selenium
4. camelot
5. sklearn
6. matplotlib
7. tqdm
8. scipy
9. pandas
10. math

## Instructions
Download codes:
```Bash
git clone https://github.com/Llf54321/Project.git
```

Required original files:
* stable-isotopes.pdf: a pdf about mass and abundance of elements.
* species.txt: the list of species used to search mass spectrum data from website.

Introduce the steps of the program, the running order of the files and the relevant outputs:
1. scrawl mass spectrum data:
    1. crawler.py: some codes in python used to crawl original mass spectrum files.  
    relevant output is data: a folder contained the crawled mass spectrum data files.
    2. process_original_data.py: some codes in python used to extract the relevant information from original data files.  
    relevant output are original_data.npy: a file to pass dictionary data about whole original mass spectrum data and new_data.npy: a file to pass dictionary data about a part of original mass spectrum data. Besides, there are three figures to show the features of the species formula data, num_of_atoms_in_molecule.png, num_of_atoms_in_part_collection.png and num_of_atoms_in_whole_collection.png.  
2. find the optional fragments and branching ratios:
    1. table_of_mass_abundances.py: some codes in python used to extract information from stable-isotopes.pdf.  
    relevant output is mass_abundance.npy: a file to pass dictionary data about mass and the corresponding abundance of isotope data.  
    2. optional_fragments.py: some codes in python used to find the optional fragments and branching ratios.  
    relevant output is processed_data.npy: a file to pass dictionary data about mass spectrum, optional fragment and branching ration data.  
3. build a database and store these data:
    1. build_database.py: some codes in python used to build a database and store main data.  
    relevant output is a table in the database.  
4. crawl total ionisation cross section data:
    1. crawl_energy_vs_total_BEB_data.py: some codes in python used to crawl total inizatoin cross section data and save them in the database.  
    relevant output is a table in the database.  
5. crawl appearance energy data:
    1. crawl_appearance_energy.py: some codes in python used to crawl appearance energy data and save them in the database.  
    relevant output is a table in the database and name_AE.npy: a file to pass dictionary data about appearance energy data.  
6. calculate partial ionisation cross sections:
    1. calculate_partial_BEB.py: some codes in python used to find partial inization cross section data and save them in the database.  
    relevant output is a table in the database.  
7. analyze data:
    1. correlation_between_AE_and_branching_ratio.py: some codes in python used to find the correlation between appearance energy and branching ratio.  
    relevant outputs are Gaussian regression.png: Gaussian regression model for the correlation, linear regression.png: linear regression model for the correlation, quadratic regression.png: quadratic regression model for the correlation, Exponential function regression.png: check if it is a exponential regression compared to power regression, loglog linear regression.png: check if it is a power regression compared to exponential regression and power function regression: power regression model for the correlation.  
    2. plot_partial_ionization_cross_sections.py: some codes in python used to plot total and partial ionization cross sections.  
    relevant output is total_and_partial_ionization_cross_sections_of_Methane.png: a sample of plot_partial_ionization_cross_sections.py

Other files:
* crawler_method.py: some functions in python about crawling data from website.
* test_database.py: some codes in python used to test the program.
* pytest_result.png: a screenshot of the pytest result

The database:
* data-20.db: a SQLite database used to store all data with four tables.
