import os 
import yaml 
from datum import DogsDATAClassifier
from models import DogsClassifier
from utils.utils import show_batch,visualize_model
from lightning.pytorch import loggers as pl_loggers
from lightning.pytorch.profilers import PyTorchProfiler
from lightning.pytorch.callbacks import (
    DeviceStatsMonitor,
    EarlyStopping,
    LearningRateMonitor,
    ModelCheckpoint,
    ModelPruning
)
from lightning.pytorch.callbacks.progress import TQDMProgressBar
import lightning as pl 

pl.seed_everything(3,workers=True)

with open( os.path.join(os.path.dirname(__file__),'config','configs.yaml') ) as f:
    config = yaml.safe_load(f)


dm = DogsDATAClassifier(
                dl_path= config['DATA'].get('PATH',None),
                num_workers=config['DATA'].get('num_workers',None),
                batch_size=config['DATA'].get('batch_size',None),
)

batch = next(iter(dm.train_dataloader()))
print(len(batch), type(batch[0]) , type(batch[1]), batch[0].shape , len(batch[1]))


model = DogsClassifier(
                    lr=config['MODEL'].get('lr',None),
                    model_name=config['MODEL'].get('name',None),
                    num_classes=config['MODEL'].get('num_class',None),
                    pretrain=config['MODEL'].get('pretrain',None),
        )
model.example_input_array = batch[0]

## Loggers
logger:pl_loggers.TensorBoardLogger = pl_loggers.TensorBoardLogger(save_dir='logs/',name= "lightning_logs",log_graph=True) 

## CallBacks
call_backs = [
    TQDMProgressBar(refresh_rate=10),
    ModelCheckpoint(
        monitor="val_loss", dirpath=os.path.join('logs','chkpoints'), filename="{epoch:02d}",save_top_k=1,
    ),
    DeviceStatsMonitor(cpu_stats=True),
    # EarlyStopping(monitor="val/loss",mode='min'),
    LearningRateMonitor(logging_interval='step')
]


## Trainer
trainer  = pl.Trainer(
                max_epochs=config['Training'].get('num_epochs',15),
                logger=logger,
                profiler='pytorch',#perf_profiler,#'advanced',
                callbacks=call_backs,
                precision=config['Training'].get('precision',15),
                enable_model_summary=False,
                enable_progress_bar=True,
                accelerator="auto",
             )



## Training
trainer.fit(model=model,datamodule=dm)
## Validation
trainer.validate(model,datamodule=dm)