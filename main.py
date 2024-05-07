from fastapi import FastAPI
from enroll import app as enroll_app
from feedback import app as feedback_app
from manage_profile import app as manage_profile_app
from student_materials import app as student_materials_app
from Student_assessment import app as student_assessment_app
from Teacher_assessment import app as teacher_assessment_app
from Teacher_feedback import app as teacher_feedback_app
from Teacher_materials import app as teacher_materials_app
from Student_login import app as Student_login_app

app = FastAPI()
# app.include_router(feedback_app)
app.include_router(Student_login_app,tags=["Student-login"])
app.include_router(enroll_app,tags=["enroll"])
app.include_router(feedback_app,tags=["feedback"])
app.include_router(manage_profile_app,tags=["manage-profile"])
app.include_router(student_materials_app,tags=["student-materials"])
app.include_router(student_assessment_app,tags=["student-assessment"])
app.include_router(teacher_assessment_app,tags=["teacher-assessment"])
app.include_router(teacher_feedback_app,tags=["teacher-feedback"])
app.include_router(teacher_materials_app,tags=["teacher-materials"])
