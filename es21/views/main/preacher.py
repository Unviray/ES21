from tinydb import Query

from ...broadcast import templated, navbar_form
from ...database import get_db


@templated('pr_report.html')
@navbar_form
def entry(id):
    db = get_db()
    q = Query()

    result = db.get(q.id == id)

    return dict(
        pr=result,
    )
