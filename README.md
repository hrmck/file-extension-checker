# File Extension Checker
This is a script/utility to help me check if the subdirectories (that has unknown level) contain suitable files.  
It scans the directory recursively, get all the file names and check if it has correct extension.

## Set up config
It is in JSON format, inside it there are three parts.  
`base_directory`: the root directory path to scan  
`submission_name_regex`: the regex pattern for submission directory name  
`file_extensions`: the file extensions that should exist in the submission  
You may also check the template file provided.  

### Example
Suppose each subdirectory should have one .sql file and one .txt file.  
We have a file structure like this in `/home/downloaded`:  
```
.  
+-- submission_1  
|	+-- text  
|	|	+-- textfile.txt  
|	+-- query.md  
+-- submission_2  
|	+-- textfile.txt  
+-- submission_3  
|	+-- textfile.txt  
|	+-- query.sql  
+-- submission_4  
	+-- textfile.txt  
	+-- query.png  
```

Then the config file should look like this:  
```JSON
{
    "base_directory": "/home/downloaded",
    "submission_name_regex": "submission_[0-9]{1}",
    "file_extensions": [
        {
            "name": ".sql",
            "amount": 1
        },
        {
            "name": ".txt",
            "amount": 1
        }
    ]
}
```

## Run
`py main.py <path_to_config_file>`
