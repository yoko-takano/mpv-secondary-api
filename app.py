from datetime import datetime

from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from sqlalchemy.exc import IntegrityError
from logger import logger
from flask_cors import CORS

from models import SavingGoal, Session
from schemas import ErrorSchema
from schemas.saving_goal import SavingGoalViewSchema, SavingGoalSchema, SavingGoalsListSchema, SavingGoalSearchSchema, \
    ConversionRequestSchema
from services import YahooFinanceService

info = Info(title="Secondary API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Defining tags
home_tag = Tag(name="Documentation", description="Selection of documentation style: Swagger, Redoc, or RapiDoc")
goals_tag = Tag(name="Goals", description="Creation, retrieval, and management of saving goals in the database")
finance_tag = Tag(name="Finance", description="")


@app.get('/', tags=[home_tag])
def home():
    """
    Redirects to /openapi, where the user can choose the documentation style.
    """
    return redirect('/openapi')


@app.post('/goals', tags=[goals_tag], responses={"200": SavingGoalViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_saving_goal(form: SavingGoalSchema):
    """
    Adds a new saving goal to the database
    Returns a representation of the saving goal.
    """
    logger.info(f"Adding saving goal with name: '{form.goal_name}'")
    saving_goal = SavingGoal(
        goal_name=form.goal_name,
        goal_currency=form.goal_currency,
        goal_value=form.goal_value,
        monthly_savings=form.monthly_savings,
    )

    session = None
    try:
        session = Session()
        session.add(saving_goal)
        session.commit()
        logger.info("Saving goal added successfully")
        return saving_goal.to_dict(), 200

    except IntegrityError:
        session.rollback()
        error_msg = "Saving goal with the same name already exists in the database."
        logger.warning(f"Error adding saving goal '{saving_goal.goal_name}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        error_msg = "Could not save the new saving goal."
        logger.warning(f"Error adding saving goal '{saving_goal.goal_name}', {error_msg}: {str(e)}")
        return {"message": error_msg}, 400

    finally:
        if session:
            session.close()


@app.get('/goals', tags=[goals_tag], responses={"200": SavingGoalsListSchema, "404": ErrorSchema})
def get_saving_goals():
    """
    Retrieves all saving goals from the database.
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


@app.get('/goals/<goal_id>', tags=[goals_tag],
         responses={"200": SavingGoalViewSchema, "404": ErrorSchema})
def get_saving_goal(query: SavingGoalSearchSchema):
    """
    Returns a specific Saving Goal by its ID.
    """
    goal_id = query.goal_id
    logger.info(f"Retrieving saving goal with ID: {query.goal_id}")
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

@app.delete('/goals/<goal_id>', tags=[goals_tag],
            responses={"200": {"description": "Successfully deleted the goal"}, "404": ErrorSchema, "400": ErrorSchema})
def delete_saving_goal(query: SavingGoalSearchSchema):
    """
    Deletes a specific Saving Goal by its ID.
    """
    goal_id = query.goal_id
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


@app.put('/goals/<goal_id>', tags=[goals_tag],
         responses={"200": SavingGoalViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_saving_goal(query: SavingGoalSearchSchema, form: SavingGoalSchema):
    """
    Updates an existing saving goal in the database by ID.
    """
    goal_id = query.goal_id
    logger.info(f"Updating saving goal with ID: '{goal_id}'")

    session = None
    try:
        session = Session()

        # Find the saving goal by ID
        saving_goal = session.query(SavingGoal).filter(SavingGoal.id == goal_id).first()

        if not saving_goal:
            error_msg = f"Saving goal with ID {goal_id} not found."
            logger.warning(error_msg)
            return {"message": error_msg}, 404

        # Update the fields of the existing saving goal
        saving_goal.goal_name = form.goal_name
        saving_goal.goal_currency = form.goal_currency
        saving_goal.goal_value = form.goal_value
        saving_goal.monthly_savings = form.monthly_savings

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


@app.get('/convert-currency', tags=[finance_tag],
         responses={"200": {"description": "Conversion Successful"},
                    "404": {"description": "Currency Data Not Found"},
                    "400": {"description": "Invalid Request"}})
def convert_currency(query: ConversionRequestSchema):
    """
    Converts an amount from one currency to another based on the current exchange rate.
    """
    try:
        # Monta o par de moedas para consulta no Yahoo Finance
        pair = f"{query.from_currency}{query.to_currency}=X"
        print(f"pair: {pair}")
        # Obtém a taxa de câmbio
        exchange_rate = YahooFinanceService.get_exchange_rate(pair)

        # Calcula o valor convertido
        converted_amount = query.amount * exchange_rate

        return {
            "amount": query.amount,
            "from_currency": query.from_currency,
            "to_currency": query.to_currency,
            "exchange_rate": exchange_rate,
            "converted_amount": converted_amount
        }
    except Exception as e:
        return {"message": f"Error: {str(e)}"}, 500
