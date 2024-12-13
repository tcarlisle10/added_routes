from app.models import Skill
from app.extensions import ma


class SkillSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Skill
        include_fk = True

skill_schema = SkillSchema()
skills_schema = SkillSchema(many=True)