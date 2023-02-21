## Provider's Example

# Configure the AWS Provider
provider "aws" {
    version = "4.55.0"
    profile = "default"
    region     = "us-east-2"
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
    version = "2.72.0"
    features {}
}