Pipeline for transforming data from long running study monitoring drug deaths over several years. 

Included there is: 
⦁	data sub-directory containing drug deaths.csv, the first file which is to be transformed.
⦁	2 .py files containing code, 2 .bat files used to run the code (first one to use = capstone_batch_1, for further transformations = capstone_batch_2)
⦁	Example files of data to append called drug_deaths_to_append and drug_deaths_to_append_new. To transform and append these, they need to be copied into the 
	data subdirectory and have the last modified date changed to be the most recent in the directory

Python code takes in csv file, performs basic transformations and returns new csv file.
If running code for first time, double click to run capstone_batch_1, to return first transformed file called drug_deaths_test
After this the pipeline checks for newest file in directory and second newest (second newest being the lastest modified file – after running capstone_batch_1 this will be drug_deaths_transform_orig)
For use with future filles simply add new file wanting to append to current data set to the data directory, double check the modified date of this file is the most recent date in the directory and that the data set you wish to append to has the second most recent date. 
Then, simply double click the batch bile named capstone_batch_2 to trandsorm the new data and appened it to the old data. This can be done on repeat with new data files, providing the modified date of the csv containing the data which you wish to transform is the newest in the data directory 
and the one onto which you want to append the data has the second most recent modified date. Each time a new csv is created after the first time of appeneding files, a counter is added to the end of the new file time so the most current version of the data can easily be identified.

Assumptions:

Data: in the form of csv files 
Packages installed: Ananconda, python 3.9, numpy 1.21.5, pyspellchecker 0.6.3, pandas 1.4.2, regex 2022.3.15
Environment setup: Assume have python 3.9 and Anaconda installed on local machine Need to create a conda environment called capstone1, which is the environment that the python scripts are run in 
	setup instructions for windows:
⦁	Open anaconda prompt and type the following commands:
Create environment and activate it:
⦁	conda create -n capstone1 python=3.9
⦁	conda activate capstone1
Install packages, with option ‘y’ when asked to proceed:
⦁	conda install numpy=1.21.5
⦁	conda install regex
⦁	conda install pandas=1.4.2
⦁	conda install -c conda-forge pyspellchecker
Check packages have been installed:
⦁	conda list -n capstone1 
If they have can deactivate the environment
⦁	conda deactivate 

In batch files used to run code, need to set the conda path and file path to be where they are located on local machine using to run the code.
		
Directory format: Python code and batch files are stored in directory which contains a subdirectory called ‘data’. This is where you store the original data and add the files to be modified and transformed. It is also where the modified files gets written to. 
File format: Need to check the last modified date and the second last modified dates of the files in the directory data correspond to the previously transformed file (latest file) and the file which you would like to transform and append (second latest modified file)



Data dictionary:

 Unnamed0: Row number
 ID: Study/patient ID
 Date: Date
 DateType: Date reported =1 Date of Death =0
 Age: Age
 Sex: Sex
 Race: Race
 ResidenceCity: City of residence 
 ResidenceCounty: County of residence (US)
 ResidenceState: State of residence (US)
 DeathCity: City of death (US)
 DeathCounty: County of death (US)
 Location: Location of death
 LocationifOther: If other listed as death location, location of death
 DescriptionofInjury: description of injury
 InjuryPlace: Place of injury eg. residence etc
 InjuryCity: City of injury (US)
 InjuryCounty: County of injury (US)
 InjuryState: State of injury (US)
 COD: Cause of death
 OtherSignifican: Any other significant information
 Heroin: Taken heroin
 Cocaine: Taken cocaine
 Fentanyl: Taken fentanyl
 FentanylAnalogue: Taken fentanyl analogue
 Oxycodone: Taken Oxycodone
 Oxymorphone: Taken oxymorphone
 Ethanol: Taken ethanol
 Hydrocodone: Taken hydrocodone
 Benzodiazepine: Taken benzodiazepine
 Methadone: Taken methadone
 Amphet: Taken amphet
 Tramad: Taken tramad
 MorphineNotHeroin: Taken morphine not heroin
 Hydromorphone: Taken hydromorphone
 Other: Taken other drug
 OpiateNOS:Taken opiateNOS
 AnyOpioid: Taken any opioid
 MannerofDeath: Manner of subjects death
 DeathCityGeo: City of death location – coordinates as can be used on Google maps
 ResidenceCityGeo: City of residence location – coordinates as can be used on Google maps
 InjuryCityGeo: City of injury location – coordinates as can be used on Google maps
