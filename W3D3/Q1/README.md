# LLM Inference Calculator

A comprehensive tool for estimating Large Language Model (LLM) inference costs, latency, memory usage, and performance across different models, hardware configurations, and deployment scenarios.

## 🚀 Features

### Core Functionality
- **Model Support**: 7+ popular LLM models (Llama 2, GPT-4, Claude, Mistral, etc.)
- **Hardware Analysis**: 6+ hardware types (CPU, V100, A100, H100, TPU)
- **Deployment Modes**: Local, Cloud, Edge, and Hybrid deployments
- **Comprehensive Metrics**: Latency, memory usage, cost, throughput, and compatibility
- **Scenario Analysis**: Pre-built analysis for common use cases

### Supported Models
1. **Llama 2 7B** - Efficient open-source model
2. **Llama 2 13B** - Balanced performance and capability
3. **GPT-4** - State-of-the-art quality (cloud only)
4. **GPT-3.5 Turbo** - Cost-effective cloud model
5. **Claude 3 Sonnet** - Long-context reasoning
6. **Mistral 7B** - Efficient long-context model
7. **Cohere Command** - Business-focused model

### Supported Hardware
1. **CPU** - General-purpose computing
2. **NVIDIA V100 (32GB)** - Previous generation GPU
3. **NVIDIA A100 (40GB)** - Current generation GPU
4. **NVIDIA A100 (80GB)** - High-memory GPU
5. **NVIDIA H100 (80GB)** - Latest generation GPU
6. **Google TPU v4** - Specialized AI accelerator

## 📁 Project Structure

```
W3D3/Q1/
├── inference_calculator.py    # Main calculator implementation
├── research_notes.md          # Comprehensive LLM inference research
├── scenario_analysis.md       # Real-world use case analysis
├── README.md                  # This file
└── examples/                  # Example usage scripts
    ├── basic_usage.py
    ├── scenario_comparison.py
    └── cost_analysis.py
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (pure Python)

### Quick Start

1. **Navigate to the project directory**
   ```bash
   cd W3D3/Q1
   ```

2. **Run the calculator**
   ```bash
   python3 inference_calculator.py
   ```

3. **Use in your own code**
   ```python
   from inference_calculator import LLMInferenceCalculator, InferenceRequest, ModelType, HardwareType, DeploymentMode
   
   calculator = LLMInferenceCalculator()
   ```

## 🎯 Usage Examples

### Basic Usage

```python
from inference_calculator import (
    LLMInferenceCalculator, 
    InferenceRequest, 
    ModelType, 
    HardwareType, 
    DeploymentMode
)

# Initialize calculator
calculator = LLMInferenceCalculator()

# Create inference request
request = InferenceRequest(
    model_type=ModelType.LLAMA_7B,
    input_tokens=100,
    output_tokens=50,
    batch_size=1,
    hardware_type=HardwareType.GPU_A100_40GB,
    deployment_mode=DeploymentMode.CLOUD
)

# Calculate inference metrics
result = calculator.calculate_inference(request)

# Print results
print(f"Latency: {result.latency_ms:.2f} ms")
print(f"Memory Usage: {result.memory_usage_gb:.2f} GB")
print(f"Cost per Request: ${result.cost_per_request:.6f}")
print(f"Throughput: {result.throughput_tokens_per_sec:.2f} tokens/sec")
print(f"Hardware Compatibility: {result.hardware_compatibility}")
```

### Scenario Comparison

```python
# Compare multiple scenarios
scenarios = [
    InferenceRequest(
        model_type=ModelType.LLAMA_7B,
        input_tokens=100,
        output_tokens=50,
        batch_size=1,
        hardware_type=HardwareType.GPU_A100_40GB,
        deployment_mode=DeploymentMode.LOCAL
    ),
    InferenceRequest(
        model_type=ModelType.GPT_4,
        input_tokens=100,
        output_tokens=50,
        batch_size=1,
        hardware_type=HardwareType.GPU_H100,
        deployment_mode=DeploymentMode.CLOUD
    )
]

results = calculator.compare_scenarios(scenarios)
print(json.dumps(results, indent=2))
```

### Cost Analysis

```python
# Analyze costs for different deployment strategies
models = [ModelType.LLAMA_7B, ModelType.LLAMA_13B, ModelType.GPT_4]
hardware = [HardwareType.CPU, HardwareType.GPU_A100_40GB, HardwareType.GPU_H100]

for model in models:
    for hw in hardware:
        request = InferenceRequest(
            model_type=model,
            input_tokens=500,
            output_tokens=200,
            batch_size=1,
            hardware_type=hw,
            deployment_mode=DeploymentMode.LOCAL
        )
        result = calculator.calculate_inference(request)
        print(f"{model.value} on {hw.value}: ${result.cost_per_request:.6f}")
```

## 📊 Key Metrics Explained

### 1. Latency (ms)
**Definition**: Time from input to first token output
- **Interactive**: <100ms (real-time chat)
- **Standard**: <1000ms (web applications)
- **Batch**: <10000ms (content generation)

### 2. Memory Usage (GB)
**Definition**: Peak memory consumption during inference
- **Components**: Model weights + activations + KV cache + system overhead
- **Scaling**: Linear with model size and sequence length

### 3. Cost per Request (USD)
**Definition**: Total cost divided by tokens generated
- **Local**: Electricity + hardware depreciation
- **Cloud**: Token cost + infrastructure cost
- **Factors**: Model size, hardware, deployment mode

### 4. Throughput (tokens/sec)
**Definition**: Tokens generated per second
- **Factors**: Hardware compute, memory bandwidth, model efficiency
- **Optimization**: Batching, quantization, parallelization

### 5. Hardware Compatibility
**Definition**: Whether hardware can run the model
- **✅ Compatible**: Sufficient memory and compute
- **⚠️ Marginal**: Close to limits
- **❌ Incompatible**: Insufficient resources

## 🔧 Advanced Features

### Quantization Support
```python
request = InferenceRequest(
    model_type=ModelType.LLAMA_7B,
    input_tokens=100,
    output_tokens=50,
    batch_size=1,
    hardware_type=HardwareType.GPU_A100_40GB,
    deployment_mode=DeploymentMode.LOCAL,
    precision="fp16",  # or "fp32", "int8"
    use_quantization=True
)
```

### Batch Processing
```python
# Analyze batch size impact
for batch_size in [1, 4, 8, 16]:
    request = InferenceRequest(
        model_type=ModelType.LLAMA_7B,
        input_tokens=100,
        output_tokens=50,
        batch_size=batch_size,
        hardware_type=HardwareType.GPU_A100_40GB,
        deployment_mode=DeploymentMode.LOCAL
    )
    result = calculator.calculate_inference(request)
    print(f"Batch {batch_size}: {result.throughput_tokens_per_sec:.2f} tokens/sec")
```

### Model Information
```python
# Get detailed model specifications
model_info = calculator.get_model_info(ModelType.LLAMA_7B)
print(f"Parameters: {model_info['parameters_billions']}B")
print(f"Context Length: {model_info['context_length']}")
print(f"Memory per Token: {model_info['memory_per_token_mb']}MB")
```

### Hardware Information
```python
# Get detailed hardware specifications
hw_info = calculator.get_hardware_info(HardwareType.GPU_A100_40GB)
print(f"Memory: {hw_info['memory_gb']}GB")
print(f"Compute: {hw_info['compute_tflops']} TFLOPS")
print(f"Cost per Hour: ${hw_info['cloud_cost_per_hour']}")
```

## 📈 Real-World Scenarios

### Scenario 1: Chatbot Application
- **Model**: GPT-3.5 Turbo (Cloud)
- **Latency**: 800ms
- **Cost**: $0.0003 per request
- **Best for**: Customer service, interactive applications

### Scenario 2: Content Generation
- **Model**: Hybrid (GPT-4 + Llama 13B)
- **Latency**: 3000-8000ms
- **Cost**: $0.0002-$0.045 per request
- **Best for**: Articles, marketing copy, bulk generation

### Scenario 3: Research Assistant
- **Model**: Claude 3 Sonnet (Cloud)
- **Latency**: 25000ms
- **Cost**: $0.1125 per request
- **Best for**: Document analysis, long-context reasoning

## 🎨 Customization

### Adding New Models
```python
# Extend the ModelType enum
class ModelType(Enum):
    CUSTOM_MODEL = "custom-model"

# Add model specifications
models[ModelType.CUSTOM_MODEL] = ModelSpecs(
    name="Custom Model",
    parameters=10,  # billions
    context_length=4096,
    precision="fp16",
    memory_per_token=0.002,  # MB per token
    flops_per_token=20_000_000_000,  # FLOPs per token
    cloud_cost_per_1k_tokens=0.001,  # USD per 1K tokens
    local_memory_requirement=20.0  # GB
)
```

### Adding New Hardware
```python
# Extend the HardwareType enum
class HardwareType(Enum):
    CUSTOM_GPU = "custom-gpu"

# Add hardware specifications
hardware[HardwareType.CUSTOM_GPU] = HardwareSpecs(
    name="Custom GPU",
    memory_gb=48.0,
    memory_bandwidth_gbps=1000.0,
    compute_tflops=200.0,
    power_watts=350.0,
    cost_per_hour=2.50,
    local_cost=8000.0
)
```

## 🔍 Research and Analysis

### Research Notes (`research_notes.md`)
Comprehensive documentation covering:
- LLM inference fundamentals
- Model architecture details
- Hardware considerations
- Deployment strategies
- Cost analysis
- Performance metrics
- Optimization techniques

### Scenario Analysis (`scenario_analysis.md`)
Detailed analysis of three real-world use cases:
1. **Chatbot Application**: Customer service automation
2. **Content Generation Service**: Marketing and content creation
3. **Research Assistant**: Academic and business research

Each scenario includes:
- Performance requirements
- Model options analysis
- Cost comparisons
- Specific recommendations
- Implementation plans

## 🚀 Performance Optimization

### 1. Model Selection
- **Small models (7B)**: Fast, cost-effective, good for simple tasks
- **Medium models (13B)**: Balanced performance and capability
- **Large models (70B+)**: Highest quality, expensive, complex deployment

### 2. Hardware Optimization
- **GPU selection**: Match model size to GPU memory
- **Memory bandwidth**: Critical for large models
- **Compute capacity**: Affects latency and throughput

### 3. Deployment Optimization
- **Local**: Best for high-volume, cost-sensitive applications
- **Cloud**: Best for variable load, managed infrastructure
- **Hybrid**: Best for balanced requirements

### 4. Inference Optimization
- **Batching**: Improve throughput with multiple requests
- **Quantization**: Reduce memory usage and improve speed
- **Caching**: Cache common responses
- **Streaming**: Reduce perceived latency

## 📊 Cost Analysis

### Cost Components
1. **Hardware Costs**: GPU/CPU purchase or cloud rental
2. **Operational Costs**: Electricity, cooling, maintenance
3. **Token Costs**: Model-specific pricing for cloud APIs
4. **Infrastructure Costs**: Load balancers, monitoring, etc.

### Cost Optimization Strategies
1. **Model Selection**: Use smaller models for simple tasks
2. **Deployment Strategy**: Local for high volume, cloud for variable load
3. **Batching**: Process multiple requests together
4. **Caching**: Cache common responses
5. **Quantization**: Use lower precision for faster inference

## 🔧 Troubleshooting

### Common Issues

**Memory Errors**
```python
# Check hardware compatibility
result = calculator.calculate_inference(request)
if "Incompatible" in result.hardware_compatibility:
    print("Consider using quantization or smaller model")
```

**High Latency**
```python
# Analyze latency components
# - Model size affects compute time
# - Hardware affects memory bandwidth
# - Network affects cloud latency
# - Batch size affects parallelization
```

**High Costs**
```python
# Cost optimization strategies
# - Use local deployment for high volume
# - Implement caching
# - Use smaller models
# - Optimize batch sizes
```

## 📈 Future Enhancements

### Planned Features
- **Machine Learning Integration**: Use ML for better predictions
- **Real-time Monitoring**: Live performance tracking
- **Automated Optimization**: AI-driven configuration recommendations
- **More Models**: Support for additional LLM architectures
- **Advanced Metrics**: More detailed performance analysis

### Extension Points
- **Custom Models**: Easy addition of new model types
- **Custom Hardware**: Support for new hardware configurations
- **Custom Metrics**: User-defined performance metrics
- **API Integration**: REST API for web applications

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test thoroughly
5. Submit a pull request

### Development Guidelines
- Follow Python PEP 8 style guidelines
- Add comprehensive docstrings
- Include unit tests for new features
- Update documentation for changes

## 📄 License

This project is part of the Misogi course materials.

## 🙏 Acknowledgments

- Built for educational and research purposes
- Inspired by the need for better LLM deployment planning
- Uses real-world hardware and model specifications
- Based on current industry best practices

## 📚 References

1. "Attention Is All You Need" - Vaswani et al. (2017)
2. "LLaMA: Open and Efficient Foundation Language Models" - Touvron et al. (2023)
3. "GPT-4 Technical Report" - OpenAI (2023)
4. "Claude 3 Technical Report" - Anthropic (2024)
5. "Efficient Memory Management for Large Language Model Serving" - Kwon et al. (2023)

---

**Happy LLM Inference Planning! 🚀** 