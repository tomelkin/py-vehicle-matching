from dataclasses import dataclass

@dataclass
class Vehicle:
    """
    Data class representing a vehicle.

    Attributes:
        id (int): Unique identifier for the vehicle.
        make (str): The make of the vehicle.
        model (str): The model of the vehicle.
        badge (str): The badge or trim of the vehicle.
        transmission_type (str): The transmission type of the vehicle.
        fuel_type (str): The fuel type of the vehicle.
        drive_type (str): The drive type of the vehicle.
    """
    id: int
    make: str
    model: str
    badge: str
    transmission_type: str
    fuel_type: str
    drive_type: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vehicle):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def get_description(self) -> str:
        attributes = [
            self.make or "",
            self.model or "", 
            self.badge or "",
            self.transmission_type or "",
            self.fuel_type or "",
            self.drive_type or ""
        ]
        return " ".join(attr for attr in attributes if attr).lower()

    @staticmethod
    def from_db_row(row: dict | tuple) -> "Vehicle":
        if isinstance(row, dict):
            try:
                return Vehicle(
                    id=row["id"],
                    make=row["make"],
                    model=row["model"],
                    badge=row["badge"],
                    transmission_type=row["transmission_type"],
                    fuel_type=row["fuel_type"],
                    drive_type=row["drive_type"]
                )
            except KeyError as e:
                raise ValueError(f"Missing required field in row: {e}")
        elif isinstance(row, tuple):
            if len(row) != 7:
                raise ValueError(f"Expected 7 fields in tuple, got {len(row)}")
            return Vehicle(*row)
        else:
            raise ValueError(f"Unsupported row type: {type(row)}") 