# 0. Instruction

GetSmells extracts code smells from Java source code using the 
[Understand API](https://scitools.com/support/understand-api-overview/). 

# 1. Prerequisites
GetSmells is written to work on either Windows or MacOS (tested on Windows 7 and MacOS 10.12)
* Understand: You must have [Understand](https://scitools.com/features/) installed locally to run the script.
  * It should be installed in the default location for your OS (`C:\Program Files\SciTools\` for Windows or
`/Applications/Understand.app` on MacOS); if it is not in the default location, you can modify the paths at 
the top of both `understandapi.py` and `understandcli.py`.
  * You can request 1-year educational license for Understand [here](https://scitools.com/student/)
* Python 3.4+: The script is written for Python 3.4+ and, on Windows, your 32-bit/64-bit version of Python 3 should match the 
bit-ness of your Understand install (developed using Python 3.6 64-bit)
* Python Libraries
  * [NumPy](https://docs.scipy.org/doc/numpy/index.html): `pip3 install numpy`

# 2. Usage
For consistency, please refer documentation in main.py 


# 3. Smells
Some extracted smells are based off the criteria outlined in [Object-Oriented Metrics in Practice](http://www.springer.com/us/book/9783540244295) by
 [Michele Lanza](http://www.inf.usi.ch/lanza/index.html) and [Radu Marinescu](http://loose.upt.ro/reengineering/research/), while others are described
 in [On the diffuseness and the impact on maintainability of code smells: a large scale empirical investigation](https://link.springer.com/article/10.1007/s10664-017-9535-z).

## 3.1 Class Level Smells
**God Class (Class-Level)**
- ATFD (Access to Foreign Data) > Few(4) 
- WMC (Weighted Method Count) >= Very High(85%) 
- TCC (Tight Class Cohesion) < 1/3

**Lazy Class (Class-Level)**
- LOC (Lines of Code) < 1st quartile of system

**Complex Class (Class-Level)**
- CMC (Complex Method Count) > 1

**Large Class (Class-Level)**
- LOC (Lines of Code) > mean of system

**Refused Bequest (Class-Level)**
- *On the diffuseness and the impact on maintainability of code smells: a large scale empirical investigation*
- Child Class overrides more than half of its parent class's methods, calculated by:
- LMC (Local Method Count) > 1/2 * TMC (Total Method Count)

**Data Class (Class-Level)**
- WMC (Weighted Method Count) <= 30 and NOPA (Number of Public Accesses) >= 3 or
- WMC (Weighted Method Count) <= 45 and NOPA (Number of Public Accesses) >= 5

**Hub-Like Dependency**
- *Automatic Detection of Instability Architectural Smells*
- ingoing dependencies > median
- outgoing dependencies > median
- |ingoing dependencies - outgoing dependencies| <  1/4 (ingoing dependencies + outgoing dependencies)

**Cyclic Dependency**
- *Automatic Detection of Instability Architectural Smells*
- involves dependency cycle

**Unhealthy Inheritance Hierarchy**
- *Hotspot Patterns: The Formal Definition and Automatic Detection of Architecture Smells*
- a parent class depends on one of its children OR
- a class depends on a parent class and all its children

**Brain Class**
- *Are all code smells harmful? A study of God Classes and Brain Classes in the evolution of three open source systems*
- not (GC) God Class
- WMC (Weighted Method Count) >= 47
- TCC (Tight Class Cohesion) < 0.5
- NBM (Number of Brain Methods) > 1 ^ LOC (Line Of Code) >= 197 OR NBM (Number of Brain Methods) = 1 ^ LOC (Line Of Code) >= 2\*197 ^ WMC (Weighted Method Count) >= 2\*47

## 3.2 Method Level Smells

**Feature Envy (Method-Level)**
- LCOM (Lack of Cohesion of Methods) >= High (73%)

**Long Method (Method-Level)**
- LOC (Lines of Code) > mean of system (revert Chris change)

**Long Parameter List (Method-Level)**
- Inputs > mean of system

**Shotgun Surgery**
- *The Evolution and Impact of Code Smells: A Case Study of Two Open Source Systems*
- CM (Changing Methods) > 10
    - CM: number of distinct methods that call a method of the class
- CC (Changing Classes) > 5
    - CC: number of classes in which the methods that call the measured method are defined
    
**Brain Method**
- *Are all code smells harmful? A study of God Classes and Brain Classes in the evolution of three open source systems*
- LOC (Lines of Code) > 65
- CYCLO (Cyclomatic Complexity) / LOC (Line of Code) >= 0.24 ^
- MAXNESTING (Maximum Nesting Level) >= 5
- NOAV (Number of Accessed Variables) >8

## 3.3 Package Level Smells
**Unstable Dependency**
- *Automatic Detection of Instability Architectural Smells*
    1. obtaining from the graph all the dependencies between packages
    2. computing the Instability metric for every package of the system;
      Ca : Afferent Couplings : The number of classes outside this category that depend upon classes within this category.
      Ce : Efferent Couplings : The number of classes inside this category that depend upon classes outside this categories.
      I : Instability : (Ce ÷ (Ca+Ce)) : This metric has the range [0,1]. I=0 indicates a maximally
    3. for every package, checking if it is afferent of a less stable package stable category. I=1 indicates a maximally instable category

**Cyclic Dependency**
- *Automatic Detection of Instability Architectural Smells*

## Files
```
getsmells
├── bin: some tools for data integration. Usages are in each py files
│   ├── androidVulProcessor.py: The motivation is that original Android vulnerability data only talks about file instead of classes.
│   ├── oneFileForOneProj.py: After vulIntegration, combining all versions together and generate one file per project
│   ├── vulIntegration.py: After main, for each [proj]-[version]-xxx-overall.csv, generate csv file that maps the counts of vulnerabilities and smells together.
├── src
│   ├── app.py: real application
│   ├── main.py: the entry point for user
│   ├── common
│   │   ├── dfs.py: Perform deep first search
│   │   ├── metricsUtil.py: Defines shared functions for [class|method]LevelSmellMetricsUtil.py
│   │   ├── statisticUtil.py: Responsible for statistics
│   │   └── __init__.py
│   ├── classLevel
│   │   ├── classLevelMetricsUtil.py
│   │   ├── classLevelSmellExtractor.py
│   │   ├── __init__.py
│   ├── methodLevel
│   │   ├── methodLevelMetricsUtil.py
│   │   ├── methodLevelSmellExtractor.py
│   │   ├── __init__.py
│   ├── packageLevel
│   │   ├── packageLevelSmellExtractor.py
│   │   ├── packageLevelSmellExtractor.py
├── README.md
├── .pylintrc
└── .gitignore 
``` 


## Useful Links
**Understand API Documentation**   
* https://scitools.com/sup/api-2/  
* https://scitools.com/documents/manuals/python/understand.html  
* https://scitools.com/documents/manuals/html/understand_api/kindApp121.html  
* https://scitools.com/documents/manuals/html/understand_api/kindApp158.html   

**Understand CLI Documentation**
* https://scitools.com/support/commandline/   
