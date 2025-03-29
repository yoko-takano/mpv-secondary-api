import enum
from datetime import datetime
from pydantic import BaseModel, field_validator, Field
from typing import List


class CurrencyEnumSchema(str, enum.Enum):
    """
    Enum that defines the possible currencies for a saving goal.
    """
    USD = "USD"
    BRL = "BRL"
    EUR = "EUR"
    JPY = "JPY"
    KRW = "KRW"


class SavingGoalSchema(BaseModel):
    """
    Defines how a new saving goal should be represented for insertion.
    """
    goal_name: str = Field("Pretty dress", description="Name of the saving goal")
    goal_currency: CurrencyEnumSchema = Field("USD", description="Currency of the saving goal")
    goal_value: float = Field(300.00, description="Total value to be saved for the goal")
    monthly_savings: float = Field(100.0, description="Savings per month of the salary to be saved")

    class Config:
        orm_mode = True


class SavingGoalSearchSchema(BaseModel):
    """
    Defines the structure for searching a SavingGoal based on its unique identifier (goal_id).
    """
    goal_id: int = Field(..., description="The unique identifier for a SavingGoal in the database")


class SavingGoalViewSchema(BaseModel):
    """
    Defines how a saving goal will be returned with full data.
    """
    id: int
    goal_name: str
    goal_currency: str
    goal_value: float
    monthly_savings: float
    converted_value: float
    created_at: datetime

    class Config:
        orm_mode = True

    @field_validator("created_at")
    @classmethod
    def convert_datetime(cls, v):
        """
        Converts the datetime object to a formatted string.
        """
        return v.strftime("%Y-%m-%d %H:%M:%S") if isinstance(v, datetime) else v


class SavingGoalsListSchema(BaseModel):
    """
    Defines how a list of saving goals will be returned.
    """
    saving_goals: List[SavingGoalViewSchema]

    class Config:
        orm_mode = True
