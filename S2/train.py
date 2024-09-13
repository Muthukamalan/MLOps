import os
import torch
import torch.nn.functional as F
import torch.optim as optim
import argparse
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR

# class Net(torch.nn.Module):
#     def __init__(self):
#         super(Net, self).__init__()
#         # TODO: Define your model architecture here

#     def forward(self, x):
#         # TODO: Define the forward pass
#         pass


class Net(torch.nn.Module):
    #This defines the structure of the NN.
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = torch.nn.Conv2d(1, 32, kernel_size=3)
        self.conv2 = torch.nn.Conv2d(32, 64, kernel_size=3)
        self.conv3 = torch.nn.Conv2d(64, 128, kernel_size=3)
        self.conv4 = torch.nn.Conv2d(128, 256, kernel_size=3)
        self.fc1 = torch.nn.Linear(4096, 50)
        self.fc2 = torch.nn.Linear(50, 10)

    def forward(self, x):
        x = torch.nn.functional.relu(self.conv1(x))                  # 28>26    | 1>3     | 1>1 
        x = torch.nn.functional.relu(torch.nn.functional.max_pool2d(self.conv2(x),2))  # 26>24>12 | 3>5>6   | 1>1>2
        x = torch.nn.functional.relu(self.conv3(x))                  # 12>10    | 6>10    | 2>2
        x = torch.nn.functional.relu(torch.nn.functional.max_pool2d(self.conv4(x),2))  # 10>8>4   | 10>14>16| 2>2>4
        x = x.view(-1, 4096)
        x = torch.nn.functional.relu(self.fc1(x))
        x = self.fc2(x)
        return torch.nn.functional.log_softmax(x, dim=1)
    



def train_epoch(epoch, args, model, device, data_loader, optimizer):
    model.train()
    for batch_idx, (data, target) in enumerate(data_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % args.log_interval == 0:
            print(f'Train Epoch: {epoch} [{batch_idx * len(data)}/{len(data_loader.dataset)} ({100. * batch_idx / len(data_loader):.0f}%)]\tLoss: {loss.item():.6f}')
            if args.dry_run:
                break

def test_epoch(model, device, data_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in data_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(data_loader.dataset)

    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format( test_loss, correct, len(data_loader.dataset),100. * correct / len(data_loader.dataset)))

def main():
    # Parser to get command line arguments
    parser = argparse.ArgumentParser(description='MNIST Training Script')
    # TODO: Define your command line arguments here
    parser.add_argument('--batch-size', type=int, default=64, metavar='N',
                        help='input batch size for training (default: 64)')
    parser.add_argument('--test-batch-size', type=int, default=1000, metavar='N',
                        help='input batch size for testing (default: 1000)')
    parser.add_argument('--epochs', type=int, default=1, metavar='N',
                        help='number of epochs to train (default: 14)')
    parser.add_argument('--lr', type=float, default=1.0, metavar='LR',
                        help='learning rate (default: 1.0)')
    parser.add_argument('--gamma', type=float, default=0.7, metavar='M',
                        help='Learning rate step gamma (default: 0.7)')
    parser.add_argument('--no-cuda', action='store_true', default=False,
                        help='disables CUDA training')
    parser.add_argument('--no-mps', action='store_true', default=False,
                        help='disables macOS GPU training')
    parser.add_argument('--dry-run', action='store_true', default=False,
                        help='quickly check a single pass')
    parser.add_argument('--seed', type=int, default=1, metavar='S',
                        help='random seed (default: 1)')
    parser.add_argument('--log-interval', type=int, default=10, metavar='N',
                        help='how many batches to wait before logging training status')
    parser.add_argument('--save-model', action='store_true', default=True,
                        help='For Saving the current Model')
    parser.add_argument('--resume', action='store_true', default=False,
                        help='load from checkpoint')
    
    args = parser.parse_args()
    use_cuda = torch.cuda.is_available()
    torch.manual_seed(args.seed)
    device = torch.device("cuda" if use_cuda else "cpu")

    # TODO: Load the MNIST dataset for training and testing
    transform=transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.1307,), (0.3081,))])
    dataset1 = datasets.MNIST('./data', train=True, download=True,transform=transform)
    dataset2 = datasets.MNIST('./data', train=False,transform=transform)


    train_kwargs = {'batch_size': args.batch_size}
    test_kwargs = {'batch_size': args.test_batch_size}
    train_loader = torch.utils.data.DataLoader(dataset1,**train_kwargs)
    test_loader = torch.utils.data.DataLoader(dataset2, **test_kwargs)
    
    # TODO: Add a way to load the model checkpoint if 'resume' argument is True
    model = Net().to(device)

    if args.resume and os.path.isfile(os.path.join(os.path.dirname(__file__),'model_checkpoint.pth')):
        checkpoint = torch.load( os.path.join(os.path.dirname(__file__),'model_checkpoint.pth') )
        model.load_state_dict(checkpoint)
    # TODO: Choose and define the optimizer here
    optimizer = optim.Adadelta(model.parameters(), lr=args.lr)
    scheduler = StepLR(optimizer, step_size=1, gamma=args.gamma)

    
    # TODO: Implement the training and testing cycles
    # Hint: Save the model after each epoch
    for epoch in range(1, args.epochs + 1):
        train_epoch(epoch=epoch, args=args, model=model, device=device, data_loader=train_loader, optimizer=optimizer)
        # train_epoch(args, model, device, optimizer, epoch,data_loader=train_loader)
        test_epoch(model, device, test_loader)
        scheduler.step()

    if args.save_model:
        torch.save(model.state_dict(), "model_checkpoint.pth")

if __name__ == "__main__":
    main()