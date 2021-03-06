"""
es21.views.widgets.pr_card
==========================

Preacher's card.
"""

from functools import lru_cache

from tinydb import Query

from ...database import get_db
from ...utils import templated
from ...filters import is_auxiliary


@lru_cache()
@templated('widgets/pr_card.html')
def entry(id, use_long_name=False):
    db = get_db()
    q = Query()

    p = db.get(q.id == id)

    if p is None:
        return None

    return dict(
        p=p,
        use_long_name=use_long_name,
        is_auxiliary=is_auxiliary()(p))
