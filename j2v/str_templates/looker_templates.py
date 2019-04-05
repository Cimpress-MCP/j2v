dimension_str_template = """
  dimension: {__dimension_name} {{
    description: \"{__desc}\"
    type: {looker_type}
    sql: ${{TABLE}}.{__path}::{json_type} ;;
  }}
    """

view_start_str_template = """
view: {name} {{ {base_table}
"""

view_end_str = """
}
"""

explore_start_str_template = """include: "{view_file_name}"
   
explore: {explore_name} {{
  view_name: {base_view_alias}
  from: {base_view}
  label: "{label}"
  description: "{description}"
"""

explore_join_str_template = """
  join: {alias} {{
     from: {view}
     sql:,{join_expression};;
     relationship: one_to_many {required_joins_line}
  }}
  """

req_joins_str_template = """
     required_joins: [{required_join}]"""

explore_end = """
}
"""
