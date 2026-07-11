import tensorrt as trt
import torch
import numpy as np
import os

class TensorRTOptimizer:
    def __init__(self, model, input_shape, engine_file_path="model_trt.engine"):
        """
        Initialize the TensorRT optimizer.

        Args:
            model: PyTorch model to be optimized.
            input_shape: The input shape for the model (e.g., (1, 3, 224, 224)).
            engine_file_path: Path to save or load the TensorRT engine.
        """
        self.model = model.eval().cuda()
        self.input_shape = input_shape
        self.engine_file_path = engine_file_path
        self.logger = trt.Logger(trt.Logger.WARNING)

    def build_engine(self):
        """
        Build a TensorRT engine from the PyTorch model.
        """
        if os.path.exists(self.engine_file_path):
            print(f"Loading existing TensorRT engine from {self.engine_file_path}")
            with open(self.engine_file_path, "rb") as f:
                runtime = trt.Runtime(self.logger)
                return runtime.deserialize_cuda_engine(f.read())

        print("Building TensorRT engine...")
        with torch.no_grad():
            input_data = torch.randn(*self.input_shape).cuda()
            traced_model = torch.jit.trace(self.model, input_data)

        with trt.Builder(self.logger) as builder, builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)) as network, trt.OnnxParser(network, self.logger) as parser:
            builder.max_workspace_size = 1 << 30  # 1GB
            builder.max_batch_size = self.input_shape[0]

            onnx_path = "model.onnx"
            torch.onnx.export(traced_model, input_data, onnx_path, export_params=True, opset_version=11, do_constant_folding=True, input_names=['input'], output_names=['output'])

            with open(onnx_path, "rb") as model:
                parser.parse(model.read())

            engine = builder.build_cuda_engine(network)
            if engine is None:
                raise RuntimeError("Failed to build TensorRT engine")

            with open(self.engine_file_path, "wb") as f:
                f.write(engine.serialize())

            return engine

    def infer(self, input_tensor):
        """
        Perform inference using the TensorRT engine.

        Args:
            input_tensor: Input tensor for inference.

        Returns:
            Output tensor from the model.
        """
        engine = self.build_engine()
        context = engine.create_execution_context()

        # Allocate buffers
        input_shape = tuple(input_tensor.size())
        input_size = trt.volume(input_shape) * input_tensor.element_size()
        output_shape = (self.input_shape[0], engine.get_binding_shape(1)[1])
        output_size = trt.volume(output_shape) * input_tensor.element_size()

        d_input = torch.cuda.mem_alloc(input_size)
        d_output = torch.cuda.mem_alloc(output_size)

        bindings = [int(d_input), int(d_output)]

        # Transfer input data to the GPU
        torch.cuda.memcpy_htod(d_input, input_tensor.cpu().numpy())

        # Run inference
        context.execute_v2(bindings)

        # Transfer predictions back
        output = torch.empty(output_shape, dtype=torch.float32, device='cuda')
        torch.cuda.memcpy_dtoh(output, d_output)

        return output

# Example usage
if __name__ == "__main__":
    from transformers import GPT2LMHeadModel

    # Load a small GPT-2 model for demonstration purposes
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    # Define input shape (batch_size=1, sequence_length=10)
    input_shape = (1, 10)

    # Initialize TensorRT optimizer
    optimizer = TensorRTOptimizer(model, input_shape)

    # Create a dummy input tensor
    input_tensor = torch.randint(0, 50256, input_shape).cuda()

    # Perform inference
    output = optimizer.infer(input_tensor)
    print("Inference output:", output)