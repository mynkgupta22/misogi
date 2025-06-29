#!/usr/bin/env python3
"""
LLM Inference Calculator

A comprehensive tool for estimating LLM inference costs, latency, and memory usage
across different models, hardware configurations, and deployment scenarios.
"""

import math
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class ModelType(Enum):
    """Supported LLM model types"""
    LLAMA_7B = "llama-7b"
    LLAMA_13B = "llama-13b"
    GPT_4 = "gpt-4"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    CLAUDE_3_SONNET = "claude-3-sonnet"
    MISTRAL_7B = "mistral-7b"
    COHERE_COMMAND = "cohere-command"

class HardwareType(Enum):
    """Supported hardware types"""
    CPU = "cpu"
    GPU_V100 = "gpu-v100"
    GPU_A100_40GB = "gpu-a100-40gb"
    GPU_A100_80GB = "gpu-a100-80gb"
    GPU_H100 = "gpu-h100"
    TPU_V4 = "tpu-v4"

class DeploymentMode(Enum):
    """Deployment modes"""
    LOCAL = "local"
    CLOUD = "cloud"
    EDGE = "edge"
    HYBRID = "hybrid"

@dataclass
class ModelSpecs:
    """Model specifications and characteristics"""
    name: str
    parameters: int  # in billions
    context_length: int
    precision: str  # fp16, fp32, int8, etc.
    memory_per_token: float  # MB per token
    flops_per_token: int  # FLOPs per token
    cloud_cost_per_1k_tokens: float  # USD per 1k tokens
    local_memory_requirement: float  # GB required for local deployment

@dataclass
class HardwareSpecs:
    """Hardware specifications"""
    name: str
    memory_gb: float
    memory_bandwidth_gbps: float
    compute_tflops: float
    power_watts: float
    cost_per_hour: float  # USD per hour for cloud deployment
    local_cost: float  # USD for local hardware

@dataclass
class InferenceRequest:
    """Input parameters for inference calculation"""
    model_type: ModelType
    input_tokens: int
    output_tokens: int
    batch_size: int
    hardware_type: HardwareType
    deployment_mode: DeploymentMode
    precision: str = "fp16"
    use_quantization: bool = False

@dataclass
class InferenceResult:
    """Results of inference calculation"""
    latency_ms: float
    memory_usage_gb: float
    cost_per_request: float
    throughput_tokens_per_sec: float
    hardware_compatibility: str
    recommendations: List[str]

class LLMInferenceCalculator:
    """Main calculator class for LLM inference estimates"""
    
    def __init__(self):
        """Initialize the calculator with model and hardware specifications"""
        self.models = self._initialize_models()
        self.hardware = self._initialize_hardware()
        self.deployment_configs = self._initialize_deployment_configs()
    
    def _initialize_models(self) -> Dict[ModelType, ModelSpecs]:
        """Initialize model specifications"""
        return {
            ModelType.LLAMA_7B: ModelSpecs(
                name="Llama 2 7B",
                parameters=7,
                context_length=4096,
                precision="fp16",
                memory_per_token=0.0014,  # ~1.4MB per token
                flops_per_token=14_000_000_000,  # 14B FLOPs per token
                cloud_cost_per_1k_tokens=0.0002,  # $0.0002 per 1k tokens
                local_memory_requirement=14.0  # 14GB for fp16
            ),
            ModelType.LLAMA_13B: ModelSpecs(
                name="Llama 2 13B",
                parameters=13,
                context_length=4096,
                precision="fp16",
                memory_per_token=0.0026,  # ~2.6MB per token
                flops_per_token=26_000_000_000,  # 26B FLOPs per token
                cloud_cost_per_1k_tokens=0.0004,  # $0.0004 per 1k tokens
                local_memory_requirement=26.0  # 26GB for fp16
            ),
            ModelType.GPT_4: ModelSpecs(
                name="GPT-4",
                parameters=175,  # Estimated
                context_length=8192,
                precision="fp16",
                memory_per_token=0.035,  # ~35MB per token
                flops_per_token=350_000_000_000,  # 350B FLOPs per token
                cloud_cost_per_1k_tokens=0.03,  # $0.03 per 1k tokens
                local_memory_requirement=350.0  # 350GB for fp16
            ),
            ModelType.GPT_3_5_TURBO: ModelSpecs(
                name="GPT-3.5 Turbo",
                parameters=6,  # Estimated
                context_length=4096,
                precision="fp16",
                memory_per_token=0.0012,  # ~1.2MB per token
                flops_per_token=12_000_000_000,  # 12B FLOPs per token
                cloud_cost_per_1k_tokens=0.002,  # $0.002 per 1k tokens
                local_memory_requirement=12.0  # 12GB for fp16
            ),
            ModelType.CLAUDE_3_SONNET: ModelSpecs(
                name="Claude 3 Sonnet",
                parameters=8,  # Estimated
                context_length=200000,
                precision="fp16",
                memory_per_token=0.0016,  # ~1.6MB per token
                flops_per_token=16_000_000_000,  # 16B FLOPs per token
                cloud_cost_per_1k_tokens=0.015,  # $0.015 per 1k tokens
                local_memory_requirement=16.0  # 16GB for fp16
            ),
            ModelType.MISTRAL_7B: ModelSpecs(
                name="Mistral 7B",
                parameters=7,
                context_length=8192,
                precision="fp16",
                memory_per_token=0.0014,  # ~1.4MB per token
                flops_per_token=14_000_000_000,  # 14B FLOPs per token
                cloud_cost_per_1k_tokens=0.0002,  # $0.0002 per 1k tokens
                local_memory_requirement=14.0  # 14GB for fp16
            ),
            ModelType.COHERE_COMMAND: ModelSpecs(
                name="Cohere Command",
                parameters=6,  # Estimated
                context_length=4096,
                precision="fp16",
                memory_per_token=0.0012,  # ~1.2MB per token
                flops_per_token=12_000_000_000,  # 12B FLOPs per token
                cloud_cost_per_1k_tokens=0.001,  # $0.001 per 1k tokens
                local_memory_requirement=12.0  # 12GB for fp16
            )
        }
    
    def _initialize_hardware(self) -> Dict[HardwareType, HardwareSpecs]:
        """Initialize hardware specifications"""
        return {
            HardwareType.CPU: HardwareSpecs(
                name="CPU (Intel i7-12700K)",
                memory_gb=32.0,
                memory_bandwidth_gbps=50.0,
                compute_tflops=0.5,  # CPU compute is much lower
                power_watts=125.0,
                cost_per_hour=0.05,  # Cloud CPU instance
                local_cost=400.0  # CPU cost
            ),
            HardwareType.GPU_V100: HardwareSpecs(
                name="NVIDIA V100 (32GB)",
                memory_gb=32.0,
                memory_bandwidth_gbps=900.0,
                compute_tflops=112.0,
                power_watts=300.0,
                cost_per_hour=2.48,  # AWS p3.2xlarge
                local_cost=8000.0  # V100 cost
            ),
            HardwareType.GPU_A100_40GB: HardwareSpecs(
                name="NVIDIA A100 (40GB)",
                memory_gb=40.0,
                memory_bandwidth_gbps=1555.0,
                compute_tflops=312.0,
                power_watts=400.0,
                cost_per_hour=3.26,  # AWS p4d.24xlarge
                local_cost=10000.0  # A100 cost
            ),
            HardwareType.GPU_A100_80GB: HardwareSpecs(
                name="NVIDIA A100 (80GB)",
                memory_gb=80.0,
                memory_bandwidth_gbps=2039.0,
                compute_tflops=312.0,
                power_watts=400.0,
                cost_per_hour=4.50,  # AWS p4d.24xlarge
                local_cost=15000.0  # A100 80GB cost
            ),
            HardwareType.GPU_H100: HardwareSpecs(
                name="NVIDIA H100 (80GB)",
                memory_gb=80.0,
                memory_bandwidth_gbps=3350.0,
                compute_tflops=989.0,
                power_watts=700.0,
                cost_per_hour=8.00,  # Estimated cloud cost
                local_cost=40000.0  # H100 cost
            ),
            HardwareType.TPU_V4: HardwareSpecs(
                name="Google TPU v4",
                memory_gb=32.0,
                memory_bandwidth_gbps=1200.0,
                compute_tflops=275.0,
                power_watts=200.0,
                cost_per_hour=2.00,  # Google Cloud TPU
                local_cost=0.0  # TPUs are cloud-only
            )
        }
    
    def _initialize_deployment_configs(self) -> Dict[DeploymentMode, Dict[str, Any]]:
        """Initialize deployment mode configurations"""
        return {
            DeploymentMode.LOCAL: {
                "overhead_factor": 1.1,  # 10% overhead for local deployment
                "network_latency_ms": 0.0,
                "infrastructure_cost_multiplier": 0.0,  # No cloud infrastructure
                "scalability_factor": 1.0
            },
            DeploymentMode.CLOUD: {
                "overhead_factor": 1.2,  # 20% overhead for cloud deployment
                "network_latency_ms": 50.0,  # Network latency
                "infrastructure_cost_multiplier": 0.1,  # 10% infrastructure overhead
                "scalability_factor": 10.0
            },
            DeploymentMode.EDGE: {
                "overhead_factor": 1.5,  # 50% overhead for edge deployment
                "network_latency_ms": 100.0,  # Higher network latency
                "infrastructure_cost_multiplier": 0.05,  # 5% infrastructure overhead
                "scalability_factor": 0.5
            },
            DeploymentMode.HYBRID: {
                "overhead_factor": 1.3,  # 30% overhead for hybrid deployment
                "network_latency_ms": 75.0,  # Medium network latency
                "infrastructure_cost_multiplier": 0.075,  # 7.5% infrastructure overhead
                "scalability_factor": 5.0
            }
        }
    
    def calculate_inference(self, request: InferenceRequest) -> InferenceResult:
        """Calculate inference metrics for the given request"""
        
        model = self.models[request.model_type]
        hardware = self.hardware[request.hardware_type]
        deployment = self.deployment_configs[request.deployment_mode]
        
        # Calculate memory usage
        memory_usage_gb = self._calculate_memory_usage(request, model, hardware)
        
        # Calculate latency
        latency_ms = self._calculate_latency(request, model, hardware, deployment)
        
        # Calculate cost
        cost_per_request = self._calculate_cost(request, model, hardware, deployment)
        
        # Calculate throughput
        throughput_tokens_per_sec = self._calculate_throughput(request, model, hardware)
        
        # Check hardware compatibility
        hardware_compatibility = self._check_hardware_compatibility(request, model, hardware)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(request, model, hardware, deployment)
        
        return InferenceResult(
            latency_ms=latency_ms,
            memory_usage_gb=memory_usage_gb,
            cost_per_request=cost_per_request,
            throughput_tokens_per_sec=throughput_tokens_per_sec,
            hardware_compatibility=hardware_compatibility,
            recommendations=recommendations
        )
    
    def _calculate_memory_usage(self, request: InferenceRequest, model: ModelSpecs, hardware: HardwareSpecs) -> float:
        """Calculate memory usage in GB"""
        # Base model memory
        model_memory = model.local_memory_requirement
        
        # Memory for input/output tokens
        total_tokens = request.input_tokens + request.output_tokens
        token_memory = total_tokens * model.memory_per_token / 1024  # Convert MB to GB
        
        # Batch size multiplier
        batch_memory = token_memory * request.batch_size
        
        # Quantization effect
        if request.use_quantization:
            model_memory *= 0.5  # 50% reduction with quantization
            batch_memory *= 0.5
        
        # Precision effect
        if request.precision == "fp32":
            model_memory *= 2.0
            batch_memory *= 2.0
        elif request.precision == "int8":
            model_memory *= 0.25
            batch_memory *= 0.25
        
        total_memory = model_memory + batch_memory
        
        # Add 20% buffer for system overhead
        return total_memory * 1.2
    
    def _calculate_latency(self, request: InferenceRequest, model: ModelSpecs, hardware: HardwareSpecs, deployment: Dict[str, Any]) -> float:
        """Calculate inference latency in milliseconds"""
        
        total_tokens = request.input_tokens + request.output_tokens
        
        # Compute-bound latency (FLOPs / compute capacity)
        compute_latency_ms = (model.flops_per_token * total_tokens) / (hardware.compute_tflops * 1e12) * 1000
        
        # Memory-bound latency (memory access time)
        memory_required_gb = total_tokens * model.memory_per_token / 1024
        memory_latency_ms = (memory_required_gb * 8) / hardware.memory_bandwidth_gbps * 1000
        
        # Take the maximum of compute and memory latency
        base_latency_ms = max(compute_latency_ms, memory_latency_ms)
        
        # Apply batch size effect (some parallelization)
        if request.batch_size > 1:
            base_latency_ms *= (0.7 + 0.3 / request.batch_size)  # Diminishing returns
        
        # Apply deployment overhead
        base_latency_ms *= deployment["overhead_factor"]
        
        # Add network latency for cloud/edge deployments
        base_latency_ms += deployment["network_latency_ms"]
        
        # Quantization effect
        if request.use_quantization:
            base_latency_ms *= 0.7  # 30% speedup with quantization
        
        return base_latency_ms
    
    def _calculate_cost(self, request: InferenceRequest, model: ModelSpecs, hardware: HardwareSpecs, deployment: Dict[str, Any]) -> float:
        """Calculate cost per request in USD"""
        
        total_tokens = request.input_tokens + request.output_tokens
        
        if request.deployment_mode == DeploymentMode.LOCAL:
            # Local deployment: only electricity cost
            latency_hours = self._calculate_latency(request, model, hardware, deployment) / (1000 * 3600)  # Convert ms to hours
            power_cost_per_hour = (hardware.power_watts * 0.00012)  # $0.12 per kWh
            return latency_hours * power_cost_per_hour
        else:
            # Cloud deployment: token cost + infrastructure cost
            token_cost = (total_tokens / 1000) * model.cloud_cost_per_1k_tokens
            
            # Infrastructure cost (time-based)
            latency_hours = self._calculate_latency(request, model, hardware, deployment) / (1000 * 3600)
            infrastructure_cost = latency_hours * hardware.cost_per_hour * deployment["infrastructure_cost_multiplier"]
            
            return token_cost + infrastructure_cost
    
    def _calculate_throughput(self, request: InferenceRequest, model: ModelSpecs, hardware: HardwareSpecs) -> float:
        """Calculate throughput in tokens per second"""
        latency_sec = self._calculate_latency(request, model, hardware, {"overhead_factor": 1.0, "network_latency_ms": 0.0}) / 1000
        total_tokens = request.input_tokens + request.output_tokens
        
        if latency_sec > 0:
            return total_tokens / latency_sec
        return 0.0
    
    def _check_hardware_compatibility(self, request: InferenceRequest, model: ModelSpecs, hardware: HardwareSpecs) -> str:
        """Check if the hardware can run the model"""
        required_memory = self._calculate_memory_usage(request, model, hardware)
        
        if required_memory <= hardware.memory_gb:
            return "✅ Compatible"
        elif required_memory <= hardware.memory_gb * 1.5:
            return "⚠️ Marginal (close to memory limit)"
        else:
            return "❌ Incompatible (insufficient memory)"
    
    def _generate_recommendations(self, request: InferenceRequest, model: ModelSpecs, hardware: HardwareSpecs, deployment: Dict[str, Any]) -> List[str]:
        """Generate recommendations for optimization"""
        recommendations = []
        
        # Memory recommendations
        required_memory = self._calculate_memory_usage(request, model, hardware)
        if required_memory > hardware.memory_gb:
            recommendations.append(f"Consider using quantization to reduce memory usage from {required_memory:.1f}GB to {required_memory * 0.5:.1f}GB")
        
        # Cost recommendations
        if request.deployment_mode == DeploymentMode.CLOUD and request.batch_size == 1:
            recommendations.append("Increase batch size to reduce per-request infrastructure costs")
        
        # Performance recommendations
        if request.input_tokens > model.context_length * 0.8:
            recommendations.append(f"Input tokens ({request.input_tokens}) are close to context limit ({model.context_length})")
        
        # Hardware recommendations
        if hardware.compute_tflops < 100 and model.parameters > 10:
            recommendations.append("Consider using a more powerful GPU for better performance with large models")
        
        # Deployment recommendations
        if request.deployment_mode == DeploymentMode.LOCAL and model.parameters > 20:
            recommendations.append("Large models may be more cost-effective in the cloud due to hardware requirements")
        
        return recommendations
    
    def compare_scenarios(self, scenarios: List[InferenceRequest]) -> Dict[str, Any]:
        """Compare multiple inference scenarios"""
        results = {}
        
        for i, scenario in enumerate(scenarios):
            result = self.calculate_inference(scenario)
            results[f"scenario_{i+1}"] = {
                "request": {
                    "model": scenario.model_type.value,
                    "input_tokens": scenario.input_tokens,
                    "output_tokens": scenario.output_tokens,
                    "batch_size": scenario.batch_size,
                    "hardware": scenario.hardware_type.value,
                    "deployment": scenario.deployment_mode.value
                },
                "results": {
                    "latency_ms": result.latency_ms,
                    "memory_usage_gb": result.memory_usage_gb,
                    "cost_per_request": result.cost_per_request,
                    "throughput_tokens_per_sec": result.throughput_tokens_per_sec,
                    "hardware_compatibility": result.hardware_compatibility
                },
                "recommendations": result.recommendations
            }
        
        return results
    
    def get_model_info(self, model_type: ModelType) -> Dict[str, Any]:
        """Get detailed information about a model"""
        model = self.models[model_type]
        return {
            "name": model.name,
            "parameters_billions": model.parameters,
            "context_length": model.context_length,
            "memory_per_token_mb": model.memory_per_token,
            "flops_per_token": model.flops_per_token,
            "cloud_cost_per_1k_tokens": model.cloud_cost_per_1k_tokens,
            "local_memory_requirement_gb": model.local_memory_requirement
        }
    
    def get_hardware_info(self, hardware_type: HardwareType) -> Dict[str, Any]:
        """Get detailed information about hardware"""
        hardware = self.hardware[hardware_type]
        return {
            "name": hardware.name,
            "memory_gb": hardware.memory_gb,
            "memory_bandwidth_gbps": hardware.memory_bandwidth_gbps,
            "compute_tflops": hardware.compute_tflops,
            "power_watts": hardware.power_watts,
            "cloud_cost_per_hour": hardware.cost_per_hour,
            "local_cost": hardware.local_cost
        }

def main():
    """Main function for command-line usage"""
    calculator = LLMInferenceCalculator()
    
    # Example usage
    print("🚀 LLM Inference Calculator")
    print("=" * 50)
    
    # Example 1: Llama 7B on A100
    request1 = InferenceRequest(
        model_type=ModelType.LLAMA_7B,
        input_tokens=100,
        output_tokens=50,
        batch_size=1,
        hardware_type=HardwareType.GPU_A100_40GB,
        deployment_mode=DeploymentMode.CLOUD
    )
    
    result1 = calculator.calculate_inference(request1)
    
    print(f"\n📊 Example 1: {request1.model_type.value} on {request1.hardware_type.value}")
    print(f"Latency: {result1.latency_ms:.2f} ms")
    print(f"Memory Usage: {result1.memory_usage_gb:.2f} GB")
    print(f"Cost per Request: ${result1.cost_per_request:.6f}")
    print(f"Throughput: {result1.throughput_tokens_per_sec:.2f} tokens/sec")
    print(f"Hardware Compatibility: {result1.hardware_compatibility}")
    
    # Example 2: GPT-4 on cloud
    request2 = InferenceRequest(
        model_type=ModelType.GPT_4,
        input_tokens=500,
        output_tokens=200,
        batch_size=1,
        hardware_type=HardwareType.GPU_H100,
        deployment_mode=DeploymentMode.CLOUD
    )
    
    result2 = calculator.calculate_inference(request2)
    
    print(f"\n📊 Example 2: {request2.model_type.value} on {request2.hardware_type.value}")
    print(f"Latency: {result2.latency_ms:.2f} ms")
    print(f"Memory Usage: {result2.memory_usage_gb:.2f} GB")
    print(f"Cost per Request: ${result2.cost_per_request:.6f}")
    print(f"Throughput: {result2.throughput_tokens_per_sec:.2f} tokens/sec")
    print(f"Hardware Compatibility: {result2.hardware_compatibility}")

if __name__ == "__main__":
    main() 