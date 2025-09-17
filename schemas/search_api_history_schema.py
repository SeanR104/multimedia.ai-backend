from pydantic import BaseModel


class SearchApiHistoryBase(BaseModel):
    api_name: str
    url_text: str
    url_parameters: str
    post_body: str
    http_status: str
    platform_running: str

    class Config:
        from_attribute = True


class SearchApiHistoryView(SearchApiHistoryBase):
    pass


class SearchApiHistoryAdd(SearchApiHistoryBase):
    pass


class SearchApiHistoryEdit(SearchApiHistoryBase):
    pass


class SearchApiHistoryRemove(SearchApiHistoryBase):
    pass
