from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag, APIBlueprint

from schemas import ErrorSchema
from schemas.saving_goal import SavingGoalViewSchema, SavingGoalSchema, SavingGoalsListSchema, SavingGoalSearchSchema
from services.saving_goal import SavingGoalService

info = Info(title="Secondary API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Define the goals tag
goals_tag = Tag(name="Goals", description="Creation, retrieval, and management of saving goals in the database")
goals = APIBlueprint('goals', __name__, url_prefix='/goals', abp_tags=[goals_tag])


@goals.post('', tags=[goals_tag], responses={
    "200": SavingGoalViewSchema,
    "409": ErrorSchema,
    "400": ErrorSchema,
    "500": ErrorSchema})
def post_saving_goal(form: SavingGoalSchema):
    """
    Returns a representation of all saving goals in the database.
    Returns a list of saving goals.
    """
    return SavingGoalService.post_saving_goal(form)


@goals.get('', tags=[goals_tag], responses={
    "200": SavingGoalsListSchema,
    "404": ErrorSchema})
def get_saving_goals():
    """
    Retrieves all saving goals from the database.
    Returns a list of saving goals.
    """
    return SavingGoalService.get_saving_goals()


@goals.get('/<goal_id>', tags=[goals_tag], responses={
    "200": SavingGoalViewSchema,
    "404": ErrorSchema})
def get_saving_goal_by_id(query: SavingGoalSearchSchema):
    """
    Returns a specific Saving Goal by its ID.
    """
    return SavingGoalService.get_saving_goal_by_id(query.goal_id)


@goals.delete('/<goal_id>', tags=[goals_tag], responses={
    "200": {"description": "Successfully deleted the goal"},
    "404": ErrorSchema,
    "400": ErrorSchema})
def delete_saving_goal_by_id(query: SavingGoalSearchSchema):
    """
    Deletes a specific Saving Goal by its ID.
    """
    return SavingGoalService.delete_saving_goal_by_id(query.goal_id)


@goals.put('/<goal_id>', tags=[goals_tag], responses={
    "200": SavingGoalViewSchema,
    "404": ErrorSchema,
    "400": ErrorSchema})
def put_saving_goal_by_id(query: SavingGoalSearchSchema, form: SavingGoalSchema):
    """
    Updates an existing saving goal in the database by ID.
    Returns a representation of the saving goal.
    """
    return SavingGoalService.put_saving_goal_by_id(query.goal_id, form)
