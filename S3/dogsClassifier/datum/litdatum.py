from lightning.pytorch.utilities.types import TRAIN_DATALOADERS
import os
import torch
from torch.utils.data import DataLoader
import lightning as pl
from torchvision import transforms
from torchvision.datasets import ImageFolder
from pathlib import Path
from typing import Union

class DogsDATAClassifier(pl.LightningDataModule):
    def __init__(self,dl_path:Union[str,Path],num_workers:int=0,batch_size:int=32) -> None:
        super().__init__()
        self._dl_path = dl_path
        self._num_workers= num_workers
        self._bs         = batch_size

    def prepare_data(self) -> None:
        ...
    
    @property
    def data_path(self):
        return Path(self._dl_path).joinpath('dogs_dataset')
    
    @property
    def normalize_transform(self):
        return transforms.Normalize(mean=[.485,.456,.406], std=[.229,.224, .225])
    
    @property
    def train_transform(self):
        return transforms.Compose([
            transforms.Resize((224,224)),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            self.normalize_transform
        ])
    
    @property
    def test_transform(self):
        return transforms.Compose([
            transforms.Resize((224,224)),
            transforms.ToTensor(),
            self.normalize_transform
        ])
    
    def create_dataset(self,root,transfms):
        return ImageFolder(root=root,transform=transfms )

    def __dataloader(self,is_train:bool):
        if is_train:
            ds = self.create_dataset(self.data_path.joinpath("train"),transfms=self.train_transform)

        else:
            ds = self.create_dataset(self.data_path.joinpath("validation"),transfms=self.test_transform)

        return DataLoader(dataset=ds,batch_size=self._bs, num_workers=self._num_workers,shuffle=True)
    
    def train_dataloader(self) -> TRAIN_DATALOADERS:
        return self.__dataloader(is_train=True)
    
    def val_dataloader(self) -> TRAIN_DATALOADERS:
        return self.__dataloader(is_train=False)
        