"""
CICIDS2017 Dataset Configuration Module

This module provides a centralized configuration for accessing the CICIDS2017 dataset files.
It automatically discovers the correct directory structure and provides helper functions
for loading data.

Usage:
    from data_config import DataConfig
    
    config = DataConfig()
    config.print_summary()
    
    # Load a specific file
    df = config.load_file('Monday-WorkingHours.pcap_ISCX.csv')
    
    # Or load from a specific dataset
    df = config.load_file('Monday-WorkingHours.pcap_ISCX.csv', dataset='ml')
"""

from pathlib import Path
from typing import Optional, List, Literal
import pandas as pd


class DataConfig:
    """Configuration and helper class for CICIDS2017 dataset access"""
    
    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize the data configuration
        
        Args:
            base_path: Base directory containing the dataset. 
                      If None, uses the default project path.
        """
        # Set base path
        if base_path is None:
            self.base_path = Path("/home/tesfayh/Artificial_inteligence/ML/CICDS/ML-CICIDS-project")
        else:
            self.base_path = Path(base_path)
        
        # Dataset base directories
        self.flow_base = self.base_path / "GeneratedLabelledFlows"
        self.ml_base = self.base_path / "MachineLearningCSV"
        
        # Find actual CSV directories
        self.flow_path = self._find_csv_directory(self.flow_base)
        self.ml_path = self._find_csv_directory(self.ml_base)
        
        # Get file lists
        self.flow_files = self._get_csv_files(self.flow_path) if self.flow_path else []
        self.ml_files = self._get_csv_files(self.ml_path) if self.ml_path else []
    
    def _find_csv_directory(self, parent_dir: Path) -> Optional[Path]:
        """
        Find the subdirectory containing CSV files
        
        Args:
            parent_dir: Parent directory to search
            
        Returns:
            Path to directory containing CSV files, or None if not found
        """
        if not parent_dir.exists():
            return None
        
        # Check if parent has CSV files directly
        csv_files = list(parent_dir.glob("*.csv"))
        if csv_files:
            return parent_dir
        
        # Check subdirectories
        for subdir in parent_dir.iterdir():
            if subdir.is_dir():
                csv_files = list(subdir.glob("*.csv"))
                if csv_files:
                    return subdir
        
        return None
    
    def _get_csv_files(self, directory: Optional[Path]) -> List[Path]:
        """Get sorted list of CSV files in a directory"""
        if directory is None or not directory.exists():
            return []
        return sorted(list(directory.glob("*.csv")))
    
    def print_summary(self):
        """Print a summary of the dataset configuration"""
        print("=" * 80)
        print("CICIDS2017 DATASET CONFIGURATION")
        print("=" * 80)
        print(f"\nBase directory: {self.base_path}")
        print(f"Exists: {'✓' if self.base_path.exists() else '✗'}")
        
        # GeneratedLabelledFlows info
        print("\n" + "-" * 80)
        print("GeneratedLabelledFlows Dataset")
        print("-" * 80)
        if self.flow_path:
            print(f"✓ Path: {self.flow_path}")
            print(f"  Files: {len(self.flow_files)}")
            if self.flow_files:
                total_size = sum(f.stat().st_size for f in self.flow_files) / (1024**3)
                print(f"  Total size: {total_size:.2f} GB")
        else:
            print(f"✗ Not found (searched: {self.flow_base})")
        
        # MachineLearningCSV info
        print("\n" + "-" * 80)
        print("MachineLearningCSV Dataset (Recommended for ML)")
        print("-" * 80)
        if self.ml_path:
            print(f"✓ Path: {self.ml_path}")
            print(f"  Files: {len(self.ml_files)}")
            if self.ml_files:
                total_size = sum(f.stat().st_size for f in self.ml_files) / (1024**3)
                print(f"  Total size: {total_size:.2f} GB")
        else:
            print(f"✗ Not found (searched: {self.ml_base})")
        
        # List files
        if self.ml_files:
            print("\n" + "-" * 80)
            print("Available CSV Files (MachineLearningCSV)")
            print("-" * 80)
            for i, f in enumerate(self.ml_files, 1):
                size_mb = f.stat().st_size / (1024 * 1024)
                print(f"  {i}. {f.name:<55} ({size_mb:>7.1f} MB)")
        
        print("\n" + "=" * 80)
    
    def get_file_path(
        self, 
        filename: str, 
        dataset: Literal['flow', 'ml'] = 'ml'
    ) -> Optional[Path]:
        """
        Get the full path to a specific CSV file
        
        Args:
            filename: Name of the CSV file
            dataset: Which dataset to use ('flow' or 'ml')
            
        Returns:
            Path to the file, or None if not found
        """
        if dataset == 'ml':
            base_path = self.ml_path
            file_list = self.ml_files
        else:
            base_path = self.flow_path
            file_list = self.flow_files
        
        if base_path is None:
            return None
        
        # Try exact match first
        file_path = base_path / filename
        if file_path.exists():
            return file_path
        
        # Try case-insensitive search
        for f in file_list:
            if f.name.lower() == filename.lower():
                return f
        
        return None
    
    def load_file(
        self,
        filename: str,
        dataset: Literal['flow', 'ml'] = 'ml',
        nrows: Optional[int] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Load a CSV file from the dataset
        
        Args:
            filename: Name of the CSV file to load
            dataset: Which dataset to use ('flow' or 'ml')
            nrows: Number of rows to read (None for all)
            **kwargs: Additional arguments to pass to pd.read_csv
            
        Returns:
            Loaded DataFrame
            
        Raises:
            FileNotFoundError: If the file is not found
        """
        file_path = self.get_file_path(filename, dataset)
        
        if file_path is None:
            raise FileNotFoundError(
                f"File '{filename}' not found in {dataset} dataset. "
                f"Available files: {[f.name for f in (self.ml_files if dataset == 'ml' else self.flow_files)]}"
            )
        
        print(f"Loading: {file_path.name}")
        if nrows:
            print(f"  Reading first {nrows:,} rows...")
        else:
            print(f"  Reading all rows...")
        
        df = pd.read_csv(file_path, nrows=nrows, **kwargs)
        print(f"  ✓ Loaded {len(df):,} rows × {len(df.columns)} columns")
        
        return df
    
    def load_all_files(
        self,
        dataset: Literal['flow', 'ml'] = 'ml',
        nrows: Optional[int] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Load and concatenate all CSV files from a dataset
        
        Args:
            dataset: Which dataset to use ('flow' or 'ml')
            nrows: Number of rows to read from each file (None for all)
            **kwargs: Additional arguments to pass to pd.read_csv
            
        Returns:
            Concatenated DataFrame from all files
        """
        file_list = self.ml_files if dataset == 'ml' else self.flow_files
        
        if not file_list:
            raise ValueError(f"No files found in {dataset} dataset")
        
        print(f"Loading {len(file_list)} files from {dataset} dataset...")
        
        dfs = []
        for file_path in file_list:
            print(f"\n  Processing: {file_path.name}")
            df = pd.read_csv(file_path, nrows=nrows, **kwargs)
            print(f"    ✓ {len(df):,} rows")
            dfs.append(df)
        
        combined = pd.concat(dfs, ignore_index=True)
        print(f"\n✓ Combined dataset: {len(combined):,} rows × {len(combined.columns)} columns")
        
        return combined


# Convenience function for quick access
def get_config(base_path: Optional[str] = None) -> DataConfig:
    """Get a DataConfig instance"""
    return DataConfig(base_path)


if __name__ == "__main__":
    # Demo usage
    config = get_config()
    config.print_summary()
