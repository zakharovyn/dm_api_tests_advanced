from __future__ import annotations
from services.dm_api_account.models.user_envelope_model import UserRole, Rating
from pydantic import BaseModel, Field, StrictStr, ConfigDict
from typing import Any, List, Optional
from datetime import datetime
from enum import Enum


class PagingSettings(BaseModel):

    model_config = ConfigDict(extra='forbid')

    posts_per_page: Optional[int] = Field(
        default=None, alias='postsPerPage',
        description='Number of posts on a game room page'
    )
    comments_per_page: Optional[int] = Field(
        default=None,
        alias='commentsPerPage',
        description='Number of commentaries on a game or a topic page',
    )
    topics_per_page: Optional[int] = Field(
        default=None,
        alias='topicsPerPage',
        description='Number of detached topics on a forum page',
    )
    messages_per_page: Optional[int] = Field(
        default=None,
        alias='messagesPerPage',
        description='Number of private messages and conversations on dialogue page',
    )
    entities_per_page: Optional[int] = Field(
        None, alias='entitiesPerPage',
        description='Number of other entities on page'
    )


class ColorSchema(Enum):
    modern = 'Modern'
    pale = 'Pale'
    classic = 'Classic'
    classic_pale = 'ClassicPale'
    night = 'Night'


class UserSettings(BaseModel):

    model_config = ConfigDict(extra='forbid')

    color_schema: Optional[ColorSchema] = Field(
        default=None,
        alias='colorSchema'
    )
    nanny_greetings_message: Optional[StrictStr] = Field(
        default=None,
        alias='nannyGreetingsMessage',
        description="Message that user's newbies will receive once they are connected",
    )
    paging: Optional[PagingSettings] = None


class BbParseMode(Enum):
    common = 'Common'
    info = 'Info'
    post = 'Post'
    chat = 'Chat'


class InfoBbText(BaseModel):

    model_config = ConfigDict(extra='forbid')

    value: Optional[StrictStr] = Field(default=None, description='Text')
    parse_mode: Optional[BbParseMode] = Field(default=None, alias='parseMode')


class UserDetails(BaseModel):

    model_config = ConfigDict(extra='forbid')

    login: Optional[StrictStr] = Field(default=None, description='Login')
    roles: Optional[List[UserRole]] = Field(default=None, description='Roles')
    medium_picture_url: Optional[StrictStr] = Field(
        default=None,
        alias='mediumPictureUrl',
        description='Profile picture URL M-size'
    )
    small_picture_url: Optional[StrictStr] = Field(
        default=None,
        alias='smallPictureUrl',
        description='Profile picture URL S-size'
    )
    status: Optional[StrictStr] = Field(
        default=None,
        description='User defined status'
    )
    rating: Optional[Rating] = None
    online: Optional[datetime] = Field(
        default=None,
        description='Last seen online moment'
    )
    name: Optional[StrictStr] = Field(
        default=None,
        description='User real name'
    )
    location: Optional[StrictStr] = Field(
        default=None,
        description='User real location'
    )
    registration: Optional[datetime] = Field(
        default=None,
        description='User registration moment'
    )
    icq: Optional[StrictStr] = Field(
        default=None,
        description='User ICQ number'
    )
    skype: Optional[StrictStr] = Field(
        default=None,
        description='User Skype login'
    )
    original_picture_url: Optional[StrictStr] = Field(
        default=None,
        alias='originalPictureUrl',
        description='URL of profile picture original'
    )
    info: Optional[InfoBbText | str] = None
    settings: Optional[UserSettings] = None


class UserDetailsEnvelope(BaseModel):

    model_config = ConfigDict(extra='forbid')

    resource: Optional[UserDetails] = None
    metadata: Optional[Any] = Field(
        default=None,
        description='Additional metadata'
    )
