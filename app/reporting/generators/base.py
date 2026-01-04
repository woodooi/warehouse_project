from abc import ABC, abstractmethod
from typing import Dict, Any

class ReportGenerator(ABC):
    def generate_file(self, data: Dict[str, Any]) -> str:
        """Template method for generating a report file."""
        content = []
        content.append(self.header(data))
        content.append(self.body(data))
        content.append(self.footer(data))
        return "\n".join(content)

    @abstractmethod
    def header(self, data: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def body(self, data: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def footer(self, data: Dict[str, Any]) -> str:
        pass
