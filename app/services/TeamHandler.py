from typing import Optional

from sqlmodel import select

from app.models.team import Team
from app.models.team_membership import Membership, Role
from app.models.user import User
from app.models.todo_list import TodoList
from app.services.BaseHandler import BaseHandler


class TeamHandler(BaseHandler):

    model = Team

    def create_team(self, name: str, creator_id: int, description: str = "") -> Team:
        if not name.strip():
            raise ValueError("Team name cannot be empty")

        team = Team(name=name, description=description, created_by_id=creator_id)
        self.save(team)

        # Ersteller wird automatisch als OWNER eingetragen
        membership = Membership(team_id=team.id, user_id=creator_id, role=Role.OWNER)
        self.session.add(membership)
        self.session.commit()
        self.session.refresh(membership)
        return team

    def update(
        self,
        team_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Optional[Team]:
        team = self.session.get(Team, team_id)
        if team is None:
            return None

        if name is not None:
            if not name.strip():
                raise ValueError("Team name cannot be empty")
            team.name = name
        if description is not None:
            team.description = description

        self.save(team)
        return team

    def add_member(self, team_id: int, user_id: int) -> Optional[Membership]:
        team = self.session.get(Team, team_id)
        if team is None:
            return None

        # Prüfen ob User bereits Mitglied ist
        existing = self.session.exec(
            select(Membership)
            .where(Membership.team_id == team_id)
            .where(Membership.user_id == user_id)
        ).first()
        if existing is not None:
            raise ValueError("User ist bereits Mitglied dieses Teams")

        membership = Membership(team_id=team_id, user_id=user_id, role=Role.MEMBER)
        self.session.add(membership)
        self.session.commit()
        self.session.refresh(membership)
        return membership

    def remove_member(self, team_id: int, user_id: int) -> bool:
        membership = self.session.exec(
            select(Membership)
            .where(Membership.team_id == team_id)
            .where(Membership.user_id == user_id)
        ).first()
        if membership is None:
            return False

        self.session.delete(membership)
        self.session.commit()
        return True

    def get_members(self, team_id: int) -> list[User]:
        memberships = self.session.exec(
            select(Membership).where(Membership.team_id == team_id)
        ).all()
        user_ids = [m.user_id for m in memberships if m.user_id is not None]
        if not user_ids:
            return []
        return list(self.session.exec(select(User).where(User.id.in_(user_ids))).all())

    def get_teams_for_user(self, user_id: int) -> list[Team]:
        memberships = self.session.exec(
            select(Membership).where(Membership.user_id == user_id)
        ).all()
        team_ids = [m.team_id for m in memberships if m.team_id is not None]
        if not team_ids:
            return []
        return list(self.session.exec(select(Team).where(Team.id.in_(team_ids))).all())

    def get_team_lists(self, team_id: int) -> list[TodoList]:
        return list(self.session.exec(
            select(TodoList).where(TodoList.team_id == team_id)
        ).all())

    def is_owner(self, team_id: int, user_id: int) -> bool:
        team = self.session.get(Team, team_id)
        if team is None:
            return False
        return team.created_by_id == user_id
