import torch 
import glob
import os 
import yaml 
from datum import DogsDATAClassifier
from models import DogsClassifier
import lightning as pl 
from sklearn.metrics import confusion_matrix
import seaborn as sns 
from matplotlib import pyplot as plt
with open( os.path.join(os.getcwd(),'config','configs.yaml') ) as f:
    config = yaml.safe_load(f)

dm = DogsDATAClassifier(
                dl_path= config['DATA'].get('PATH',None),
                num_workers=config['DATA'].get('num_workers',None),
                batch_size=config['DATA'].get('batch_size',None),
)



checkpoints = sorted(glob.glob(os.path.join(os.getcwd(),'logs','chkpoints',"*.ckpt")),key=os.path.getctime)

assert len(checkpoints)>0, "train before eval!!"
resnet = DogsClassifier.load_from_checkpoint(checkpoints[0])


trainer  = pl.Trainer(
                max_epochs=config['Training'].get('num_epochs',15),
                accelerator="auto",
             )


trainer.validate(resnet,dm)

imgs,classes = next(iter(dm.val_dataloader()))
preds = resnet(imgs[:10,...])

ax = sns.heatmap(confusion_matrix(
     classes[:10].detach().numpy(),
     torch.softmax(preds,dim=-1).argmax(dim=-1).detach().numpy()
),cmap='autumn',annot=True,cbar=False)
plt.title("Random 10 images")

plt.show()