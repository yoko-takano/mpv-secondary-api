from sqlalchemy import Column, String, Integer, DateTime, Float
from datetime import datetime
from typing import Any
from models import Base
from services import YahooFinanceService


class SavingGoal(Base):
    """
    Model representing a saving goal, including details such as the name,
    currency, value, and savings per month of the salary to be saved.
    """
    __tablename__ = "saving_goals"

    id = Column("pk_goal", Integer, primary_key=True, autoincrement=True)
    goal_name = Column(String(100), nullable=False)
    goal_currency = Column(String(10), nullable=False)
    goal_value = Column(Float, nullable=False)
    monthly_savings = Column(Float, nullable=False)
    converted_value = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    def __init__(
            self,
            goal_name: str,
            goal_currency: str,
            goal_value: float,
            monthly_savings: float,
            converted_value: float,
            **kw: Any):
        """
        Initializes a new saving goal with the provided parameters.

        :param goal_name: The name of the saving goal (e.g., "Trip to Japan")
        :param goal_currency: The currency for the saving goal (e.g., "BRL", "USD")
        :param goal_value: The total value to be saved for the goal
        :param monthly_savings: Savings per month of the salary to be saved
        :param converted_value: The converted value for the saving goal
        """
        super().__init__(**kw)
        self.goal_name = goal_name
        self.goal_currency = goal_currency.split(".")[-1]
        self.goal_value = goal_value
        self.monthly_savings = monthly_savings
        self.goal_currency = goal_currency
        self.converted_value = converted_value

    def to_dict(self):
        """
        Returns a dictionary representation of the SavingGoal object.
        """
        return {
            "id": self.id,
            "goal_name": self.goal_name,
            "goal_currency": self.goal_currency,
            "goal_value": self.goal_value,
            "monthly_savings": self.monthly_savings,
            "converted_value": self.converted_value,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def __repr__(self):
        return f"SavingGoal(id={self.id}, goal_name='{self.goal_name}', goal_currency='{self.goal_currency}', goal_value={self.goal_value}, monthly_savings={self.monthly_savings}, converted_value={self.converted_value})"
