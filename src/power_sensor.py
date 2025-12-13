"""Power Sensor Abstraction Layer for Firmus AI Infrastructure

Provides hardware-agnostic interface for power monitoring across different GPU
architectures and power measurement devices. Supports NVIDIA (H200, B200, 
Grace-Hopper), AMD, and future hardware platforms.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class PowerSensor(ABC):
    """Abstract base class for power monitoring sensors."""
    
    @abstractmethod
    def get_power_watts(self) -> float:
        """Get current power consumption in watts.
        
        Returns:
            float: Current power draw in watts
            
        Raises:
            RuntimeError: If power reading fails
        """
        pass
    
    @abstractmethod
    def get_temperature(self) -> Optional[float]:
        """Get current device temperature in Celsius.
        
        Returns:
            Optional[float]: Temperature in Celsius, or None if unavailable
        """
        pass
    
    @abstractmethod
    def get_device_info(self) -> Dict[str, Any]:
        """Get device information.
        
        Returns:
            Dict with keys: name, type, max_power_watts, features
        """
        pass
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the sensor hardware."""
        pass
    
    @abstractmethod
    def shutdown(self) -> None:
        """Clean shutdown of sensor."""
        pass


class NvidiaPowerSensor(PowerSensor):
    """NVIDIA GPU power sensor using NVML.
    
    Supports H200, B200, Grace-Hopper, and other NVIDIA GPUs with NVML support.
    """
    
    def __init__(self, gpu_index: int = 0):
        """Initialize NVIDIA power sensor.
        
        Args:
            gpu_index: GPU device index (default: 0)
        """
        self.gpu_index = gpu_index
        self.handle = None
        self._initialized = False
    
    def initialize(self) -> None:
        """Initialize NVML and get device handle."""
        try:
            import pynvml
            pynvml.nvmlInit()
            self.handle = pynvml.nvmlDeviceGetHandleByIndex(self.gpu_index)
            self._initialized = True
            
            device_info = self.get_device_info()
            logger.info(f"Initialized NVIDIA power sensor: {device_info['name']}")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize NVIDIA sensor: {e}")
    
    def get_power_watts(self) -> float:
        """Get current GPU power consumption.
        
        Returns:
            float: Power consumption in watts
        """
        if not self._initialized:
            raise RuntimeError("Sensor not initialized. Call initialize() first.")
        
        try:
            import pynvml
            power_mw = pynvml.nvmlDeviceGetPowerUsage(self.handle)
            return power_mw / 1000.0
        except Exception as e:
            raise RuntimeError(f"Failed to read power: {e}")
    
    def get_temperature(self) -> Optional[float]:
        """Get GPU temperature.
        
        Returns:
            Optional[float]: Temperature in Celsius
        """
        if not self._initialized:
            return None
        
        try:
            import pynvml
            return float(pynvml.nvmlDeviceGetTemperature(
                self.handle, pynvml.NVML_TEMPERATURE_GPU
            ))
        except Exception as e:
            logger.warning(f"Failed to read temperature: {e}")
            return None
    
    def get_device_info(self) -> Dict[str, Any]:
        """Get NVIDIA GPU information.
        
        Returns:
            Dict with device details
        """
        if not self._initialized:
            raise RuntimeError("Sensor not initialized")
        
        try:
            import pynvml
            name = pynvml.nvmlDeviceGetName(self.handle)
            
            # Get power limit (max TDP)
            try:
                max_power_mw = pynvml.nvmlDeviceGetPowerManagementLimit(self.handle)
                max_power_w = max_power_mw / 1000.0
            except:
                max_power_w = None
            
            return {
                "name": name,
                "type": "NVIDIA_GPU",
                "index": self.gpu_index,
                "max_power_watts": max_power_w,
                "features": ["power", "temperature", "utilization"]
            }
        except Exception as e:
            raise RuntimeError(f"Failed to get device info: {e}")
    
    def shutdown(self) -> None:
        """Shutdown NVML."""
        if self._initialized:
            try:
                import pynvml
                pynvml.nvmlShutdown()
                self._initialized = False
                logger.debug("NVIDIA sensor shutdown complete")
            except:
                pass


class RackPowerSensor(PowerSensor):
    """Rack-level power sensor for datacenter monitoring.
    
    Placeholder for future integration with PDU/BMC-level power monitoring.
    """
    
    def __init__(self, rack_id: str, endpoint: str):
        """Initialize rack power sensor.
        
        Args:
            rack_id: Rack identifier
            endpoint: API endpoint for power data
        """
        self.rack_id = rack_id
        self.endpoint = endpoint
        self._initialized = False
    
    def initialize(self) -> None:
        """Initialize rack sensor connection."""
        # Placeholder for PDU/BMC API connection
        logger.warning("RackPowerSensor is not yet implemented")
        raise NotImplementedError("Rack-level monitoring coming soon")
    
    def get_power_watts(self) -> float:
        raise NotImplementedError()
    
    def get_temperature(self) -> Optional[float]:
        return None
    
    def get_device_info(self) -> Dict[str, Any]:
        return {
            "name": f"Rack-{self.rack_id}",
            "type": "RACK_PDU",
            "features": ["power"]
        }
    
    def shutdown(self) -> None:
        pass


def create_power_sensor(sensor_type: str = "nvidia", **kwargs) -> PowerSensor:
    """Factory function to create power sensors.
    
    Args:
        sensor_type: Type of sensor ("nvidia", "rack")
        **kwargs: Sensor-specific parameters
        
    Returns:
        PowerSensor instance
        
    Example:
        >>> sensor = create_power_sensor("nvidia", gpu_index=0)
        >>> sensor.initialize()
        >>> power = sensor.get_power_watts()
    """
    sensors = {
        "nvidia": NvidiaPowerSensor,
        "rack": RackPowerSensor,
    }
    
    if sensor_type not in sensors:
        raise ValueError(f"Unknown sensor type: {sensor_type}. "
                       f"Available: {list(sensors.keys())}")
    
    return sensors[sensor_type](**kwargs)
