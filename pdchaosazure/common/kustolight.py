"""
Filter Azure resources with the Kusto query syntax.

The querying and filtering of resources is based on the Azure Kusto query syntax. Nevertheless we offer a subset
of the Kusto query syntax.

Working examples are:

* ``where instance_id=='0'``
* ``where instance_id=='0' or instance_id=='1 and/or ...``
* ``where instance_id=='0' or instance_id=='1' | sample 1``
* ``sample 1``
* Instead of the ``sample`` command you can put the ``take`` or ``top`` command.
* You may use the pipe operator to pipe and filter outputs
"""

import random
import re
from typing import List

import jmespath

operator_pattern = re.compile(r'[=><~]{1,2}')


def __split_clause(clause, delimiter):
    split = clause.strip().split(delimiter, 1)
    lhs = split[0].strip()
    rhs = split[1].strip()
    return lhs, rhs


def __and_or_expressions_to_jmespath(where_clause: str) -> str:
    result = ""
    expression_pattern = re.compile(r'[\s]+(?:and|or){1}[\s]+[\w]+[\s]*[=><~]{1,2}[\s]*[\']?[\w]*[\']?')
    expression_clauses = expression_pattern.findall(where_clause)

    for clause in expression_clauses:
        clause = clause.strip()
        operator = operator_pattern.findall(clause)[0]
        if clause.startswith('and'):
            expression_kustolight = 'and'
            expression_jmespath = '&&'
        else:
            expression_kustolight = 'or'
            expression_jmespath = '||'

        lhs, rhs = __split_clause(clause[len(expression_kustolight):], operator)
        result += " {} {} {} {}".format(expression_jmespath, lhs, operator, rhs)

    return result


def __where_clause_to_jmespath(where_clause: str):
    """ Transforms a Kusto light where clause to JMESPath syntax """

    # Regex patterns to find operator, where clauses and possible and/or expressions
    where_pattern = re.compile(r'where[\s]+[\w]+[\s]*[=><~]{1,2}[\s]*[\']?[\w]*[\']?')

    # Only one where clause is allowed - so we return it together with its operator
    found_where = where_pattern.findall(where_clause)[0]
    operator = operator_pattern.findall(found_where)[0]

    # Get the left hand side (key) and the right hand side (value) of the operator
    lhs, rhs = __split_clause(found_where[len('where'):], operator)

    return "[?{} {} {}".format(lhs, operator, rhs) + __and_or_expressions_to_jmespath(where_clause) + "]"


def __where_clauses_to_jmespath(kustolight_filter: str) -> str:
    """ Catches where clauses such as ``where instance_id == '0' and name=='i_0' or interval==30`` """
    result = kustolight_filter
    where_pattern = re.compile((r'where[\s]+[\w]+[\s]*[=><~]{1,2}[\s]*[\']?[\w]*[\']?'
                                r'(?:[\s]+(?:and|or){1}[\s]+[\w]+[\s]*[=><~]{2}[\s]*[\']?[\w]*[\']?)*'))
    where_clauses = where_pattern.findall(kustolight_filter)
    for kustol_clause in where_clauses:
        jmse_clause = __where_clause_to_jmespath(kustol_clause)
        result = result.replace(kustol_clause, jmse_clause, 1)

    return result


def __fetch_rows(resources: List[dict], command: str):
    command = __normalize_expression(command)

    if command.startswith('sample'):
        count = int(command[len('sample'):].strip())
        return random.sample(resources, count)

    elif command.startswith('top'):
        count = int(command[len('top'):].strip())
        return resources[:count]

    elif command.startswith('take'):
        count = int(command[len('top'):].strip())
        return resources[:count]

    else:
        raise Exception("Unknown command. Please select one of 'sample, take, top'")


def __normalize_expression(command):
    if command.startswith('|'):
        return command[1:].strip()
    else:
        return command.strip()


def __filter_resources(resources, kustol_filter: str) -> List[dict]:
    pattern = re.compile(r'\|{0,1}[\s]*(?:take|top|sample){1}[\s]+[\d]')
    taketopsample_list = pattern.findall(kustol_filter)

    if taketopsample_list:
        split = pattern.split(kustol_filter, 1)
        command = taketopsample_list[0]
        lhs = split[0] if split[0] else None
        rhs = split[1] if split[1] else None

        if lhs and rhs:
            jmes_filter = __where_clauses_to_jmespath(lhs)
            result = jmespath.search(jmes_filter, resources)
            resources = __fetch_rows(result, command)
            return __filter_resources(resources, rhs)
        elif lhs and not rhs:
            jmes_filter = __where_clauses_to_jmespath(lhs)
            result = jmespath.search(jmes_filter, resources)
            resources = __fetch_rows(result, command)
            return resources
        elif not lhs and rhs:
            resources = __fetch_rows(resources, command)
            return __filter_resources(resources, rhs)
        else:
            resources = __fetch_rows(resources, command)
            return resources

    else:
        jmes_filter = __where_clauses_to_jmespath(kustol_filter)
        result = jmespath.search(jmes_filter, resources)
        return result


def filter_resources(resources: List[dict], kustol_filter: str) -> List[dict]:
    if not resources:
        return resources

    return __filter_resources(resources, kustol_filter)
