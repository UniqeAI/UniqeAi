# -*- coding: utf-8 -*-
"""
🚨 ENHANCED ERROR HANDLING - V3 OPTIMIZATION
============================================

Bu modül, SupremeHumanLevelDatasetGenerator için özel hata sınıflarını içerir.
Tüm hata yönetimi buradan merkezi olarak yapılır.
"""

class SchemaValidationError(Exception):
    """Schema validation hatası - daha detaylı error reporting için"""
    def __init__(self, function_name: str, error_detail: str):
        self.function_name = function_name
        self.error_detail = error_detail
        super().__init__(f"Schema validation failed for {function_name}: {error_detail}")

class ParameterMismatchError(Exception):
    """Parameter uyumsuzluğu hatası"""
    def __init__(self, function_name: str, missing_params: list, provided_params: list):
        self.function_name = function_name
        self.missing_params = missing_params
        self.provided_params = provided_params
        super().__init__(f"Parameter mismatch in {function_name}: missing {missing_params}, provided {provided_params}")
        

class DataGenerationError(Exception):
    """Veri üretimi hatası"""
    def __init__(self, scenario_type: str, error_detail: str):
        self.scenario_type = scenario_type
        self.error_detail = error_detail
        super().__init__(f"Data generation failed for {scenario_type}: {error_detail}")

class ValidationError(Exception):
    """Genel validasyon hatası"""
    def __init__(self, validation_type: str, error_detail: str):
        self.validation_type = validation_type
        self.error_detail = error_detail
        super().__init__(f"Validation failed for {validation_type}: {error_detail}")

class APIResponseError(Exception):
    """API yanıt hatası"""
    def __init__(self, api_function: str, error_detail: str):
        self.api_function = api_function
        self.error_detail = error_detail
        super().__init__(f"API response error for {api_function}: {error_detail}") 