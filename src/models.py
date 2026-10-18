"""Small shared model definitions for the CIFAR-10 project."""

from torch import nn
from torchvision.models import resnet18


def resnet18_cifar(num_classes: int = 10) -> nn.Module:
    """Create a ResNet-18 with a CIFAR-appropriate 32x32 image stem."""
    model = resnet18(weights=None)
    model.conv1 = nn.Conv2d(
        in_channels=3,
        out_channels=64,
        kernel_size=3,
        stride=1,
        padding=1,
        bias=False,
    )
    model.maxpool = nn.Identity()
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    return model
