import pandas as pd
from pathlib import Path
from pydantic import BaseModel


class FileInput(BaseModel):
    file_path: Path

    @classmethod
    def validate_file_path(cls, value: Path) -> Path:
        if not value.exists():
            raise ValueError(f"File '{value}' does not exist.")
        if value.suffix.lower() not in {'.csv', '.xlsx'}:
            raise ValueError(f"Unsupported file format. Please provide a CSV or Excel file.")
        return value


class DemandLoader:
    def __init__(self, file_path: Path):
        validated_file_path = FileInput(file_path=file_path).file_path
        self.demand_data = self.load_demand_data(validated_file_path)

    @staticmethod
    def load_demand_data(file_path: Path) -> dict:
        demand_data = {}
        if file_path.suffix.lower() == '.csv':
            demand_df = pd.read_csv(file_path)
        else:
            demand_df = pd.read_excel(file_path)
        for _, row in demand_df.iterrows():
            product_id = row['product_id']
            week_id = row['week_id']
            demand = row['demand']
            demand_data.setdefault(product_id, {})[week_id] = demand
        return demand_data


class CapacityLoader:
    def __init__(self, file_path: Path):
        validated_file_path = FileInput(file_path=file_path).file_path
        self.capacity_data = self.load_capacity_data(validated_file_path)

    @staticmethod
    def load_capacity_data(file_path: Path) -> dict:
        capacity_data = {}
        if file_path.suffix.lower() == '.csv':
            capacity_df = pd.read_csv(file_path)
        else:
            capacity_df = pd.read_excel(file_path)
        for _, row in capacity_df.iterrows():
            machine_id = row['machine_id']
            product_id = row['product_id']
            week_cap = row['week_cap']
            capacity_data.setdefault(machine_id, {})[product_id] = week_cap
        return capacity_data


class TranstimeLoader:
    def __init__(self, file_path: Path):
        validated_file_path = FileInput(file_path=file_path).file_path
        self.transtime_data = self.load_transition_times(validated_file_path)

    @staticmethod
    def load_transition_times(file_path: Path) -> dict:
        transition_times = {}
        if file_path.suffix.lower() == '.csv':
            transition_df = pd.read_csv(file_path)
        elif file_path.suffix.lower() == '.xlsx':
            transition_df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")

        for _, row in transition_df.iterrows():
            machine_id = row['machine_Id']
            from_product = row['from']
            to_product = row['to']
            trans_time_days = row['trans_time_days']

            if machine_id not in transition_times:
                transition_times[machine_id] = {}

            transition_times[machine_id].setdefault((from_product, to_product), trans_time_days)

        return transition_times


class DowntimeLoader:
    def __init__(self, file_path: Path):
        validated_file_path = FileInput(file_path=file_path).file_path
        self.downtime_data = self.load_downtime_data(validated_file_path)

    @staticmethod
    def load_downtime_data(file_path: Path) -> dict:
        downtime_data = {}
        if file_path.suffix.lower() == '.csv':
            downtime_df = pd.read_csv(file_path)
        elif file_path.suffix.lower() == '.xlsx':
            downtime_df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")

        for _, row in downtime_df.iterrows():
            machine_id = row['machine_Id']
            week_id = row['week_id']

            downtime_data.setdefault(week_id, set()).add(machine_id)

        return downtime_data


# Example usage for loading demand data
demand_loader = DemandLoader(file_path=Path("input/demand.xlsx"))
print(demand_loader.demand_data)

# Example usage for loading capacity data
capacity_loader = CapacityLoader(file_path=Path("input/capacity.xlsx"))
print(capacity_loader.capacity_data)

# Example usage for loading transition times data
transtime_loader = TranstimeLoader(file_path=Path("input/transition_times.xlsx"))
print(transtime_loader.transtime_data)

# Example usage for loading scheduled downtime data
downtime_loader = DowntimeLoader(file_path=Path("input/scheduled_downtime.xlsx"))
print(downtime_loader.downtime_data)

# # Example usages
# demand_loader.demand_data.get('product_100', {}).get('week_29', 0)
# capacity_loader.capacity_data.get('machine_1', {}).get('product_1', 0)
# transtime_loader.transtime_data.get('machine_1', {}).get(('product_1', 'product_2'), 0)
# downtime_loader.downtime_data.get('week_1', set())

print('hi')
