# Sweepers
- optuna


A sweeper is responsible for converting cmd line args into multiple jobs


Multiple jobs actually doable by `-m` flag. they why?? IG, Better way to Sweepers handle it.

- mentioning `-m` we've to do explicitly everytime, what are needs to change.
- mentioned in 'hydra.sweeper.params'  and don't need to mention explicitly just pass `-m` flag alone

e.g)
```
In jupyter,
python app.py -m ui=windows,linux       # '-m' mentioned multirun explicitly
python appp.py -m ui=[windows,linux]    # sweep over it, add --multirun to your command line
```

```pip-requirements
pip install hydra-joblib-launcher
pip install hydra-optuna-sweeper
```
```sh
hydra-core==1.3.2
hydra-joblib-launcher==1.2.0
hydra-optuna-sweeper==1.2.0
```


Demios:
- launcher: joblib
- sweeper: optuna


<!-- bool,choice,float,glob,int,interval,range,shuffle,sort,str,tag -->