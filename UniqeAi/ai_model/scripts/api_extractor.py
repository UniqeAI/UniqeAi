#!/usr/bin/env python3
"""
API Endpoint Extractor for Telekom AI Training Dataset
Automatically extracts all unique API endpoints from the extended dataset
and generates/updates API mapping files.
"""

import re
import json
from pathlib import Path
from typing import Set, Dict, List
from collections import defaultdict

class APIExtractor:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.api_pattern = re.compile(r'backend_api\.([a-zA-Z_][a-zA-Z0-9_]*)')
        
    def extract_apis_from_file(self, file_path: Path) -> Set[str]:
        """Extract all unique API endpoints from a Python file"""
        apis = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = self.api_pattern.findall(content)
                apis.update(matches)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            
        return apis
        
    def categorize_apis(self, apis: Set[str]) -> Dict[str, List[str]]:
        """Categorize API endpoints based on their names"""
        categories = defaultdict(list)
        
        # API kategorileri için keyword mapping
        category_keywords = {
            "User Management": ["user", "customer", "account", "profile", "register", "login", "auth"],
            "Product Management": ["product", "category", "item", "inventory", "stock", "price", "catalog"],
            "Order Management": ["order", "cart", "checkout", "purchase", "sale", "transaction"],
            "Payment & Billing": ["payment", "bill", "invoice", "charge", "refund", "credit", "debit"],
            "Analytics & Reporting": ["report", "analytics", "segment", "analyze", "forecast", "trend", "metric"],
            "Communication & Support": ["support", "ticket", "message", "communication", "notification", "help"],
            "AI & Machine Learning": ["ai", "predict", "recommendation", "neural", "sentiment", "behavior"],
            "Blockchain & Security": ["blockchain", "verify", "security", "auth", "encrypt", "quantum"],
            "Telecom Package": ["package", "tariff", "quota", "subscription", "line", "sim"],
            "Telecom Technical": ["network", "signal", "fault", "technical", "infrastructure", "modem"],
            "Telecom Billing": ["autopay", "payment_status", "bill_details"],
            "Advanced Features": ["ar", "vr", "drone", "voice", "biometric", "sustainability", "carbon"]
        }
        
        for api in sorted(apis):
            api_lower = api.lower()
            categorized = False
            
            for category, keywords in category_keywords.items():
                if any(keyword in api_lower for keyword in keywords):
                    categories[category].append(api)
                    categorized = True
                    break
                    
            if not categorized:
                categories["General"].append(api)
                
        return dict(categories)
        
    def generate_mapping_dict(self, apis: Set[str]) -> Dict[str, str]:
        """Generate API mapping dictionary"""
        mapping = {}
        for api in sorted(apis):
            mapping[api] = f"backend_api.{api}"
        return mapping
        
    def extract_from_dataset(self, file_path: str = "extended_data_generator.py") -> None:
        """Extract APIs from the extended dataset and generate mapping"""
        dataset_path = self.base_path / file_path
        
        if not dataset_path.exists():
            print(f"Dataset file not found: {dataset_path}")
            return
            
        print(f"Extracting APIs from: {dataset_path}")
        apis = self.extract_apis_from_file(dataset_path)
        
        print(f"Found {len(apis)} unique API endpoints")
        
        # Categorize APIs
        categorized = self.categorize_apis(apis)
        
        # Generate mapping
        mapping = self.generate_mapping_dict(apis)
        
        # Save results
        self.save_api_mapping(mapping, categorized)
        self.save_api_analysis(apis, categorized)
        
        print("\nAPI extraction completed successfully!")
        print(f"- Updated: {self.base_path}/UniqeAi/ai_model/scripts/api_mapping_v2.py")
        print(f"- Analysis: {self.base_path}/UniqeAi/ai_model/scripts/api_analysis.json")
        
    def save_api_mapping(self, mapping: Dict[str, str], categorized: Dict[str, List[str]]) -> None:
        """Save the API mapping to a Python file"""
        output_path = self.base_path / "UniqeAi/ai_model/scripts/api_mapping_v2.py"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('"""\n')
            f.write('COMPREHENSIVE API MAPPING FOR TELEKOM AI TRAINING DATASET\n')
            f.write('Version 2.0 - Auto-generated from extended dataset\n')
            f.write('\n')
            f.write('This file contains all API endpoints extracted from the extended dataset.\n')
            f.write('Use this mapping to easily update backend API paths once finalized.\n')
            f.write('\n')
            f.write('Generated by: api_extractor.py\n')
            f.write('Total endpoints: {}\n'.format(len(mapping)))
            f.write('"""\n\n')
            
            f.write('# Complete API mapping dictionary\n')
            f.write('API_MAP = {\n')
            
            # Write categorized APIs
            for category, apis in categorized.items():
                f.write(f'\n    # --- {category} ---\n')
                for api in apis:
                    f.write(f'    "{api}": "{mapping[api]}",\n')
            
            f.write('}\n\n')
            
            # Add helper functions
            f.write('def get_api_path(api_name: str) -> str:\n')
            f.write('    """Get the full API path for a given API name"""\n')
            f.write('    return API_MAP.get(api_name, f"backend_api.{api_name}")\n\n')
            
            f.write('def get_apis_by_category() -> dict:\n')
            f.write('    """Get APIs organized by category"""\n')
            f.write('    return {\n')
            for category, apis in categorized.items():
                f.write(f'        "{category}": {apis},\n')
            f.write('    }\n\n')
            
            f.write('def get_all_apis() -> list:\n')
            f.write('    """Get all API names as a list"""\n')
            f.write('    return list(API_MAP.keys())\n\n')
            
            f.write('# Version information\n')
            f.write('VERSION = "2.0"\n')
            f.write('TOTAL_ENDPOINTS = {}\n'.format(len(mapping)))
            
    def save_api_analysis(self, apis: Set[str], categorized: Dict[str, List[str]]) -> None:
        """Save API analysis to JSON file"""
        analysis_path = self.base_path / "UniqeAi/ai_model/scripts/api_analysis.json"
        
        analysis = {
            "total_endpoints": len(apis),
            "categories": {cat: len(apis_list) for cat, apis_list in categorized.items()},
            "categorized_apis": categorized,
            "all_apis": sorted(list(apis)),
            "extraction_date": "2024-01-01",  # Will be updated when run
            "version": "2.0"
        }
        
        with open(analysis_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)

def main():
    """Main execution function"""
    print("=== Telekom AI API Extractor ===")
    print("Extracting API endpoints from extended dataset...")
    
    extractor = APIExtractor()
    extractor.extract_from_dataset()
    
    print("\n=== Extraction Summary ===")
    print("1. Created comprehensive API mapping (api_mapping_v2.py)")
    print("2. Generated API analysis report (api_analysis.json)")
    print("3. Categorized APIs by functionality")
    print("4. Added helper functions for easy usage")
    print("\nNext steps:")
    print("- Review the generated mapping file")
    print("- Update extended_data_generator.py to use the mapping")
    print("- Coordinate with backend team for final API paths")

if __name__ == "__main__":
    main() 