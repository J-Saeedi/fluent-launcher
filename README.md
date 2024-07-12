# fluent-launcher
 > simple fluent launcher for multiple cases and data

## Introduce
This is a Python application designed to automate the process of running Ansys Fluent, a software used for computational fluid dynamics (CFD). The application is specifically developed to handle large numbers of case files, making it easier to run simulations and save the results for future analysis and post-processing.

## Installation
To install the application on the **Windows**, you can use pre-compiled binary versions. You can download it through the link below. Additionally, if you need to use this software on other operating systems, you can easily install Python from the program's source and use the software.

 - [Download installer for windows](https://github.com/J-Saeedi/fluent-launcher/releases/latest/download/fluent-launcher-setup.msi) 
  - [Use source code with python](https://github.com/J-Saeedi/fluent-launcher/archive/refs/heads/main.zip)

## Usage

### directory structure
The working directory should contain a `case_list.txt` file which each line of it has address of each simulation (containing case and data).
Also, at the current version, all of the case and data should have __same name__.
```bash
working-directory
├── case_list.txt
├── simulation_1
│   ├── case_and_data.cas.h5
│   └── case_and_data.dat.h5
├── simulation_2
│   ├── case_and_data.cas.h5
│   └── case_and_data.dat.h5
├── simulation_3
│   ├── case_and_data.cas.h5
│   └── case_and_data.dat.h5
└── simulation_4
    ├── case_and_data.cas.h5
    └── case_and_data.dat.h5
```
The `fluent-launcher` run the simulations in row, so you can assign cpu cores to one fluent process. By default, the path of fluent binary in windows assumed as 
`C:/Program Files/ANSYS Inc/v212/fluent/ntbin/win64/fluent.exe`. Although, it is possible to change it with `--fluent` argument.

```bash
$  fluent-launcher -h
usage: fluent-launcher.exe [-h] -t CORE -m MAX_ITER -i INPUT -o OUTPUT [-c [CASE_LIST]] [--fluent [FLUENT]]

fluent-launcher for run multiple case files

optional arguments:
  -h, --help            show this help message and exit
  -t CORE, --core CORE  Number of CPU cores
  -m MAX_ITER, --max_iter MAX_ITER
                        Number of maximum iterations
  -i INPUT, --input INPUT
                        filename for input case without extensions
  -o OUTPUT, --output OUTPUT
                        filename for output case without extensions
  -c [CASE_LIST], --case_list [CASE_LIST]
                        file address of case_list.txt
  --fluent [FLUENT]     custom location of fluent.exe
```

## Example
This is an example of `fluent-launcher` in structure that introduced above.
```bash
fluent-launcher  -m 1200 -t 6 -i 'case_and_data' -o 'output' -c ./case_list.txt
```
which means:
 - `-m 1200` ➡ set maximum iterations as 1200
 - `-t 6` ➡ 6 cores will be used for fluent
  - `-i 'case_and_data'` ➡ case and data in each folder have this name
  - `-o 'output'` ➡ resultant case and data will save in output.cas.h5 and output.dat.h5
  - `-c ./case_list.txt` ➡ case_list.txt contain something like this:

    ---
            case_list.txt:
             
                   simulation_1
                   simulation_2
                   simulation_3
                   simulation_4
    ---