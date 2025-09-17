from pydantic import BaseModel


class SearchApiStatusBase(BaseModel):
    platform_running: str

    class Config:
        from_attribute = True


class SearchApiStatusView(SearchApiStatusBase):
    pass


class SearchApiStatusAdd(SearchApiStatusBase):
    api_name: str


class SearchApiStatusEdit(SearchApiStatusBase):
    pass


class SearchApiStatusRemove(SearchApiStatusBase):
    pass


class SearchApiStatusFilter(BaseModel):
    api_name: str
    platform_running: str
