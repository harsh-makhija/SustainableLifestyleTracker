from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from users.form import ExerciseLogForm
from app import db
from models import ExerciseLog

function_blueprint = Blueprint('log', __name__, template_folder='templates')


"""
    This file contains all the routes for the exercise log functionality
"""
@function_blueprint.route("/log")
@login_required
def log_main():
    return render_template("exerciseLog/Log.html", name=current_user.firstname)



@function_blueprint.route("/log/CreateLog", methods=['GET', 'POST'])
@login_required
def create_log():
    """
    Developed by Harsh
        This route is used to create a new exercise log
    """
    form = ExerciseLogForm()

    if form.validate_on_submit():
        # Create a new ExerciseLog object with the submitted data and the current user's entry_num
        new_exercise_log = ExerciseLog(
            entry_num=form.entry_num.data,
            email=current_user.email,
            date=form.exercise_date.data,
            exercise_type=form.exercise_type.data,
            duration=form.duration.data,
            intensity=form.intensity.data,
            comments=form.comments.data
        )

        # Add the new exercise_log to the database
        db.session.add(new_exercise_log)
        db.session.commit()

        flash('Your exercise has been logged!')
        return render_template("exerciseLog/Log.html", name=current_user.firstname)

    return render_template("exerciseLog/CreateLog.html", form=form)


@function_blueprint.route("/log/ViewLog", methods=['GET', 'POST'])
def view_log():
    """
    Developed by Harsh
        This route is used to view all the exercise logs for the current user
    """
    all_logs = ExerciseLog.query.filter_by(email=current_user.email).all()
    if not all_logs:
        flash('There are no logs to view, Please create a log')
        return render_template("exerciseLog/Log.html", name=current_user.firstname)
    else:
        return render_template("exerciseLog/ViewLog.html", name=current_user.firstname, logs=all_logs)



@function_blueprint.route("/log/DeleteLog", methods=['GET', 'POST'])
@login_required
def delete_log():
    """
    Developed by Harsh
        This route is used to Delete exercise
    """
    # Get all the logs for the current user
    logs_to_delete = ExerciseLog.query.filter_by(email=current_user.email).all()

    # Loops through checking which logs have been selected to delete
    for log in logs_to_delete:
        # Delete the log from the database
        db.session.delete(log)
    db.session.commit()
    return render_template("exerciseLog/DeleteLog.html", name=current_user.firstname)
