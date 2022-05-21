from sqlmodel.sql.expression import Select, SelectOfScalar


def fix_inherit_cache_warning():
    """Fix inherit cache warning, details: sqlmodel#189"""
    SelectOfScalar.inherit_cache = True
    Select.inherit_cache = True
