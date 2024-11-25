import torch

# Check if 'dml' device type is available
if torch.backends.mps.is_available():
    print("DirectML backend is available!")
    device = torch.device('dml')
else:
    print("DirectML backend is NOT available.")
    device = torch.device('cpu')

# Run a tensor operation on the detected device
a = torch.tensor([1.0, 2.0, 3.0], device=device)
b = torch.tensor([4.0, 5.0, 6.0], device=device)
result = a + b

print(f"Result: {result}")
print(f"Tensor is on device: {result.device}")
