# Individual Research Project

## Project Description
In this project, mass spectrum, appearance energy and total ionization cross section data are crawled from two web database, NIST Chemistry Webbook and Electron-Impact Cross Sections for Ionization and Excitation Database. Based on these data, the optional fragments, branching ratios and partial ionization cross sections are obtained. A SQL database is built to store these data. Besides, the correlation between branching ratio and appearance energy is discussed in this project.

## Enviroment
This program is written by Python 3.9.0 on Windows system.

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

introduce the files and their functions:
* data: a folder contained the crawled mass spectrum data files.
* build_database.py: some codes in python used to build a database and store main data.
* calculate_partial_BEB.py: some codes in python used to find partial inization cross section data and save them in the database.
* correlation_between_AE_and_branching_ratio.py: some codes in python used to find the correlation between appearance energy and branching ratio.
* crawl_appearance_energy.py: some codes in python used to crawl appearance energy data and save them in the database.
* crawl_energy_vs_total_BEB_data.py: some codes in python used to crawl total inizatoin cross section data and save them in the database.
* crawler_method.py: some functions in python about crawling data from website.
* crawler.py: some codes in python used to crawl original mass spectrum files.
* data-20.db: a SQLite database used to store all data.
* Gaussian regression.png: Gaussian regression model for the correlation.
* linear regression.png: linear regression model for the correlation.
* quadratic regression.png: quadratic regression model for the correlation.
* mass_abundance.py: a file to pass dictionary data about mass and abundance of elements.
* name_AE.npy: a file to pass dictionary data about appearance energy data.
* new_data.npy: a file to pass dictionary data about a part of original mass spectrum data.
* original_data.npy: a file to pass dictionary data about whole original mass spectrum data.
* optional_fragments.py: some codes in python used to find the optional fragments and branching ratios.
* plot_partial_ionization_cross_sections.py: some codes in python used to plot total and partial ionization cross sections.
* process_original_data.py: some codes in python used to extract the relevant information from original data files.
* processed_data.npy: a file to pass dictionary data about mass spectrum, optional fragment and branching ration data.
* species.txt: the list of species used to search mass spectrum data from website.
* stable-isotopes.pdf: a pdf about mass and abundance of elements.
* table_of_mass_abundances.py: some codes in python used to extract information from stable-isotopes.pdf.
* test_database.py: some codes in python used to test the program.
* total_and_partial_ionization_cross_sections_of_Methane.png: a sample of plot_partial_ionization_cross_sections.py
