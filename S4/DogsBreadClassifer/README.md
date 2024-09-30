# Dosg Bread Classifier

# TODO:
- [ ] pyproject.toml
- [ ] Dockerfile
- [ ] .devcontainer
- [ ] codecov
- [ ] Docker Image to GHCR
- [ ] fail if accuracy<.95 
- [ ] store artifact

### [Dogs Dataset](https://www.kaggle.com/datasets/khushikhushikhushi/dog-breed-image-dataset)
In Order to run program successfully, modification `.env` file
###### step 1: download API key from kaggle
![kaggle key](./assets/kaggle_key.png)
- create new key
- paste it on `.env`file

###### step 2: modify .env file
```
username=
key=
```


### Project Folder Structure
```sh.
$ tree --dirsfirst -L 2 -a -I .git .
├── configs
│   ├── callbacks
│   ├── data
│   ├── experiment
│   ├── hydra
│   ├── logger
│   ├── model
│   ├── paths
│   ├── trainer
│   ├── train_old.yaml
│   └── train.yaml
├── data
├── Dockerfile
├── .gitignore
├── .python-version
├── .env
├── pyproject.toml
├── README.md
├── src
│   ├── datamodules
│   ├── infer.py
│   ├── models
│   ├── train.py
│   └── utils
└── tests
    ├── conftest.py
    ├── datamodules
    ├── models
    └── test_train.py

```

# Training, Testing
```sh
python src/train.py data.batch_size:64 model.pretrained=false trainer.max_epochs=10
```
## confusion matrix
- Train

    ![Training](./assets/confusion_matrix(train).png)

- Test

    ![Testing](./assets/confusion_matrix(test).png)



# Inference
```sh 
python src/inference.py --ckpt_path=/path/model.ckpt --input_folder=/home/path_folder --output_folder=/home/path_folder
```


# Tensorboard logs
```sh
tensorboard --logdir outputs/ --load_fast=false
```

```website
http://localhost:6006/
```