"""Authentication provider interface and interactive login results."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from ..domain.models import AuthSession


@dataclass(frozen=True, slots=True)
class ChallengeOption:
    """One verification channel offered by the account service.

    ``sent`` is the account service's own flag: ``False`` means the channel is
    merely *available* and no code has been dispatched yet. Treating it as
    "already sent" is why a user can end up staring at a code field that will
    never be filled.
    """

    name: str
    account_type: str
    sent: bool


@dataclass(frozen=True, slots=True)
class LoginChallenge:
    """Challenge information shown to the user."""

    prompt: str
    challenge_name: str
    challenge_type: str
    options: tuple[ChallengeOption, ...] = ()


@dataclass(frozen=True, slots=True)
class LoginStart:
    """Result of starting an account login."""

    session: AuthSession | None = None
    challenge: LoginChallenge | None = None


class AuthProvider(Protocol):
    """Port for Huawei account authentication."""

    async def async_begin_login(self, account: str, password: str) -> LoginStart:
        """Start account/password login."""

    async def async_complete_challenge(self, code: str) -> AuthSession:
        """Complete a pending device challenge."""

    async def async_refresh_oauth(self, session: AuthSession) -> AuthSession:
        """Refresh the OAuth session token with the Huawei service token."""

    async def async_refresh_hms_lite(self, session: AuthSession) -> AuthSession:
        """Reissue the HMS-lite token through the Huawei silent-auth flow."""
