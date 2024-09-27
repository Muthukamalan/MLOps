from torchvision.utils import make_grid
import torch 
# from IPython import display
# from IPython.display import Image


# Visualization: Dataset sample
def show_batch(dataloader, num_images=16):
    from matplotlib import pyplot as plt 
    batch = next(iter(dataloader))
    images, labels = batch
    grid = make_grid(images[:num_images])
    plt.figure(figsize=(10, 5))
    plt.imshow(grid.permute(1, 2, 0))
    plt.axis('off')
    plt.title('Sample batch from the dataset')
    plt.show()


#  Visualization: Model Architecture
def visualize_model(model):
    from torchviz import make_dot
    x = torch.randn(1, 3, 224, 224)
    y = model(x)
    dot = make_dot(y, params=dict(model.named_parameters()))
    dot.render("model_architecture", format="png")
    # display(Image("model_architecture.png"))