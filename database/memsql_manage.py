# -*- coding: utf-8 -*-
__author__ = 'huzixu'

import os
import datetime
import sys
import traceback
import memsql_toolkit


def execute_sql(sql, action="qu"):
    result = None
    try:
        with memsql_toolkit.get_connection() as conn:
            if action == "qu":
                result = conn.query(sql)
            elif action == "up":
                print sql
                result = conn.execute(sql)
            else:
                pass
    except Exception, e:
        print e
        traceback.print_exc()
        sys.exit(1)
    finally:
        print()
    return result
