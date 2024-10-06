# DVC
git init
dvc init  ( we use dvc+supporting SCM tool always here)


<!-- add dvc -->
dvc add path/data_folder/


dvc config core.analytics false

<!-- autotage -->
dvc config core.autostage true

<!-- space check -->
dvc du path/data_folder/

<!-- check dvc remote -->
dvc remote list


<!-- GOOGLE DRive -->
```sh
$ Google API Console
>> Enable Drive API
>> create credentials >> user-data >> APP-NAme, Developer-contact, Test-User SAVE
>> **CLIENT-ID** and **CLIENT-SECRET**
```

<!-- add gdrive -->
dvc remote add --default remote-name gdrive:/GDRIVE-ID
dvc remote modify gdrive gdrive_acknowledge_abuse true

dvc remote modify gdrive gdrive_clien_id CLIENT-ID
dvc remote modify gdrive gdrive_clien_secret  CLIENT-SECRET

<!-- push to dgrive and manage -->
dvc push -r gdrive

<!-- 
    whenever data change and commit dvc md5 hash changes, do  git commit `best practise`
 -->