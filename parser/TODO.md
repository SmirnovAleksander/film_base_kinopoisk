E722 Do not use bare `except`
   --> main_parser.py:544:13
    |
542 |             try:
543 |                 self.db_connection.rollback()
544 |             except:
    |             ^^^^^^
545 |                 pass
546 |         finally:
    |

Found 1 error.