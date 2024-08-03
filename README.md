# Automated chip-scale testing

Author: Tzu-Yun Chang, University: University of Southampton

This is developed to control the motion of 8SMCx-USB Stepper & DC Motor Controller by Standa to automate the positional alignment of the fibers to the grating coupler. 

For positional alignment, it currently only support grid search algorithm to optimise the optical power. The idea is to perform a search algorithm to find the power at each (x,y) points and fit it to a known function. The peak of the fitted result will be the final position of the fiber. [Not Implementd] If the maximum power is outside of the standard deviation from the given point of the initial search space, it will perform a second search centering around the point. Unfortunately, the second failure will result in "FAILED" in the report.

## Installation
Make sure to install the full Standa XIMC software package or minimally its development kit (libximc). 

The following guide on installationg of XIMC package is for Windows user only as it has not been downloaded on other platforms. If full package is installed, the `libximc` package will be installed automatically and added to pythonpath; therefore, no additional work needs to be done. However, if you were to choose to only download development kit, please launch the PowerShell in administrator mode, type in the following and replace "zip filepath" and "destination folder" with appropriate paths. 
```
Get-ChildItem -Path "<zip filepath>" -Filter "*.tar.gz" | Foreach-Object {
    tar -xvzf $_.FullName -C "<destination folder>"
}
```
This command unzip the file and stores then in the destination folder. Afterwards, add the destination folder path to the pythonpath in the environment variables.

## Usage
Before starting the autotesting, please make sure that the file is in the correct format - a comma separated .csv file. Please also make sure that the first (x0) and second (y0) columns correspond to the left-arm and the third (x1) and fourth (y1) columns correspond to the right-arm of the fiber. The command below will make sure that the .csv file is a comma-separated file but does NOT make sure that the column is in the order of (x0, y0, x1, y1). This is at the user's discretion.
```python
# .xlsx to .csv
python convert.py <C:/path/to/file.xlsx> -s="sheet 1"
```

**main.py**: This is the user interface. Running this by typing `python main.py` in your terminal.

**user_setting.yml**: This defines the appropriate settings for the controller. It is loaded everytime main.py is run.


