from typing import Optional

from sqlalchemy.exc import IntegrityError

from logger import logger
from models import SavingGoal, Session
from schemas.saving_goal import SavingGoalSchema
from services import YahooFinanceService


class SavingGoalService:
    """
    Service class for managing saving goals.
    """

    @staticmethod
    def convert_to_brl(goal: SavingGoalSchema) -> Optional[float]:
        """
        Converts the goal value to BRL if the currency is different.
        Using the external YahooFinanceService to fetch the exchange rate and convert the goal value
        Returns the converted value or an error response
        """
        if goal.goal_currency != "BRL":
            try:
                pair = f"{goal.goal_currency.value}BRL=X"
                exchange_rate = YahooFinanceService.get_exchange_rate(pair)
                converted_value = round(goal.goal_value * exchange_rate, 2)
                return converted_value
            except Exception as e:
                error_msg = "Could not fetch the exchange rate and convert the goal value"
                logger.error(f"{error_msg}: {str(e)}")
                return None
        else:
            return goal.goal_value

    @staticmethod
    def post_saving_goal(goal: SavingGoalSchema):
        """
        Creates a new saving goal in the database.
        Returns a representation of the saving goal.
        """
        logger.info(f"Adding saving goal with name: '{goal.goal_name}'")

        # Using the external YahooFinanceService to fetch the exchange rate and convert the goal value to BRL
        converted_value = SavingGoalService.convert_to_brl(goal)

        if converted_value is None:
            # If conversion failed, return an error response
            error_msg = "Could not fetch the exchange rate and convert the goal value."
            return {"message": error_msg}, 400

        # Creating a SavingGoal instance to save it to the database
        saving_goal = SavingGoal(
            goal_name=goal.goal_name,
            goal_currency=goal.goal_currency,
            goal_value=goal.goal_value,
            monthly_savings=goal.monthly_savings,
            converted_value=converted_value
        )

        session = Session()
        try:
            session.add(saving_goal)
            session.commit()
            logger.info("Saving goal added successfully")
            return saving_goal.to_dict(), 200
        except IntegrityError:
            session.rollback()
            error_msg = "Saving goal with the same name already exists."
            logger.warning(error_msg)
            return {"message": error_msg}, 409
        except Exception as e:
            session.rollback()
            error_msg = "Could not save the new saving goal."
            logger.error(f"{error_msg}: {str(e)}")
            return {"message": error_msg}, 400
        finally:
            session.close()


    @staticmethod
    def get_saving_goals():
        """
        Returns a representation of all saving goals in the database.
        Returns a list of saving goals.
        """
        logger.info("Retrieving all saving goals")
        session = None

        try:
            session = Session()
            saving_goals = session.query(SavingGoal).all()

            if not saving_goals:
                return {"saving_goals": []}, 200

            logger.info(f"{len(saving_goals)} saving goals found")
            return {"saving_goals": [goal.to_dict() for goal in saving_goals]}, 200

        except Exception as e:
            error_msg = "Error retrieving saving goals"
            logger.error(f"{error_msg}: {str(e)}")
            return {"message": error_msg}, 400

        finally:
            if session:
                session.close()

    @staticmethod
    def get_saving_goal_by_id(goal_id: int):
        """
        Returns a specific Saving Goal by its ID.
        """
        logger.info(f"Retrieving saving goal with ID: {goal_id}")
        session = None

        try:
            session = Session()
            # Find the saving goal by ID
            saving_goal = session.query(SavingGoal).filter(SavingGoal.id == goal_id).first()

            if not saving_goal:
                error_msg = f"Saving goal with ID {goal_id} not found."
                logger.warning(error_msg)
                return {"message": error_msg}, 404

            logger.info(f"Saving goal with ID {goal_id} found")
            return saving_goal.to_dict(), 200

        except Exception as e:
            error_msg = f"Error retrieving saving goal with ID {goal_id}."
            logger.error(f"{error_msg}: {str(e)}")
            return {"message": error_msg}, 400

        finally:
            if session:
                session.close()

    @staticmethod
    def delete_saving_goal_by_id(goal_id: int):
        """
        Deletes a specific Saving Goal by its ID.
        """
        logger.info(f"Deleting saving goal with ID: '{goal_id}'")

        session = None
        try:
            session = Session()

            # Find the saving goal by ID
            saving_goal = session.query(SavingGoal).filter(SavingGoal.id == goal_id).first()

            if not saving_goal:
                error_msg = f"Saving goal with ID {goal_id} not found."
                logger.warning(error_msg)
                return {"message": error_msg}, 404

            # Delete the saving goal
            session.delete(saving_goal)
            session.commit()
            logger.info(f"Saving goal with ID {goal_id} deleted successfully")

            return {"message": f"Saving goal with ID {goal_id} deleted successfully"}, 200

        except Exception as e:
            error_msg = f"Error deleting saving goal with ID {goal_id}."
            logger.error(f"{error_msg}: {str(e)}")
            return {"message": error_msg}, 400

        finally:
            if session:
                session.close()

    @staticmethod
    def put_saving_goal_by_id(goal_id: int, goal: SavingGoalSchema):
        """
        Updates an existing saving goal in the database by ID.
        Returns a representation of the saving goal.
        """
        logger.info(f"Updating saving goal with ID: '{goal_id}'")

        # Using the external YahooFinanceService to fetch the exchange rate and convert the goal value to BRL
        converted_value = SavingGoalService.convert_to_brl(goal)

        if converted_value is None:
            # If conversion failed, return an error response
            error_msg = "Could not fetch the exchange rate and convert the goal value."
            return {"message": error_msg}, 400

        session = None
        try:
            session = Session()

            # Find the saving goal by ID
            saving_goal = session.query(SavingGoal).filter(SavingGoal.id == goal_id).first()

            if not saving_goal:
                error_msg = f"Saving goal with ID {goal_id} not found."
                logger.warning(error_msg)
                return {"message": error_msg}, 404

            # Creating a SavingGoal instance to update it to the database
            saving_goal.goal_name = goal.goal_name
            saving_goal.goal_currency = goal.goal_currency
            saving_goal.goal_value = goal.goal_value
            saving_goal.monthly_savings = goal.monthly_savings
            saving_goal.converted_value = converted_value

            session.commit()
            logger.info(f"Saving goal with ID {goal_id} updated successfully")

            return saving_goal.to_dict(), 200

        except Exception as e:
            error_msg = f"Could not update saving goal with ID {goal_id}."
            logger.warning(f"Error updating saving goal with ID {goal_id}: {str(e)}")
            return {"message": error_msg}, 400

        finally:
            if session:
                session.close()
